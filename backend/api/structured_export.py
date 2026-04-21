"""
Structured export API.
"""

from __future__ import annotations

import io
import json
import logging
import queue
import threading
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Generator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.users import get_current_user
from config import settings
from database import get_db
from services.data_parser import DataParser
from services.query_engine import QueryEngine
from services.structured_export_service import StructuredExportService
from utils.file_utils import sanitize_filename

router = APIRouter(prefix="/api/v1/export/corpus", tags=["export"])
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Streaming ZIP helpers
# ---------------------------------------------------------------------------

class _QueueWriter(io.RawIOBase):
    """Non-seekable writable that pushes bytes into a queue for streaming."""

    def __init__(self, q: "queue.Queue[bytes | None]") -> None:
        self._q = q

    def write(self, b: bytes) -> int:  # type: ignore[override]
        if b:
            self._q.put(bytes(b))
        return len(b)

    def writable(self) -> bool:
        return True


def _iter_streaming_zip(
    entries: list[tuple[str, bytes | Path]],
) -> Generator[bytes, None, None]:
    """
    Yield ZIP bytes incrementally as files are added, without a temp file.

    entries: list of (zip_internal_path, source)
      source may be raw bytes (for JSON) or a Path (for image files).
    """
    chunk_q: queue.Queue[bytes | None] = queue.Queue(maxsize=128)

    def _writer() -> None:
        writer = _QueueWriter(chunk_q)
        try:
            with zipfile.ZipFile(
                writer, mode="w", compression=zipfile.ZIP_STORED, allowZip64=True
            ) as zf:
                for zip_path, source in entries:
                    if isinstance(source, Path):
                        zf.write(str(source), zip_path)
                    else:
                        zf.writestr(zip_path, source)
        except Exception as exc:
            logger.error("Streaming ZIP writer error: %s", exc, exc_info=True)
        finally:
            chunk_q.put(None)  # sentinel

    t = threading.Thread(target=_writer, daemon=True)
    t.start()

    while True:
        chunk = chunk_q.get()
        if chunk is None:
            break
        yield chunk



def _get_json_files_for_data_source(processor_name: str, data_source: str | None = None) -> list[Path]:
    if data_source:
        json_dir = settings.PROCESSED_DIR / processor_name / data_source
    else:
        json_dir = settings.PROCESSED_DIR / processor_name

    if not json_dir.exists():
        logger.warning("Export source directory does not exist: %s", json_dir)
        return []

    json_files = sorted(json_dir.glob("page_*.json"))
    if json_files:
        return json_files

    return sorted(json_dir.glob("*.json"))


def _build_failure_case_export_records(
    db: Session,
    data_sources: list[str] | None = None,
) -> list[dict]:
    engine = QueryEngine(processor_name="failure_case")
    grouped_records = engine._get_failure_case_list(db, limit=1_000_000, offset=0)
    selected_sources = {str(item).strip() for item in (data_sources or []) if str(item).strip()}

    export_records: list[dict] = []
    for grouped in grouped_records:
        source_file = (grouped.get("source_file") or "").strip()
        data_source = sanitize_filename(Path(source_file).stem or source_file)
        if selected_sources and data_source not in selected_sources:
            continue

        image_paths = [str(path).strip() for path in (grouped.get("image_paths") or []) if str(path).strip()]
        record = {
            field: grouped.get(field, "") or ""
            for field in QueryEngine.FAILURE_CASE_REQUIRED_FIELDS
        }
        record["_data_source"] = data_source
        record["_image_paths"] = image_paths
        record["图片"] = f"![图片]({image_paths[0]})" if image_paths else ""
        export_records.append(record)

    return export_records


def _load_export_records(
    processor_name: str,
    data_sources: list[str] | None,
    db: Session,
) -> list[dict]:
    if processor_name == "failure_case":
        return _build_failure_case_export_records(db, data_sources)

    if data_sources:
        json_files: list[Path] = []
        for ds in data_sources:
            json_files.extend(_get_json_files_for_data_source(processor_name, ds))
    else:
        json_files = _get_json_files_for_data_source(processor_name)

    if not json_files:
        return []

    parser = DataParser(processor_name=processor_name)
    all_records: list[dict] = []
    for json_file in json_files:
        records = parser.parse_json_file(str(json_file))
        data_source = json_file.parent.name
        for record in records:
            record["_data_source"] = data_source
        all_records.extend(records)

    return all_records


class ExportRequest(BaseModel):
    data_sources: list[str] = []


class BatchExportRequest(BaseModel):
    data_sources: list[str] = []
    formats: list[str] = ["entity_text", "clip_alignment", "qa_alignment"]
    include_images: bool = True


@router.post("/{processor_name}/entity-text")
async def export_entity_text(
    processor_name: str,
    request: ExportRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    start_time = time.time()
    try:
        all_records = _load_export_records(processor_name, request.data_sources, db)
        if not all_records:
            return {"success": True, "data": [], "count": 0}

        exporter = StructuredExportService(processor_name=processor_name)
        results = exporter.export_entity_text(all_records)
        logger.info("[EXPORT] format=entity_text records=%s duration=%.2fs", len(results), time.time() - start_time)
        return {"success": True, "data": results, "count": len(results)}
    except Exception as exc:
        logger.error("[EXPORT_ERROR] entity_text: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {exc}")


@router.post("/{processor_name}/clip-alignment")
async def export_clip_alignment(
    processor_name: str,
    request: ExportRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    start_time = time.time()
    try:
        all_records = _load_export_records(processor_name, request.data_sources, db)
        if not all_records:
            return {"success": True, "data": [], "count": 0}

        exporter = StructuredExportService(processor_name=processor_name)
        results = exporter.export_clip_alignment(all_records)
        logger.info("[EXPORT] format=clip_alignment records=%s duration=%.2fs", len(results), time.time() - start_time)
        return {"success": True, "data": results, "count": len(results)}
    except Exception as exc:
        logger.error("[EXPORT_ERROR] clip_alignment: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {exc}")


@router.post("/{processor_name}/qa-alignment")
async def export_qa_alignment(
    processor_name: str,
    request: ExportRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    start_time = time.time()
    try:
        all_records = _load_export_records(processor_name, request.data_sources, db)
        if not all_records:
            return {"success": True, "data": [], "count": 0}

        exporter = StructuredExportService(processor_name=processor_name)
        results = exporter.export_qa_alignment(all_records)
        logger.info("[EXPORT] format=qa_alignment records=%s duration=%.2fs", len(results), time.time() - start_time)
        return {"success": True, "data": results, "count": len(results)}
    except Exception as exc:
        logger.error("[EXPORT_ERROR] qa_alignment: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {exc}")


@router.post("/{processor_name}/batch/info")
async def batch_export_info(
    processor_name: str,
    request: BatchExportRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    快速预查询导出总大小，供前端进度条使用。

    策略（避免序列化全量数据导致超时）：
    - JSON 大小：采样前 10 条记录序列化，计算均值后外推全量
    - 图片大小：直接 stat() 扫描各数据源的 imgs 目录，不读取内容
    """
    try:
        all_records = _load_export_records(processor_name, request.data_sources, db)
        record_count = len(all_records)
        if record_count == 0:
            return {"total_bytes": 0, "record_count": 0, "image_count": 0}

        total_bytes = 0

        # --- JSON 大小估算：采样 10 条，外推全量 ---
        if request.formats:
            exporter = StructuredExportService(processor_name=processor_name)
            sample = all_records[: min(10, record_count)]
            sample_results = exporter.batch_export(sample, request.formats, include_images=False)
            sample_bytes = sum(
                len(json.dumps(sample_results[fmt], ensure_ascii=False, indent=2).encode())
                for fmt in request.formats
                if fmt in sample_results
            )
            avg_per_record = sample_bytes / len(sample)
            total_bytes += int(avg_per_record * record_count)

        # --- 图片大小：仅 stat()，不读内容 ---
        image_count = 0
        if request.include_images:
            data_sources = request.data_sources or []
            if not data_sources:
                proc_dir = settings.PROCESSED_DIR / processor_name
                if proc_dir.exists():
                    data_sources = [d.name for d in proc_dir.iterdir() if d.is_dir()]

            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
            for ds in data_sources:
                imgs_dir = settings.PROCESSED_DIR / processor_name / ds / 'imgs'
                if not imgs_dir.exists():
                    # kf 图片直接在 data source 目录下，尝试回退
                    imgs_dir = settings.PROCESSED_DIR / processor_name / ds
                for f in imgs_dir.iterdir() if imgs_dir.exists() else []:
                    if f.is_file() and f.suffix.lower() in image_extensions:
                        try:
                            total_bytes += f.stat().st_size
                            image_count += 1
                        except OSError:
                            pass

        logger.info(
            "[BATCH_INFO] processor=%s records=%d images=%d est_bytes=%d",
            processor_name, record_count, image_count, total_bytes,
        )
        return {
            "total_bytes": total_bytes,
            "record_count": record_count,
            "image_count": image_count,
        }
    except Exception as exc:
        logger.error("[BATCH_INFO_ERROR]: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"查询导出信息失败: {exc}")


@router.post("/{processor_name}/batch")
async def batch_export(
    processor_name: str,
    request: BatchExportRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    start_time = time.time()

    try:
        all_records = _load_export_records(processor_name, request.data_sources, db)
        if not all_records:
            raise HTTPException(status_code=404, detail="未找到可导出的数据")

        exporter = StructuredExportService(processor_name=processor_name)
        results = exporter.batch_export(all_records, request.formats, request.include_images)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Build ordered entry list: JSON files first, then images
        entries: list[tuple[str, bytes | Path]] = []

        for fmt in request.formats:
            if fmt in results:
                json_bytes = json.dumps(
                    results[fmt], ensure_ascii=False, indent=2
                ).encode("utf-8")
                entries.append((f"{fmt}_ALL_{timestamp}.json", json_bytes))

        if request.include_images and "image_files" in results:
            for zip_path, local_path in results["image_files"]:
                p = Path(local_path)
                if p.exists():
                    entries.append((zip_path, p))
                else:
                    logger.warning("Skip missing image: %s", local_path)

        logger.info(
            "[BATCH_EXPORT] formats=%s records=%d images=%d prep=%.2fs",
            request.formats,
            len(all_records),
            sum(1 for _, s in entries if isinstance(s, Path)),
            time.time() - start_time,
        )

        zip_filename = f"corpus_export_{processor_name}_{timestamp}.zip"
        return StreamingResponse(
            _iter_streaming_zip(entries),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{zip_filename}",
                "X-Export-Records": str(len(all_records)),
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("[BATCH_EXPORT_ERROR]: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"批量导出失败: {exc}")
