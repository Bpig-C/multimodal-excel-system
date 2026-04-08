"""
标签管理API
提供实体类型、关系类型、标签定义生成、审核、导入导出、版本管理等功能
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.schemas import SuccessResponse, ErrorResponse
from models.db_models import Dataset
from services.label_management_service import LabelManagementService
from services.dynamic_prompt_builder import DynamicPromptBuilder
from services.label_config_cache import LabelConfigCache
from agents.label_definition_generator import LabelDefinitionGenerator

router = APIRouter(prefix="/api/v1/labels", tags=["labels"])


# ============================================================================
# 实体类型管理API
# ============================================================================

@router.get("/entities")
async def list_entity_types(
    include_inactive: bool = Query(False, description="是否包含不活跃的类型"),
    include_unreviewed: bool = Query(True, description="是否包含未审核的类型"),
    db: Session = Depends(get_db)
):
    """获取实体类型列表"""
    try:
        service = LabelManagementService(db)
        entity_types = service.list_entity_types(
            include_inactive=include_inactive,
            include_unreviewed=include_unreviewed
        )
        
        return {
            "success": True,
            "message": "获取实体类型列表成功",
            "data": {
                "items": [
                    {
                        "id": et.id,
                        "type_name": et.type_name,
                        "type_name_zh": et.type_name_zh,
                        "color": et.color,
                        "description": et.description,
                        "definition": et.definition,
                        "examples": et.examples,
                        "disambiguation": et.disambiguation,
                        "supports_bbox": et.supports_bbox,
                        "is_active": et.is_active,
                        "is_reviewed": et.is_reviewed,
                        "reviewed_by": et.reviewed_by,
                        "reviewed_at": et.reviewed_at.isoformat() if et.reviewed_at else None,
                        "created_at": et.created_at.isoformat(),
                        "updated_at": et.updated_at.isoformat() if et.updated_at else None
                    }
                    for et in entity_types
                ],
                "total": len(entity_types)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取实体类型列表失败: {str(e)}")


@router.post("/entities")
async def create_entity_type(
    type_name: str = Body(..., description="类型名称(英文)"),
    type_name_zh: str = Body(..., description="类型名称(中文)"),
    color: str = Body(..., description="颜色代码"),
    description: Optional[str] = Body(None, description="描述"),
    supports_bbox: bool = Body(False, description="是否支持边界框"),
    db: Session = Depends(get_db)
):
    """创建实体类型"""
    try:
        service = LabelManagementService(db)
        entity_type = service.create_entity_type(
            type_name=type_name,
            type_name_zh=type_name_zh,
            color=color,
            description=description,
            supports_bbox=supports_bbox
        )
        
        return {
            "success": True,
            "message": "实体类型创建成功",
            "data": {
                "id": entity_type.id,
                "type_name": entity_type.type_name,
                "type_name_zh": entity_type.type_name_zh,
                "color": entity_type.color,
                "is_reviewed": entity_type.is_reviewed
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建实体类型失败: {str(e)}")


@router.put("/entities/{entity_type_id}")
async def update_entity_type(
    entity_type_id: int,
    type_name: Optional[str] = Body(None),
    type_name_zh: Optional[str] = Body(None),
    color: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    supports_bbox: Optional[bool] = Body(None),
    db: Session = Depends(get_db)
):
    """更新实体类型"""
    try:
        service = LabelManagementService(db)
        
        # 构建更新字段
        update_data = {}
        if type_name is not None:
            update_data['type_name'] = type_name
        if type_name_zh is not None:
            update_data['type_name_zh'] = type_name_zh
        if color is not None:
            update_data['color'] = color
        if description is not None:
            update_data['description'] = description
        if supports_bbox is not None:
            update_data['supports_bbox'] = supports_bbox
        
        entity_type = service.update_entity_type(entity_type_id, **update_data)
        
        if not entity_type:
            raise HTTPException(status_code=404, detail="实体类型不存在")
        
        return {
            "success": True,
            "message": "实体类型更新成功",
            "data": {
                "id": entity_type.id,
                "type_name": entity_type.type_name,
                "type_name_zh": entity_type.type_name_zh
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新实体类型失败: {str(e)}")


@router.delete("/entities/{entity_type_id}")
async def delete_entity_type(
    entity_type_id: int,
    db: Session = Depends(get_db)
):
    """删除实体类型(软删除)"""
    try:
        service = LabelManagementService(db)
        success = service.delete_entity_type(entity_type_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="实体类型不存在")
        
        return {
            "success": True,
            "message": "实体类型删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除实体类型失败: {str(e)}")


@router.post("/entities/{entity_type_id}/generate-definition")
async def generate_entity_definition(
    entity_type_id: int,
    db: Session = Depends(get_db)
):
    """生成实体类型定义(调用LLM)"""
    try:
        service = LabelManagementService(db)
        entity_type = service.get_entity_type(entity_type_id)
        
        if not entity_type:
            raise HTTPException(status_code=404, detail="实体类型不存在")
        
        # 调用LLM生成定义
        generator = LabelDefinitionGenerator()
        result = generator.generate_entity_definition(
            type_name=entity_type.type_name,
            type_name_zh=entity_type.type_name_zh,
            description=entity_type.description or ""
        )
        
        # 更新实体类型
        entity_type = service.update_entity_type(
            entity_type_id,
            definition=result.definition,
            examples=result.examples,
            disambiguation=result.disambiguation
        )
        
        return {
            "success": True,
            "message": "定义生成成功",
            "data": {
                "definition": result.definition,
                "examples": result.examples,
                "disambiguation": result.disambiguation
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成定义失败: {str(e)}")


@router.post("/entities/{entity_type_id}/review")
async def review_entity_type(
    entity_type_id: int,
    reviewed_by: int = Body(..., description="审核人ID"),
    definition: Optional[str] = Body(None, description="定义(可编辑)"),
    examples: Optional[List[str]] = Body(None, description="示例列表(可编辑)"),
    disambiguation: Optional[str] = Body(None, description="类别辨析(可编辑)"),
    db: Session = Depends(get_db)
):
    """审核实体类型定义"""
    try:
        service = LabelManagementService(db)
        entity_type = service.review_entity_type(
            entity_type_id=entity_type_id,
            reviewed_by=reviewed_by,
            definition=definition,
            examples=examples,
            disambiguation=disambiguation
        )
        
        if not entity_type:
            raise HTTPException(status_code=404, detail="实体类型不存在")
        
        return {
            "success": True,
            "message": "审核完成",
            "data": {
                "id": entity_type.id,
                "is_reviewed": entity_type.is_reviewed,
                "reviewed_by": entity_type.reviewed_by,
                "reviewed_at": entity_type.reviewed_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"审核失败: {str(e)}")


# ============================================================================
# 关系类型管理API
# ============================================================================

@router.get("/relations")
async def list_relation_types(
    include_inactive: bool = Query(False, description="是否包含不活跃的类型"),
    include_unreviewed: bool = Query(True, description="是否包含未审核的类型"),
    db: Session = Depends(get_db)
):
    """获取关系类型列表"""
    try:
        service = LabelManagementService(db)
        relation_types = service.list_relation_types(
            include_inactive=include_inactive,
            include_unreviewed=include_unreviewed
        )
        
        return {
            "success": True,
            "message": "获取关系类型列表成功",
            "data": {
                "items": [
                    {
                        "id": rt.id,
                        "type_name": rt.type_name,
                        "type_name_zh": rt.type_name_zh,
                        "color": rt.color,
                        "description": rt.description,
                        "definition": rt.definition,
                        "direction_rule": rt.direction_rule,
                        "examples": rt.examples,
                        "disambiguation": rt.disambiguation,
                        "is_active": rt.is_active,
                        "is_reviewed": rt.is_reviewed,
                        "reviewed_by": rt.reviewed_by,
                        "reviewed_at": rt.reviewed_at.isoformat() if rt.reviewed_at else None,
                        "created_at": rt.created_at.isoformat(),
                        "updated_at": rt.updated_at.isoformat() if rt.updated_at else None
                    }
                    for rt in relation_types
                ],
                "total": len(relation_types)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取关系类型列表失败: {str(e)}")


@router.post("/relations")
async def create_relation_type(
    type_name: str = Body(..., description="类型名称(英文)"),
    type_name_zh: str = Body(..., description="类型名称(中文)"),
    color: str = Body(..., description="颜色代码"),
    description: Optional[str] = Body(None, description="描述"),
    db: Session = Depends(get_db)
):
    """创建关系类型"""
    try:
        service = LabelManagementService(db)
        relation_type = service.create_relation_type(
            type_name=type_name,
            type_name_zh=type_name_zh,
            color=color,
            description=description
        )
        
        return {
            "success": True,
            "message": "关系类型创建成功",
            "data": {
                "id": relation_type.id,
                "type_name": relation_type.type_name,
                "type_name_zh": relation_type.type_name_zh,
                "color": relation_type.color,
                "is_reviewed": relation_type.is_reviewed
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建关系类型失败: {str(e)}")


@router.put("/relations/{relation_type_id}")
async def update_relation_type(
    relation_type_id: int,
    type_name: Optional[str] = Body(None),
    type_name_zh: Optional[str] = Body(None),
    color: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """更新关系类型"""
    try:
        service = LabelManagementService(db)
        
        # 构建更新字段
        update_data = {}
        if type_name is not None:
            update_data['type_name'] = type_name
        if type_name_zh is not None:
            update_data['type_name_zh'] = type_name_zh
        if color is not None:
            update_data['color'] = color
        if description is not None:
            update_data['description'] = description
        
        relation_type = service.update_relation_type(relation_type_id, **update_data)
        
        if not relation_type:
            raise HTTPException(status_code=404, detail="关系类型不存在")
        
        return {
            "success": True,
            "message": "关系类型更新成功",
            "data": {
                "id": relation_type.id,
                "type_name": relation_type.type_name,
                "type_name_zh": relation_type.type_name_zh
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新关系类型失败: {str(e)}")


@router.delete("/relations/{relation_type_id}")
async def delete_relation_type(
    relation_type_id: int,
    db: Session = Depends(get_db)
):
    """删除关系类型(软删除)"""
    try:
        service = LabelManagementService(db)
        success = service.delete_relation_type(relation_type_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="关系类型不存在")
        
        return {
            "success": True,
            "message": "关系类型删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除关系类型失败: {str(e)}")


@router.post("/relations/{relation_type_id}/generate-definition")
async def generate_relation_definition(
    relation_type_id: int,
    db: Session = Depends(get_db)
):
    """生成关系类型定义(调用LLM)"""
    try:
        service = LabelManagementService(db)
        relation_type = service.get_relation_type(relation_type_id)
        
        if not relation_type:
            raise HTTPException(status_code=404, detail="关系类型不存在")
        
        # 调用LLM生成定义
        generator = LabelDefinitionGenerator()
        result = generator.generate_relation_definition(
            type_name=relation_type.type_name,
            type_name_zh=relation_type.type_name_zh,
            description=relation_type.description or ""
        )
        
        # 更新关系类型
        relation_type = service.update_relation_type(
            relation_type_id,
            definition=result.definition,
            direction_rule=result.direction_rule,
            examples=result.examples,
            disambiguation=result.disambiguation
        )
        
        return {
            "success": True,
            "message": "定义生成成功",
            "data": {
                "definition": result.definition,
                "direction_rule": result.direction_rule,
                "examples": result.examples,
                "disambiguation": result.disambiguation
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成定义失败: {str(e)}")


@router.post("/relations/{relation_type_id}/review")
async def review_relation_type(
    relation_type_id: int,
    reviewed_by: int = Body(..., description="审核人ID"),
    definition: Optional[str] = Body(None, description="定义(可编辑)"),
    direction_rule: Optional[str] = Body(None, description="方向规则(可编辑)"),
    examples: Optional[List[str]] = Body(None, description="示例列表(可编辑)"),
    disambiguation: Optional[str] = Body(None, description="类别辨析(可编辑)"),
    db: Session = Depends(get_db)
):
    """审核关系类型定义"""
    try:
        service = LabelManagementService(db)
        relation_type = service.review_relation_type(
            relation_type_id=relation_type_id,
            reviewed_by=reviewed_by,
            definition=definition,
            direction_rule=direction_rule,
            examples=examples,
            disambiguation=disambiguation
        )
        
        if not relation_type:
            raise HTTPException(status_code=404, detail="关系类型不存在")
        
        return {
            "success": True,
            "message": "审核完成",
            "data": {
                "id": relation_type.id,
                "is_reviewed": relation_type.is_reviewed,
                "reviewed_by": relation_type.reviewed_by,
                "reviewed_at": relation_type.reviewed_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"审核失败: {str(e)}")


# ============================================================================
# 导入导出API
# ============================================================================

@router.post("/import")
async def import_label_schema(
    schema_data: dict = Body(..., description="标签配置JSON"),
    merge: bool = Body(False, description="是否合并(True=合并, False=替换)"),
    db: Session = Depends(get_db)
):
    """导入标签配置"""
    try:
        service = LabelManagementService(db)
        stats = service.import_label_schema(schema_data, merge=merge)
        
        return {
            "success": True,
            "message": "导入成功",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")


@router.get("/export")
async def export_label_schema(
    db: Session = Depends(get_db)
):
    """导出标签配置"""
    try:
        service = LabelManagementService(db)
        schema_data = service.export_label_schema()
        
        return {
            "success": True,
            "message": "导出成功",
            "data": schema_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.get("/prompt-preview")
async def preview_prompt(
    prompt_type: str = Query("entity", description="Prompt类型: entity或relation"),
    db: Session = Depends(get_db)
):
    """预览Agent Prompt"""
    try:
        # 获取标签配置
        entity_types = LabelConfigCache.get_entity_types(db)
        relation_types = LabelConfigCache.get_relation_types(db)
        
        # 构建Prompt预览
        preview = DynamicPromptBuilder.build_prompt_preview(entity_types, relation_types)
        
        if prompt_type == "entity":
            prompt_text = f"""你是一个专业的品质失效案例实体抽取专家。

## 实体类型定义

{preview['entity_types_section']}

## 标注原则
1. 实体边界清晰
2. 避免重叠
3. 保留原文
4. 偏移量准确
5. 类型准确
"""
        else:
            prompt_text = f"""你是一个专业的品质失效案例关系抽取专家。

## 关系类型定义

{preview['relation_types_section']}

## 标注原则
1. 方向准确
2. 实体有效
3. 关系合理
4. 避免冗余
5. 类型准确
"""
        
        return {
            "success": True,
            "message": "获取Prompt预览成功",
            "data": {
                "prompt": prompt_text,
                "entity_count": preview['entity_count'],
                "entity_reviewed_count": preview['entity_reviewed_count'],
                "entity_pending_count": preview['entity_pending_count'],
                "relation_count": preview['relation_count'],
                "relation_reviewed_count": preview['relation_reviewed_count'],
                "relation_pending_count": preview['relation_pending_count'],
                "total_reviewed": preview['total_reviewed'],
                "total_pending": preview['total_pending']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取Prompt预览失败: {str(e)}")


# ============================================================================
# 版本管理API
# ============================================================================

@router.get("/versions")
async def list_versions(
    db: Session = Depends(get_db)
):
    """获取版本列表"""
    try:
        service = LabelManagementService(db)
        versions = service.list_versions()
        
        # 统计每个版本使用的数据集数量，并解析schema_data获取实体和关系类型
        import json
        version_data = []
        for version in versions:
            datasets_count = db.query(func.count(Dataset.id))\
                .filter(Dataset.label_schema_version_id == version.id)\
                .scalar() or 0
            
            # 解析schema_data获取实体和关系类型
            schema_data = json.loads(version.schema_data)
            
            version_data.append({
                "id": version.id,
                "version_id": version.version_id,
                "version_name": version.version_name,
                "description": version.description,
                "is_active": version.is_active,
                "datasets_count": datasets_count,
                "entity_types": schema_data.get('entity_types', []),
                "relation_types": schema_data.get('relation_types', []),
                "created_by": version.created_by,
                "created_at": version.created_at.isoformat()
            })
        
        return {
            "success": True,
            "message": "获取版本列表成功",
            "data": {
                "items": version_data,
                "total": len(version_data)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取版本列表失败: {str(e)}")


@router.post("/versions/snapshot")
async def create_version_snapshot(
    version_name: str = Body(..., description="版本名称"),
    description: Optional[str] = Body(None, description="版本说明"),
    created_by: int = Body(..., description="创建人ID"),
    db: Session = Depends(get_db)
):
    """创建版本快照"""
    try:
        service = LabelManagementService(db)
        version = service.create_version_snapshot(
            version_name=version_name,
            description=description,
            created_by=created_by
        )
        
        # 解析schema_data获取统计信息
        import json
        schema_data = json.loads(version.schema_data)
        
        return {
            "success": True,
            "message": "版本快照创建成功",
            "data": {
                "version_id": version.version_id,
                "version_name": version.version_name,
                "entity_types_count": schema_data['metadata']['total_entity_types'],
                "relation_types_count": schema_data['metadata']['total_relation_types'],
                "created_at": version.created_at.isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建版本快照失败: {str(e)}")


@router.get("/versions/{version_id}")
async def get_version_detail(
    version_id: str,
    db: Session = Depends(get_db)
):
    """获取版本详情"""
    try:
        service = LabelManagementService(db)
        version = service.get_version(version_id)
        
        if not version:
            raise HTTPException(status_code=404, detail="版本不存在")
        
        # 解析schema_data
        import json
        schema_data = json.loads(version.schema_data)
        
        # 获取使用该版本的数据集列表
        from models.db_models import Dataset
        datasets = db.query(Dataset)\
            .filter(Dataset.label_schema_version_id == version.id)\
            .all()
        
        return {
            "success": True,
            "message": "获取版本详情成功",
            "data": {
                "version_id": version.version_id,
                "version_name": version.version_name,
                "description": version.description,
                "is_active": version.is_active,
                "entity_types": schema_data['entity_types'],
                "relation_types": schema_data['relation_types'],
                "datasets": [
                    {
                        "dataset_id": ds.dataset_id,
                        "name": ds.name
                    }
                    for ds in datasets
                ],
                "created_at": version.created_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取版本详情失败: {str(e)}")


@router.post("/versions/{version_id}/activate")
async def activate_version(
    version_id: str,
    db: Session = Depends(get_db)
):
    """激活版本"""
    try:
        service = LabelManagementService(db)
        version = service.activate_version(version_id)
        
        if not version:
            raise HTTPException(status_code=404, detail="版本不存在")
        
        return {
            "success": True,
            "message": f"已切换到版本: {version.version_name}",
            "data": {
                "version_id": version.version_id,
                "is_active": version.is_active
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"激活版本失败: {str(e)}")


@router.get("/versions/compare")
async def compare_versions(
    from_version: str = Query(..., description="源版本ID"),
    to_version: str = Query(..., description="目标版本ID"),
    db: Session = Depends(get_db)
):
    """比较版本差异"""
    try:
        service = LabelManagementService(db)
        
        # 获取两个版本
        from_ver = service.get_version(from_version)
        to_ver = service.get_version(to_version)
        
        if not from_ver or not to_ver:
            raise HTTPException(status_code=404, detail="版本不存在")
        
        # 解析schema_data
        import json
        from_schema = json.loads(from_ver.schema_data)
        to_schema = json.loads(to_ver.schema_data)
        
        # 比较实体类型
        from_entities = {et['type_name']: et for et in from_schema['entity_types']}
        to_entities = {et['type_name']: et for et in to_schema['entity_types']}
        
        entity_changes = {
            'added': [et for name, et in to_entities.items() if name not in from_entities],
            'removed': [et for name, et in from_entities.items() if name not in to_entities],
            'modified': []
        }
        
        # 检查修改的实体类型
        for name in set(from_entities.keys()) & set(to_entities.keys()):
            if from_entities[name] != to_entities[name]:
                changes = []
                for key in ['definition', 'examples', 'disambiguation', 'description']:
                    if from_entities[name].get(key) != to_entities[name].get(key):
                        changes.append(key)
                if changes:
                    entity_changes['modified'].append({
                        'type_name': name,
                        'changes': changes
                    })
        
        # 比较关系类型(类似逻辑)
        from_relations = {rt['type_name']: rt for rt in from_schema['relation_types']}
        to_relations = {rt['type_name']: rt for rt in to_schema['relation_types']}
        
        relation_changes = {
            'added': [rt for name, rt in to_relations.items() if name not in from_relations],
            'removed': [rt for name, rt in from_relations.items() if name not in to_relations],
            'modified': []
        }
        
        for name in set(from_relations.keys()) & set(to_relations.keys()):
            if from_relations[name] != to_relations[name]:
                changes = []
                for key in ['definition', 'direction_rule', 'examples', 'disambiguation', 'description']:
                    if from_relations[name].get(key) != to_relations[name].get(key):
                        changes.append(key)
                if changes:
                    relation_changes['modified'].append({
                        'type_name': name,
                        'changes': changes
                    })
        
        return {
            "success": True,
            "message": "版本比较成功",
            "data": {
                "from_version": from_version,
                "to_version": to_version,
                "changes": {
                    "entity_types": entity_changes,
                    "relation_types": relation_changes
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"版本比较失败: {str(e)}")
