"""
统一文档导入API
提供Excel上传、处理、导入图谱的统一入口
"""
import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import shutil
import zipfile
from pathlib import Path

from database import get_db
from api.users import get_current_user
from services.document_processor import DocumentProcessor
from services.data_parser import DataParser
from services.graph_builder import GraphBuilder
from services.qms_graph_builder import QMSGraphBuilder
from services.excel_processing import ExcelProcessingService
from config import settings
from models.db_models import QuickResponseEvent, QMSDefectOrder

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])
logger = logging.getLogger(__name__)


def _count_imported_records_by_source(db: Session, processor_name: str, data_source: str) -> int:
    """Count imported records for one processor/data_source pair."""
    if processor_name == 'kf':
        return db.query(QuickResponseEvent).filter(
            QuickResponseEvent.data_source == data_source
        ).count()
    if processor_name == 'qms':
        return db.query(QMSDefectOrder).filter(
            QMSDefectOrder.data_source == data_source
        ).count()
    return 0


def _build_graph_importer(processor_name: str):
    """Get parser and graph builder for graph-style processors."""
    parser = DataParser(processor_name=processor_name)
    if processor_name == 'kf':
        return parser, GraphBuilder()
    if processor_name == 'qms':
        return parser, QMSGraphBuilder()
    return parser, GraphBuilder()


def _import_processed_records(
    db: Session,
    processor_name: str,
    data_source: str,
) -> dict:
    """Import processed JSON records into the workflow database."""
    json_dir = settings.PROCESSED_DIR / processor_name / data_source

    if not json_dir.exists():
        raise HTTPException(status_code=404, detail=f"目录不存在: {json_dir}")

    json_files = list(json_dir.glob("*.json"))
    if not json_files:
        raise HTTPException(status_code=404, detail=f"目录下没有JSON文件: {json_dir}")

    parser, graph_builder = _build_graph_importer(processor_name)

    total_records = 0
    inserted_records = 0
    skipped_records = 0
    failed_records = 0
    error_samples = []
    skipped_samples: list[str] = []  # 被跳过记录的 event_id 样本（最多 5 条）

    for json_file in json_files:
        records = parser.parse_json_file(str(json_file))

        for record in records:
            total_records += 1
            entities = parser.extract_entities(record, data_source=data_source)
            record_id = (
                record.get('制令单号')
                or record.get('快反编号')
                or record.get('event_id')
                or record.get('id')
                or f"row_{total_records}"
            )

            try:
                success = graph_builder.build_graph(db, entities, skip_if_exists=True)
                if success:
                    inserted_records += 1
                else:
                    skipped_records += 1
                    if len(skipped_samples) < 5 and record_id:
                        skipped_samples.append(str(record_id))
            except Exception as exc:
                failed_records += 1
                db.rollback()
                logger.exception(
                    "导入记录失败: processor=%s data_source=%s record_id=%s",
                    processor_name,
                    data_source,
                    record_id,
                )
                if len(error_samples) < 10:
                    error_samples.append({
                        "record_id": str(record_id),
                        "error": str(exc),
                    })
                continue

    database_records = _count_imported_records_by_source(db, processor_name, data_source)
    logger.info(
        "导入汇总: processor=%s data_source=%s total=%d inserted=%d skipped=%d failed=%d db_total=%d",
        processor_name, data_source,
        total_records, inserted_records, skipped_records, failed_records, database_records,
    )
    if skipped_records > 0:
        logger.info(
            "跳过原因：记录已存在于数据库（按 event_id 或内容哈希去重）。"
            "如需强制覆盖，请先删除该数据源后重新导入。"
        )
    if total_records > 0 and inserted_records == 0 and database_records == 0:
        raise HTTPException(
            status_code=500,
            detail=(
                f"导入未写入数据库: processor={processor_name}, "
                f"data_source={data_source}, total_records={total_records}"
            )
        )

    return {
        "total_records": total_records,
        "inserted_records": inserted_records,
        "skipped_records": skipped_records,
        "failed_records": failed_records,
        "database_records": database_records,
        "error_samples": error_samples,
        "skipped_samples": skipped_samples,
        "processed_files": len(json_files),
    }


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    processor_name: str = Form(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传Excel文件并处理

    - 将上传文件保存到 data/uploads/ 临时目录
    - 实例化 DocumentProcessor 解析Excel
    - 如果是重复文件，返回提示信息
    - 如果 processor_name == 'failure_case'，额外调用 ExcelProcessingService
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="仅支持Excel文件格式（.xlsx, .xls）")

    # 临时文件按处理器隔离到子目录，避免不同处理器同名文件冲突
    upload_subdir = settings.UPLOAD_DIR / processor_name
    upload_subdir.mkdir(parents=True, exist_ok=True)
    file_path = upload_subdir / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc_processor = DocumentProcessor(processor_name=processor_name)
        result = doc_processor.process_excel(str(file_path), file.filename)

        if not result.get('success'):
            return {
                "success": False,
                "message": result.get('message', '处理失败'),
            }

        if result.get('is_duplicate'):
            return {
                "success": True,
                "is_duplicate": True,
                "message": result.get('message', '文件已处理过'),
                "data_source": result.get('data_source'),
                "output_dir": result.get('output_dir')
            }

        corpus_count = 0
        auto_import_result = None
        if processor_name == 'failure_case':
            excel_service = ExcelProcessingService(db)
            corpus_result = excel_service.process_excel_file(str(file_path), file.filename)
            corpus_count = corpus_result.get('corpus_count', 0)
        elif processor_name in {'kf', 'qms'}:
            auto_import_result = _import_processed_records(db, processor_name, result['data_source'])

        response = {
            "success": True,
            "is_duplicate": False,
            "message": result.get('message', '文件处理成功'),
            "data_source": result.get('data_source'),
            "output_dir": result.get('output_dir'),
            "table_count": result.get('table_count'),
            "image_count": result.get('image_count'),
            "json_files": result.get('json_files', []),
            "corpus_count": corpus_count
        }

        if auto_import_result is not None:
            response.update(auto_import_result)
            response["message"] = (
                f"{result.get('message', '文件处理成功')}，"
                f"已自动导入主流程数据库 {auto_import_result['inserted_records']} 条，"
                f"跳过 {auto_import_result['skipped_records']} 条"
            )

        return response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"处理文件时出错: {str(e)}")
    finally:
        if file_path.exists():
            file_path.unlink()


@router.post("/import")
async def import_documents(
    processor_name: str = Form(...),
    data_source: str = Form(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    将处理好的JSON文件导入图谱数据库

    - 找到 data/processed/{processor_name}/{data_source}/ 目录下的所有JSON文件
    - 使用 DataParser 解析每条记录
    - 使用 GraphBuilder 或 QMSGraphBuilder 写入数据库
    """
    try:
        import_result = _import_processed_records(db, processor_name, data_source)
        return {
            "success": True,
            "message": "导入完成",
            **import_result,
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")


@router.post("/images")
async def upload_images(
    file: UploadFile = File(...),
    data_source: str = Form(...),
    processor_name: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """
    上传图片ZIP文件并解压到 data/images/{data_source}/ 目录。
    仅限 QMS 处理器使用：KF 图片内嵌于 Excel，无需外部上传；
    品质案例处理器使用独立图片目录，不走此接口。
    """
    if processor_name != 'qms':
        raise HTTPException(
            status_code=400,
            detail="图片上传仅适用于 QMS 处理器。KF 快反的图片直接内嵌于 Excel 文件中，无需单独上传。"
        )

    # 图片解压到 parser 实际查找的目录：data/processed/qms/{data_source}/imgs/
    images_dir = settings.PROCESSED_DIR / 'qms' / data_source / 'imgs'
    images_dir.mkdir(parents=True, exist_ok=True)

    zip_path = images_dir / f"{data_source}_upload.zip"

    try:
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(images_dir)

        extracted_count = len(list(images_dir.glob("**/*.*")))

        return {
            "success": True,
            "message": f"成功解压 {extracted_count} 个文件",
            "data_source": data_source,
            "images_dir": str(images_dir)
        }

    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="无效的ZIP文件")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")
    finally:
        if zip_path.exists():
            zip_path.unlink()


@router.get("/images")
async def get_images_info(
    data_source: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """
    查询指定数据源的已上传图片数量
    """
    images_dir = settings.PROCESSED_DIR / 'qms' / data_source / 'imgs'
    if not images_dir.exists():
        return {"success": True, "count": 0, "images_dir": str(images_dir)}

    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    count = sum(
        1 for f in images_dir.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    )
    return {"success": True, "count": count, "images_dir": str(images_dir)}


@router.get("/processed-files")
async def get_processed_files(
    processor_name: str = Query(..., description="处理器名称 (kf/qms/failure_case)"),
    current_user: dict = Depends(get_current_user)
):
    """
    获取已处理文件列表
    """
    try:
        doc_processor = DocumentProcessor(processor_name=processor_name)
        files = doc_processor.get_processed_files()

        return {
            "success": True,
            "processor_name": processor_name,
            "files": files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")


@router.delete("/processed-files")
async def delete_processed_file(
    processor_name: str = Query(...),
    data_source: str = Query(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    彻底删除指定数据源的所有数据：
    - 从 file_hashes.json 中移除记录
    - 删除 data/processed/{processor_name}/{data_source}/ 目录
    - 从数据库中删除该数据源的所有相关记录
    """
    import shutil as _shutil
    from models.db_models import QuickResponseEvent, QMSDefectOrder, Corpus, DatasetCorpus
    from services.storage_service import storage_service

    try:
        doc_processor = DocumentProcessor(processor_name=processor_name)

        # 从哈希记录中找到原始文件名（failure_case 需要）并移除条目
        original_filename = None
        removed = False
        for file_hash, record in list(doc_processor.file_hashes.items()):
            if record.get('data_source') == data_source:
                original_filename = record.get('original_filename', '')
                del doc_processor.file_hashes[file_hash]
                removed = True
                break

        if not removed:
            raise HTTPException(status_code=404, detail=f"未找到数据源记录: {data_source}")

        doc_processor._save_hashes()

        # 删除处理结果目录
        output_dir = settings.PROCESSED_DIR / processor_name / data_source
        if output_dir.exists():
            _shutil.rmtree(output_dir)

        # 删除数据库记录
        db_deleted = 0
        if processor_name == 'kf':
            result = db.query(QuickResponseEvent).filter(
                QuickResponseEvent.data_source == data_source
            ).delete(synchronize_session=False)
            db_deleted = result
            db.commit()
        elif processor_name == 'qms':
            result = db.query(QMSDefectOrder).filter(
                QMSDefectOrder.data_source == data_source
            ).delete(synchronize_session=False)
            db_deleted = result
            db.commit()
        elif processor_name == 'failure_case' and original_filename:
            # 与语料管理对齐：跳过已被数据集引用的语料，只删除可删除的
            corpus_records = db.query(Corpus).filter(
                Corpus.source_file == original_filename
            ).all()

            if not corpus_records:
                db_deleted = 0
            else:
                corpus_ids = [c.id for c in corpus_records]
                used_ids = {
                    cid
                    for (cid,) in db.query(DatasetCorpus.corpus_id)
                    .filter(DatasetCorpus.corpus_id.in_(corpus_ids))
                    .all()
                }
                deletable = [c for c in corpus_records if c.id not in used_ids]
                skipped = len(used_ids)

                # 先删物理图片文件
                from models.db_models import Image
                deletable_ids = [c.id for c in deletable]
                image_paths = [
                    path for (path,) in db.query(Image.file_path)
                    .filter(Image.corpus_id.in_(deletable_ids))
                    .all()
                ]
                for path in image_paths:
                    storage_service.delete_image(path)

                for c in deletable:
                    db.delete(c)
                db.commit()
                db_deleted = len(deletable)

                if skipped > 0:
                    return {
                        "success": True,
                        "message": (
                            f"已删除数据源 {data_source}，"
                            f"清理语料 {db_deleted} 条，"
                            f"跳过 {skipped} 条已被数据集引用（需先在数据集中移除）"
                        )
                    }

        return {
            "success": True,
            "message": f"已删除数据源 {data_source}，清理数据库记录 {db_deleted} 条"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
