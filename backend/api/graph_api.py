"""图谱查询API - 知识图谱数据查询接口（暂不注册）"""
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from api.users import get_current_user
from services.query_engine import QueryEngine

router = APIRouter(prefix="/api/v1/graph", tags=["graph"])


@router.get("/data")
async def get_graph_data(
    customer: Optional[str] = Query(None, description="客户名称"),
    product: Optional[str] = Query(None, description="产品型号"),
    defect: Optional[str] = Query(None, description="缺陷类型"),
    workshop: Optional[str] = Query(None, description="车间（QMS）"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    limit: int = Query(100, description="返回数量限制", ge=1, le=500),
    processor: str = Query('kf', description="处理器名称（kf/qms）"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取知识图谱的节点和边数据"""
    try:
        filters = {}
        if customer:
            filters['customer'] = customer
        if product:
            filters['product'] = product
        if defect:
            filters['defect'] = defect
        if workshop:
            filters['workshop'] = workshop
        if start_date:
            filters['start_date'] = start_date
        if end_date:
            filters['end_date'] = end_date

        engine = QueryEngine(processor_name=processor)
        graph_data = engine.get_graph_data(db, filters if filters else None, limit)

        return {
            "success": True,
            "data": graph_data,
            "filters": filters,
            "node_count": len(graph_data['nodes']),
            "edge_count": len(graph_data['lines'])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/events/{event_id}")
async def get_event_detail(
    event_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取单个快反事件的详细信息"""
    try:
        engine = QueryEngine(processor_name='kf')
        event = engine.get_event_detail(db, event_id)

        if not event:
            raise HTTPException(status_code=404, detail=f"事件不存在: {event_id}")

        return {
            "success": True,
            "data": event
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/statistics")
async def get_statistics(
    processor: str = Query('kf', description="处理器名称（kf/qms）"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取统计数据"""
    try:
        engine = QueryEngine(processor_name=processor)
        stats = engine.get_statistics(db)

        return {
            "success": True,
            "data": stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计失败: {str(e)}")
