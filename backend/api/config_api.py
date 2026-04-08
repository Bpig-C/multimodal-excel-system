"""处理器配置API - 提供处理器列表和前端配置"""
from fastapi import APIRouter, HTTPException, Depends

from api.users import get_current_user
from processors import list_processors, get_processor

router = APIRouter(prefix="/api/v1/config", tags=["config"])


@router.get("/processors")
async def get_processors(current_user: dict = Depends(get_current_user)):
    """获取所有可用的处理器列表"""
    return {"processors": list_processors()}


@router.get("/processors/{name}/graph-config")
async def get_graph_config(
    name: str,
    current_user: dict = Depends(get_current_user)
):
    """获取指定处理器的图谱可视化配置"""
    try:
        processor = get_processor(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    config = processor.get_graph_config()
    return {
        "processor": name,
        "display_name": processor.display_name,
        "node_types": config.node_types,
        "edge_labels": config.edge_labels,
    }


@router.get("/processors/{name}/field-mapping")
async def get_field_mapping(
    name: str,
    current_user: dict = Depends(get_current_user)
):
    """获取指定处理器的字段映射配置"""
    try:
        processor = get_processor(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "processor": name,
        "display_name": processor.display_name,
        "field_mapping": processor.field_mapping,
    }
