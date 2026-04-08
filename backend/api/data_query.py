"""数据查询 API - KF/QMS/品质案例列表与统计。"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.users import get_current_user
from database import get_db
from services.query_engine import QueryEngine

router = APIRouter(prefix="/api/v1/data", tags=["data"])


@router.get("/list")
async def get_data_list(
    processor_name: str = Query("kf", description="处理器名称(kf/qms/failure_case)"),
    page: Optional[int] = Query(None, description="页码(从1开始)", ge=1),
    page_size: Optional[int] = Query(None, description="每页数量", ge=1, le=500),
    limit: int = Query(100, description="兼容参数: 返回数量限制", ge=1, le=500),
    offset: int = Query(0, description="兼容参数: 偏移量", ge=0),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取 KF/QMS/品质失效案例数据列表（支持分页）。"""
    try:
        engine = QueryEngine(processor_name=processor_name)

        if page is not None or page_size is not None:
            resolved_page_size = page_size or limit
            resolved_page = page or (offset // resolved_page_size + 1)
            resolved_offset = (resolved_page - 1) * resolved_page_size
        else:
            resolved_page_size = limit
            resolved_offset = offset
            resolved_page = (resolved_offset // resolved_page_size) + 1

        data = engine.get_data_list(db, processor_name, resolved_page_size, resolved_offset)
        total_count = engine.get_data_total_count(db, processor_name)

        return {
            "success": True,
            "data": data,
            "count": len(data),
            "total_count": total_count,
            "page": resolved_page,
            "page_size": resolved_page_size,
            "processor": processor_name,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/statistics")
async def get_statistics(
    processor_name: str = Query("kf", description="处理器名称(kf/qms/failure_case)"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取统计分析数据。"""
    try:
        engine = QueryEngine(processor_name=processor_name)
        stats = engine.get_statistics(db)

        return {
            "success": True,
            "data": stats,
            "processor": processor_name,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计失败: {str(e)}")
