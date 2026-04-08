"""
语料管理API路由
提供语料上传、查询、删除等功能
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import shutil
from pathlib import Path
import uuid

from database import get_db
from models.db_models import Corpus, Image, DatasetCorpus
from services.storage_service import storage_service
from models.schemas import (
    CorpusRecord, CorpusListResponse, ExcelUploadResponse,
    ImageInfo, SuccessResponse
)
from services.excel_processing import ExcelProcessingService
from config import settings

router = APIRouter(prefix="/api/v1/corpus", tags=["corpus"])


def _delete_corpus_records(db: Session, corpus_list: list) -> SuccessResponse:
    """
    通用删除逻辑：阻止删除已被数据集引用的语料。
    """
    if not corpus_list:
        raise HTTPException(status_code=404, detail="未找到匹配的语料")

    corpus_ids = [c.id for c in corpus_list]
    text_id_map = {c.id: c.text_id for c in corpus_list}

    used_ids = {
        cid
        for (cid,) in db.query(DatasetCorpus.corpus_id)
        .filter(DatasetCorpus.corpus_id.in_(corpus_ids))
        .all()
    }
    deletable_ids = [cid for cid in corpus_ids if cid not in used_ids]

    if not deletable_ids:
        raise HTTPException(
            status_code=400,
            detail="语料已被数据集索引，请先在相关数据集中移除后再删除"
        )

    # 删除物理图片文件
    image_paths = [
        path for (path,) in db.query(Image.file_path)
        .filter(Image.corpus_id.in_(deletable_ids))
        .all()
    ]
    for path in image_paths:
        storage_service.delete_image(path)

    db.query(Corpus).filter(Corpus.id.in_(deletable_ids)).delete(
        synchronize_session=False
    )
    db.commit()

    return SuccessResponse(
        success=True,
        message=f"成功删除 {len(deletable_ids)} 条，跳过 {len(used_ids)} 条已被数据集引用",
        data={
            "deleted": len(deletable_ids),
            "skipped": len(used_ids),
            "skipped_text_ids": [text_id_map[cid] for cid in used_ids],
        },
    )


@router.post("/upload", response_model=ExcelUploadResponse)
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传Excel文件并处理
    
    - 验证文件格式
    - 提取WPS内嵌图片
    - 解析表格数据
    - 生成语料记录
    """
    # 验证文件类型
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="仅支持Excel文件格式（.xlsx, .xls）"
        )
    
    # 保存上传的文件
    upload_id = uuid.uuid4().hex[:16]
    file_path = settings.UPLOAD_DIR / f"{upload_id}_{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 创建Excel处理服务
        excel_service = ExcelProcessingService(db)
        
        # 验证Excel文件
        validation_result = excel_service.validate_excel_file(str(file_path))
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Excel文件验证失败: {validation_result['error']}"
            )
        
        # 处理Excel文件
        result = excel_service.process_excel_file(
            str(file_path),
            file.filename
        )
        
        # 统计各字段的句子分布
        field_distribution = {}
        for corpus_id in result["corpus_ids"]:
            corpus = db.query(Corpus).filter(Corpus.text_id == corpus_id).first()
            if corpus and corpus.source_field:
                field_distribution[corpus.source_field] = field_distribution.get(corpus.source_field, 0) + 1
        
        return ExcelUploadResponse(
            success=True,
            message=f"成功处理文件 {file.filename}",
            total_records=result["corpus_count"],
            total_sentences=result["sentence_count"],
            total_images=result["image_count"],
            field_distribution=field_distribution
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理文件时出错: {str(e)}"
        )
    finally:
        # 清理上传的临时文件
        if file_path.exists():
            file_path.unlink()


@router.get("", response_model=CorpusListResponse)
async def get_corpus_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=1000, description="每页数量"),  # 提高到1000
    source_file: Optional[str] = Query(None, description="按文件名筛选"),
    source_field: Optional[str] = Query(None, description="按字段分类筛选"),
    has_images: Optional[bool] = Query(None, description="是否包含图片"),
    db: Session = Depends(get_db)
):
    """
    获取语料列表
    
    - 支持分页
    - 支持按文件名筛选
    - 支持按字段分类筛选
    - 支持按是否包含图片筛选
    """
    # 构建查询
    query = db.query(Corpus)
    
    # 应用筛选条件
    if source_file:
        query = query.filter(Corpus.source_file.like(f"%{source_file}%"))
    if source_field:
        query = query.filter(Corpus.source_field == source_field)
    if has_images is not None:
        query = query.filter(Corpus.has_images == has_images)
    
    # 获取总数
    total = query.count()
    
    # 分页查询
    offset = (page - 1) * page_size
    corpus_list = query.order_by(Corpus.created_at.desc()).offset(offset).limit(page_size).all()
    
    # 构建响应
    items = []
    for corpus in corpus_list:
        # 获取关联的图片
        images = db.query(Image).filter(Image.corpus_id == corpus.id).all()
        image_infos = [
            ImageInfo(
                image_id=img.image_id,
                file_path=img.file_path,
                original_name=img.original_name,
                width=img.width,
                height=img.height
            )
            for img in images
        ]
        
        items.append(CorpusRecord(
            id=corpus.id,  # 添加数据库ID
            text_id=corpus.text_id,
            text=corpus.text,
            text_type=corpus.text_type,
            source_file=corpus.source_file,
            source_row=corpus.source_row,
            source_field=corpus.source_field,
            has_images=corpus.has_images,
            images=image_infos,
            created_at=corpus.created_at
        ))
    
    return CorpusListResponse(
        total=total,
        items=items
    )


@router.get("/{corpus_id}", response_model=CorpusRecord)
async def get_corpus_detail(
    corpus_id: str,
    db: Session = Depends(get_db)
):
    """
    获取语料详情
    
    - 返回完整的语料信息
    - 包含关联的图片列表
    """
    # 查询语料
    corpus = db.query(Corpus).filter(Corpus.text_id == corpus_id).first()
    
    if not corpus:
        raise HTTPException(
            status_code=404,
            detail=f"语料 {corpus_id} 不存在"
        )

    # 阻止删除已被数据集引用的语料
    used = db.query(DatasetCorpus).filter(DatasetCorpus.corpus_id == corpus.id).first()
    if used:
        raise HTTPException(
            status_code=400,
            detail="语料已被数据集索引，请先在相关数据集中移除后再删除"
        )
    
    # 获取关联的图片
    images = db.query(Image).filter(Image.corpus_id == corpus.id).all()
    image_infos = [
        ImageInfo(
            image_id=img.image_id,
            file_path=img.file_path,
            original_name=img.original_name,
            width=img.width,
            height=img.height
        )
        for img in images
    ]
    
    return CorpusRecord(
        id=corpus.id,  # 添加数据库ID
        text_id=corpus.text_id,
        text=corpus.text,
        text_type=corpus.text_type,
        source_file=corpus.source_file,
        source_row=corpus.source_row,
        source_field=corpus.source_field,
        has_images=corpus.has_images,
        images=image_infos,
        created_at=corpus.created_at
    )


@router.delete("/by-file", response_model=SuccessResponse)
async def delete_corpus_by_file(
    source_file: str = Query(..., description="Source file name (exact match)"),
    db: Session = Depends(get_db)
):
    """
    Delete all corpus records under a file. Records referenced by datasets are skipped and reported.
    """
    corpus_list = db.query(Corpus).filter(Corpus.source_file == source_file).all()
    return _delete_corpus_records(db, corpus_list)


@router.delete("/by-row", response_model=SuccessResponse)
async def delete_corpus_by_row(
    source_file: str = Query(..., description="Source file name (exact match)"),
    source_row: int = Query(..., description="Excel row number"),
    db: Session = Depends(get_db)
):
    """
    Delete all corpus records in a specific file row. Records referenced by datasets are skipped and reported.
    """
    corpus_list = db.query(Corpus).filter(
        Corpus.source_file == source_file,
        Corpus.source_row == source_row
    ).all()
    return _delete_corpus_records(db, corpus_list)


@router.delete("/{corpus_id}", response_model=SuccessResponse)
async def delete_corpus(
    corpus_id: str,
    db: Session = Depends(get_db)
):
    """
    删除语料
    
    - 删除语料记录
    - 级联删除关联的图片记录
    - 注意：不会删除物理图片文件
    """
    # 查询语料
    corpus = db.query(Corpus).filter(Corpus.text_id == corpus_id).first()

    if not corpus:
        raise HTTPException(
            status_code=404,
            detail=f"语料 {corpus_id} 不存在"
        )
    
    try:
        # 删除物理图片文件
        image_paths = [img.file_path for img in db.query(Image).filter(Image.corpus_id == corpus.id).all()]
        for path in image_paths:
            storage_service.delete_image(path)

        # 删除语料（级联删除会自动删除关联的图片记录）
        db.delete(corpus)
        db.commit()
        
        return SuccessResponse(
            success=True,
            message=f"成功删除语料 {corpus_id}"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"删除语料时出错: {str(e)}"
        )


@router.get("/{corpus_id}/images", response_model=List[ImageInfo])
async def get_corpus_images(
    corpus_id: str,
    db: Session = Depends(get_db)
):
    """
    获取语料关联的图片列表
    
    - 返回该语料的所有关联图片
    """
    # 查询语料
    corpus = db.query(Corpus).filter(Corpus.text_id == corpus_id).first()
    
    if not corpus:
        raise HTTPException(
            status_code=404,
            detail=f"语料 {corpus_id} 不存在"
        )
    
    # 获取关联的图片
    images = db.query(Image).filter(Image.corpus_id == corpus.id).all()
    
    return [
        ImageInfo(
            image_id=img.image_id,
            file_path=img.file_path,
            original_name=img.original_name,
            width=img.width,
            height=img.height
        )
        for img in images
    ]
