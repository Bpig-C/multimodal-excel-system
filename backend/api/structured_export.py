"""
语料导出API
提供三种格式的数据导出：实体文本、CLIP对齐、Q&A对齐
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import json
import io
import logging
import time
import zipfile
import tempfile
import os

from api.users import get_current_user
from services.structured_export_service import StructuredExportService
from services.data_parser import DataParser
from config import settings

router = APIRouter(prefix="/api/v1/export/corpus", tags=["export"])

logger = logging.getLogger(__name__)


def _get_json_files_for_data_source(processor_name: str, data_source: str = None) -> list:
    """
    获取JSON文件列表

    Args:
        processor_name: 处理器名称
        data_source: 数据源名称（可选）

    Returns:
        JSON文件路径列表
    """
    if data_source:
        json_dir = settings.PROCESSED_DIR / processor_name / data_source
    else:
        json_dir = settings.PROCESSED_DIR / processor_name

    if not json_dir.exists():
        logger.warning(f"目录不存在: {json_dir}")
        return []

    # 查找所有page_*.json文件
    json_files = sorted(json_dir.glob('page_*.json'))
    if json_files:
        return json_files

    # 如果没有page_*.json，查找所有.json文件
    json_files = sorted(json_dir.glob('*.json'))
    return json_files


class ExportRequest(BaseModel):
    """导出请求模型"""
    data_sources: list = []  # 数据源列表，空列表表示全部


class BatchExportRequest(BaseModel):
    """批量导出请求模型"""
    data_sources: list = []  # 数据源列表，空列表表示全部
    formats: list = ["entity_text", "clip_alignment", "qa_alignment"]  # 导出格式列表
    include_images: bool = True


@router.post("/{processor_name}/entity-text")
async def export_entity_text(
    processor_name: str,
    request: ExportRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    导出实体标注文本格式
    """
    start_time = time.time()
    format_type = "entity_text"

    try:
        # 获取JSON文件
        if request.data_sources:
            json_files = []
            for ds in request.data_sources:
                files = _get_json_files_for_data_source(processor_name, ds)
                json_files.extend(files)
        else:
            # 导出全部
            json_files = _get_json_files_for_data_source(processor_name)

        if not json_files:
            return {"success": True, "data": [], "count": 0}

        # 解析所有JSON文件
        parser = DataParser(processor_name=processor_name)
        all_records = []
        for json_file in json_files:
            records = parser.parse_json_file(str(json_file))
            # 标记数据源
            data_source = json_file.parent.name
            for record in records:
                record['_data_source'] = data_source
            all_records.extend(records)

        # 导出
        exporter = StructuredExportService(processor_name=processor_name)
        results = exporter.export_entity_text(all_records)

        duration = time.time() - start_time
        logger.info(f"[EXPORT] 格式={format_type}, 记录数={len(results)}, 耗时={duration:.2f}秒")

        return {"success": True, "data": results, "count": len(results)}

    except Exception as e:
        logger.error(f"[EXPORT_ERROR] {format_type}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.post("/{processor_name}/clip-alignment")
async def export_clip_alignment(
    processor_name: str,
    request: ExportRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    导出CLIP风格的图文对齐格式
    """
    start_time = time.time()
    format_type = "clip_alignment"

    try:
        # 获取JSON文件
        if request.data_sources:
            json_files = []
            for ds in request.data_sources:
                files = _get_json_files_for_data_source(processor_name, ds)
                json_files.extend(files)
        else:
            json_files = _get_json_files_for_data_source(processor_name)

        if not json_files:
            return {"success": True, "data": [], "count": 0}

        # 解析所有JSON文件
        parser = DataParser(processor_name=processor_name)
        all_records = []
        for json_file in json_files:
            records = parser.parse_json_file(str(json_file))
            data_source = json_file.parent.name
            for record in records:
                record['_data_source'] = data_source
            all_records.extend(records)

        # 导出
        exporter = StructuredExportService(processor_name=processor_name)
        results = exporter.export_clip_alignment(all_records)

        duration = time.time() - start_time
        logger.info(f"[EXPORT] 格式={format_type}, 记录数={len(results)}, 耗时={duration:.2f}秒")

        return {"success": True, "data": results, "count": len(results)}

    except Exception as e:
        logger.error(f"[EXPORT_ERROR] {format_type}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.post("/{processor_name}/qa-alignment")
async def export_qa_alignment(
    processor_name: str,
    request: ExportRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    导出Q&A风格的多模态对齐格式
    """
    start_time = time.time()
    format_type = "qa_alignment"

    try:
        # 获取JSON文件
        if request.data_sources:
            json_files = []
            for ds in request.data_sources:
                files = _get_json_files_for_data_source(processor_name, ds)
                json_files.extend(files)
        else:
            json_files = _get_json_files_for_data_source(processor_name)

        if not json_files:
            return {"success": True, "data": [], "count": 0}

        # 解析所有JSON文件
        parser = DataParser(processor_name=processor_name)
        all_records = []
        for json_file in json_files:
            records = parser.parse_json_file(str(json_file))
            data_source = json_file.parent.name
            for record in records:
                record['_data_source'] = data_source
            all_records.extend(records)

        # 导出
        exporter = StructuredExportService(processor_name=processor_name)
        results = exporter.export_qa_alignment(all_records)

        duration = time.time() - start_time
        logger.info(f"[EXPORT] 格式={format_type}, 记录数={len(results)}, 耗时={duration:.2f}秒")

        return {"success": True, "data": results, "count": len(results)}

    except Exception as e:
        logger.error(f"[EXPORT_ERROR] {format_type}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.post("/{processor_name}/batch")
async def batch_export(
    processor_name: str,
    request: BatchExportRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    批量导出多个文件的多种格式，并打包ZIP
    """
    start_time = time.time()
    temp_file_path = None

    try:
        # 获取JSON文件
        if request.data_sources:
            json_files = []
            for ds in request.data_sources:
                files = _get_json_files_for_data_source(processor_name, ds)
                json_files.extend(files)
        else:
            json_files = _get_json_files_for_data_source(processor_name)

        if not json_files:
            raise HTTPException(status_code=404, detail="未找到JSON文件")

        # 解析所有JSON文件
        parser = DataParser(processor_name=processor_name)
        all_records = []
        for json_file in json_files:
            records = parser.parse_json_file(str(json_file))
            data_source = json_file.parent.name
            for record in records:
                record['_data_source'] = data_source
            all_records.extend(records)

        # 导出
        exporter = StructuredExportService(processor_name=processor_name)
        results = exporter.batch_export(all_records, request.formats, request.include_images)

        # 创建临时ZIP文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_file_path = temp_file.name
        temp_file.close()

        with zipfile.ZipFile(temp_file_path, 'w', zipfile.ZIP_STORED) as zip_file:
            for fmt in request.formats:
                if fmt == 'entity_text' and 'entity_text' in results:
                    json_str = json.dumps(results['entity_text'], ensure_ascii=False, indent=2)
                    zip_file.writestr(f"entity_text_ALL_{timestamp}.json", json_str)
                elif fmt == 'clip_alignment' and 'clip_alignment' in results:
                    json_str = json.dumps(results['clip_alignment'], ensure_ascii=False, indent=2)
                    zip_file.writestr(f"clip_alignment_ALL_{timestamp}.json", json_str)
                elif fmt == 'qa_alignment' and 'qa_alignment' in results:
                    json_str = json.dumps(results['qa_alignment'], ensure_ascii=False, indent=2)
                    zip_file.writestr(f"qa_alignment_ALL_{timestamp}.json", json_str)

            # 打包图片文件
            if request.include_images and 'image_files' in results:
                for zip_path, local_path in results['image_files']:
                    try:
                        zip_file.write(local_path, zip_path)
                    except Exception as img_err:
                        logger.warning(f"图片打包跳过 {local_path}: {img_err}")

        file_size = os.path.getsize(temp_file_path)
        duration = time.time() - start_time

        logger.info(f"[BATCH_EXPORT] 格式数={len(request.formats)}, 记录数={len(all_records)}, "
                    f"耗时={duration:.2f}秒, 文件大小={file_size}字节")

        # 返回ZIP文件
        from starlette.background import BackgroundTask
        zip_filename = f"corpus_export_{processor_name}_{timestamp}.zip"

        return StreamingResponse(
            io.FileIO(temp_file_path, 'rb'),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{zip_filename}",
                "Content-Length": str(file_size)
            },
            background=BackgroundTask(lambda: os.unlink(temp_file_path) if os.path.exists(temp_file_path) else None)
        )

    except HTTPException:
        raise
    except Exception as e:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass
        logger.error(f"[BATCH_EXPORT_ERROR]: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"批量导出失败: {str(e)}")
