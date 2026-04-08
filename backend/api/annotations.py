"""
标注任务API
提供批量自动标注、标注任务管理、实体和关系的CRUD操作
"""
import asyncio
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body, Query
from sqlalchemy.orm import Session

from database import get_db, SessionLocal
from models.db_models import AnnotationTask, TextEntity, Relation, Corpus, Dataset
from services.batch_annotation_service import BatchAnnotationService
from services.task_query_service import TaskQueryService
from services.label_config_cache import LabelConfigCache
from services.dynamic_prompt_builder import DynamicPromptBuilder
from api.users import get_current_user

router = APIRouter(prefix="/api/v1/annotations", tags=["annotations"])


def _run_batch_annotation_job(
    job_id: str,
    user_id: Optional[int],
    user_role: str,
    task_ids: Optional[List[str]] = None
):
    """后台执行批量标注（使用独立数据库会话，避免请求会话关闭后失效）"""
    db = SessionLocal()
    try:
        service = BatchAnnotationService(db)
        service.execute_batch_annotation(job_id, user_id, user_role, task_ids=task_ids)
    finally:
        db.close()


# ============================================================================
# 跨数据集任务列表API
# ============================================================================

@router.get("")
async def get_annotations(
    dataset_id: Optional[int] = Query(None, description="数据集ID筛选"),
    status: Optional[str] = Query(None, description="状态筛选 (pending/processing/completed/failed)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    sort_by: str = Query("created_at", description="排序字段 (created_at/updated_at/status)"),
    sort_order: str = Query("desc", description="排序方向 (asc/desc)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取跨数据集任务列表
    
    根据用户角色返回相应的任务：
    - 管理员：返回所有任务（可选按数据集筛选）
    - 标注员：返回分配给该用户的任务（基于 DatasetAssignment）
    - 浏览员：返回403错误（浏览员不使用此端点）
    
    Args:
        dataset_id: 数据集ID筛选（可选）
        status: 状态筛选（可选）
        page: 页码
        page_size: 每页数量
        sort_by: 排序字段
        sort_order: 排序方向
        db: 数据库会话
        current_user: 当前用户
    
    Returns:
        任务列表响应
    """
    try:
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')
        
        # 浏览员不能使用此端点
        if user_role == 'viewer':
            raise HTTPException(
                status_code=403,
                detail="浏览员无权访问任务列表，请通过数据集页面查看已完成的标注结果"
            )
        
        # 创建任务查询服务
        task_service = TaskQueryService(db)
        
        # 获取任务列表
        tasks, total = task_service.get_user_tasks(
            user_id=user_id,
            user_role=user_role,
            dataset_id=dataset_id,
            status=status,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # 构建响应数据
        items = []
        for task in tasks:
            # 获取数据集信息
            dataset = db.query(Dataset).filter(Dataset.id == task.dataset_id).first()
            dataset_name = dataset.name if dataset else "未知数据集"
            
            # 获取语料信息
            corpus = db.query(Corpus).filter(Corpus.id == task.corpus_id).first()
            corpus_text = corpus.text[:100] if corpus and corpus.text else ""
            
            # 统计实体和关系数量
            entity_count = db.query(TextEntity).filter(
                TextEntity.task_id == task.id,
                TextEntity.version == task.current_version
            ).count()
            
            relation_count = db.query(Relation).filter(
                Relation.task_id == task.id,
                Relation.version == task.current_version
            ).count()
            
            items.append({
                "id": task.id,
                "task_id": task.task_id,
                "dataset_id": dataset.dataset_id if dataset else None,
                "dataset_name": dataset_name,
                "corpus_id": task.corpus_id,
                "corpus_text": corpus_text,
                "status": task.status,
                "annotation_type": task.annotation_type,
                "entity_count": entity_count,
                "relation_count": relation_count,
                "current_version": task.current_version,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            })
        
        return {
            "success": True,
            "message": "获取任务列表成功",
            "data": {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取任务列表失败: {str(e)}"
        )


# ============================================================================
# 批量标注API
# ============================================================================

@router.post("/batch")
async def trigger_batch_annotation(
    dataset_id: str = Body(..., description="数据集ID"),
    task_ids: Optional[List[str]] = Body(None, description="指定要标注的任务ID列表（可选）"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    触发批量自动标注
    
    创建批量任务并在后台异步执行
    
    权限要求：
    - 管理员：可以批量标注任何数据集的任务
    - 标注员：只能批量标注分配给自己的任务
    - 浏览员：无权限
    
    参数：
    - dataset_id: 数据集ID（必填）
    - task_ids: 指定要标注的任务ID列表（可选）
      - 如果提供，只标注指定的任务
      - 如果不提供，标注所有符合权限的pending任务
    """
    user_id = current_user['user_id']
    user_role = current_user['role']
    
    # 1. 检查角色权限
    if user_role == 'viewer':
        raise HTTPException(
            status_code=403,
            detail="浏览员没有批量标注权限"
        )
    
    # 2. 检查数据集访问权限（标注员）
    if user_role == 'annotator':
        # 查询数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="数据集不存在")
        
        # 检查是否有分配
        from models.db_models import DatasetAssignment
        assignment = db.query(DatasetAssignment).filter(
            DatasetAssignment.dataset_id == dataset.id,
            DatasetAssignment.user_id == user_id,
            DatasetAssignment.role == 'annotator',
            DatasetAssignment.is_active == True
        ).first()
        
        if not assignment:
            raise HTTPException(
                status_code=403,
                detail="您没有权限访问该数据集"
            )
    
    try:
        service = BatchAnnotationService(db)
        
        # 创建批量任务（传递用户信息和任务ID列表）
        batch_job = service.create_batch_job(
            dataset_id=dataset_id,
            created_by=user_id,
            user_role=user_role,
            task_ids=task_ids
        )
        
        # 在后台执行批量标注（独立会话，避免阻塞主请求和会话生命周期问题）
        background_tasks.add_task(
            _run_batch_annotation_job,
            batch_job.job_id,
            user_id,
            user_role,
            task_ids
        )
        
        return {
            "success": True,
            "message": "批量标注任务已创建",
            "data": {
                "job_id": batch_job.job_id,
                "dataset_id": dataset_id,
                "total_tasks": batch_job.total_tasks,
                "status": batch_job.status
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建批量任务失败: {str(e)}")


@router.get("/batch/{job_id}")
async def get_batch_job_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    """获取批量任务状态和进度"""
    try:
        service = BatchAnnotationService(db)
        stats = service.get_batch_job_statistics(job_id)
        
        if not stats:
            raise HTTPException(status_code=404, detail="批量任务不存在")
        
        return {
            "success": True,
            "message": "获取批量任务状态成功",
            "data": stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取批量任务状态失败: {str(e)}")


@router.post("/batch/{job_id}/cancel")
async def cancel_batch_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    """取消批量任务"""
    try:
        service = BatchAnnotationService(db)
        success = service.cancel_batch_job(job_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="无法取消该任务")
        
        return {
            "success": True,
            "message": "批量任务已取消"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消批量任务失败: {str(e)}")


# ============================================================================
# 标注任务管理API
# ============================================================================

@router.get("/{task_id}")
async def get_annotation_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取标注任务详情
    
    权限规则：
    - 管理员：允许访问所有任务
    - 标注员：只允许访问分配的任务
    - 浏览员：只允许访问已完成任务
    """
    try:
        # 查询任务
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 权限检查
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')
        
        task_service = TaskQueryService(db)
        has_permission = task_service.check_task_permission(
            user_id=user_id,
            user_role=user_role,
            task_id=task.id
        )
        
        if not has_permission:
            if user_role == 'viewer':
                raise HTTPException(
                    status_code=403,
                    detail="浏览员只能访问已完成的任务"
                )
            elif user_role == 'annotator':
                raise HTTPException(
                    status_code=403,
                    detail="该任务未分配给您"
                )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="无权访问该任务"
                )
        
        # 查询语料
        corpus = db.query(Corpus).filter(Corpus.id == task.corpus_id).first()
        
        # 查询实体
        entities = db.query(TextEntity)\
            .filter(TextEntity.task_id == task.id)\
            .filter(TextEntity.version == task.current_version)\
            .all()
        
        # 查询关系
        relations = db.query(Relation)\
            .filter(Relation.task_id == task.id)\
            .filter(Relation.version == task.current_version)\
            .all()
        
        return {
            "success": True,
            "message": "获取标注任务详情成功",
            "data": {
                "task_id": task.task_id,
                "dataset_id": task.dataset.dataset_id if task.dataset else None,
                "corpus": {
                    "text_id": corpus.text_id,
                    "text": corpus.text,
                    "text_type": corpus.text_type,
                    "has_images": corpus.has_images
                } if corpus else None,
                "status": task.status,
                "annotation_type": task.annotation_type,
                "current_version": task.current_version,
                "entities": [
                    {
                        "id": e.id,
                        "entity_id": e.entity_id,
                        "token": e.token,
                        "label": e.label,
                        "start_offset": e.start_offset,
                        "end_offset": e.end_offset,
                        "confidence": e.confidence
                    }
                    for e in entities
                ],
                "relations": [
                    {
                        "id": r.id,
                        "relation_id": r.relation_id,
                        "from_entity_id": r.from_entity_id,
                        "to_entity_id": r.to_entity_id,
                        "relation_type": r.relation_type
                    }
                    for r in relations
                ],
                "error_message": task.error_message,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取标注任务详情失败: {str(e)}")


@router.get("/{task_id}/prompts")
async def get_task_prompts(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取任务运行时使用的实体/关系Prompt文本（用于版本核对）"""
    try:
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")

        user_id = current_user.get('user_id')
        user_role = current_user.get('role')

        task_service = TaskQueryService(db)
        has_permission = task_service.check_task_permission(
            user_id=user_id,
            user_role=user_role,
            task_id=task.id
        )

        if not has_permission:
            if user_role == 'viewer':
                raise HTTPException(status_code=403, detail="浏览员只能访问已完成的任务")
            if user_role == 'annotator':
                raise HTTPException(status_code=403, detail="该任务未分配给您")
            raise HTTPException(status_code=403, detail="无权访问该任务")

        corpus = db.query(Corpus).filter(Corpus.id == task.corpus_id).first()
        if not corpus:
            raise HTTPException(status_code=404, detail="任务对应语料不存在")

        entity_types = LabelConfigCache.get_entity_types(db)
        relation_types = LabelConfigCache.get_relation_types(db)

        entity_prompt = DynamicPromptBuilder.build_entity_extraction_prompt(
            text_id=corpus.text_id,
            text=corpus.text,
            entity_types=entity_types
        )

        existing_entities = db.query(TextEntity)\
            .filter(TextEntity.task_id == task.id)\
            .filter(TextEntity.version == task.current_version)\
            .all()

        entities_for_relation = [
            {
                "id": idx,
                "token": entity.token,
                "label": entity.label
            }
            for idx, entity in enumerate(existing_entities)
        ]

        relation_prompt = DynamicPromptBuilder.build_relation_extraction_prompt(
            text_id=corpus.text_id,
            text=corpus.text,
            entities=entities_for_relation,
            relation_types=relation_types
        )

        return {
            "success": True,
            "message": "获取任务Prompt成功",
            "data": {
                "task_id": task.task_id,
                "text_id": corpus.text_id,
                "entity_prompt": entity_prompt,
                "relation_prompt": relation_prompt,
                "entity_type_count": len(entity_types),
                "relation_type_count": len(relation_types),
                "entity_count_for_relation_prompt": len(entities_for_relation)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务Prompt失败: {str(e)}")


@router.put("/{task_id}")
async def update_annotation_task(
    task_id: str,
    request_body: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    更新标注任务
    
    权限规则：
    - 管理员：允许编辑所有任务
    - 标注员：只允许编辑分配的任务
    - 浏览员：禁止编辑（返回403）
    """
    try:
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 权限检查
        user_id = current_user.get('user_id')
        user_role = current_user.get('role')
        
        # 浏览员禁止编辑
        if user_role == 'viewer':
            raise HTTPException(
                status_code=403,
                detail="浏览员无权编辑任务"
            )
        
        # 标注员和管理员需要检查权限
        task_service = TaskQueryService(db)
        has_permission = task_service.check_task_permission(
            user_id=user_id,
            user_role=user_role,
            task_id=task.id
        )
        
        if not has_permission:
            if user_role == 'annotator':
                raise HTTPException(
                    status_code=403,
                    detail="该任务未分配给您"
                )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="无权编辑该任务"
                )
        
        # 更新状态
        status = request_body.get('status')
        if status:
            task.status = status
        
        db.commit()
        db.refresh(task)
        
        return {
            "success": True,
            "message": "标注任务更新成功",
            "data": {
                "task_id": task.task_id,
                "status": task.status
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新标注任务失败: {str(e)}")


# ============================================================================
# 实体管理API
# ============================================================================

@router.post("/{task_id}/entities")
async def add_entity(
    task_id: str,
    request_body: dict = Body(...),
    db: Session = Depends(get_db)
):
    """添加文本实体"""
    try:
        import uuid
        
        # 从请求体中提取参数
        token = request_body.get('token')
        label = request_body.get('label')
        start_offset = request_body.get('start_offset')
        end_offset = request_body.get('end_offset')
        
        if not all([token, label, start_offset is not None, end_offset is not None]):
            raise HTTPException(status_code=400, detail="缺少必需参数")
        
        # 查询任务
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 创建实体
        entity = TextEntity(
            task_id=task.id,
            entity_id=f"entity-{uuid.uuid4().hex[:8]}",
            token=token,
            label=label,
            start_offset=start_offset,
            end_offset=end_offset,
            version=task.current_version
        )
        
        db.add(entity)
        
        # 更新任务为手动标注
        if task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        db.refresh(entity)
        
        return {
            "success": True,
            "message": "实体添加成功",
            "data": {
                "id": entity.id,
                "entity_id": entity.entity_id,
                "token": entity.token,
                "label": entity.label,
                "start_offset": entity.start_offset,
                "end_offset": entity.end_offset
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加实体失败: {str(e)}")


@router.put("/{task_id}/entities/{entity_id}")
async def update_entity(
    task_id: str,
    entity_id: int,
    request_body: dict = Body(...),
    db: Session = Depends(get_db)
):
    """更新文本实体"""
    try:
        # 从请求体中提取参数
        token = request_body.get('token')
        label = request_body.get('label')
        start_offset = request_body.get('start_offset')
        end_offset = request_body.get('end_offset')
        
        # 查询任务
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 查询实体
        entity = db.query(TextEntity)\
            .filter(TextEntity.id == entity_id)\
            .filter(TextEntity.task_id == task.id)\
            .first()
        
        if not entity:
            raise HTTPException(status_code=404, detail="实体不存在")
        
        # 更新字段
        if token is not None:
            entity.token = token
        if label is not None:
            entity.label = label
        if start_offset is not None:
            entity.start_offset = start_offset
        if end_offset is not None:
            entity.end_offset = end_offset
        
        # 更新任务为手动标注
        if task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        db.refresh(entity)
        
        return {
            "success": True,
            "message": "实体更新成功",
            "data": {
                "id": entity.id,
                "entity_id": entity.entity_id,
                "token": entity.token,
                "label": entity.label,
                "start_offset": entity.start_offset,
                "end_offset": entity.end_offset
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新实体失败: {str(e)}")


@router.delete("/{task_id}/entities/{entity_id}")
async def delete_entity(
    task_id: str,
    entity_id: int,
    db: Session = Depends(get_db)
):
    """删除文本实体"""
    try:
        # 查询任务
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 查询实体
        entity = db.query(TextEntity)\
            .filter(TextEntity.id == entity_id)\
            .filter(TextEntity.task_id == task.id)\
            .first()
        
        if not entity:
            raise HTTPException(status_code=404, detail="实体不存在")
        
        # 删除关联的关系
        db.query(Relation)\
            .filter(
                (Relation.from_entity_id == entity.entity_id) |
                (Relation.to_entity_id == entity.entity_id)
            )\
            .filter(Relation.task_id == task.id)\
            .delete()
        
        # 删除实体
        db.delete(entity)
        
        # 更新任务为手动标注
        if task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        
        return {
            "success": True,
            "message": "实体删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除实体失败: {str(e)}")


# ============================================================================
# 关系管理API
# ============================================================================

@router.post("/{task_id}/relations")
async def add_relation(
    task_id: str,
    request_body: dict = Body(...),
    db: Session = Depends(get_db)
):
    """添加关系"""
    try:
        import uuid
        
        # 从请求体中提取参数
        from_entity_id = request_body.get('from_entity_id')
        to_entity_id = request_body.get('to_entity_id')
        relation_type = request_body.get('relation_type', 'relates_to')
        
        if not from_entity_id or not to_entity_id:
            raise HTTPException(status_code=400, detail="缺少必需参数: from_entity_id 或 to_entity_id")
        
        # 查询任务
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 验证实体存在
        from_entity = db.query(TextEntity)\
            .filter(TextEntity.entity_id == from_entity_id)\
            .filter(TextEntity.task_id == task.id)\
            .first()
        
        to_entity = db.query(TextEntity)\
            .filter(TextEntity.entity_id == to_entity_id)\
            .filter(TextEntity.task_id == task.id)\
            .first()
        
        if not from_entity or not to_entity:
            raise HTTPException(status_code=400, detail="源实体或目标实体不存在")
        
        # 创建关系
        relation = Relation(
            task_id=task.id,
            relation_id=f"relation-{uuid.uuid4().hex[:8]}",
            from_entity_id=from_entity_id,
            to_entity_id=to_entity_id,
            relation_type=relation_type,
            version=task.current_version
        )
        
        db.add(relation)
        
        # 更新任务为手动标注
        if task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        db.refresh(relation)
        
        return {
            "success": True,
            "message": "关系添加成功",
            "data": {
                "id": relation.id,
                "relation_id": relation.relation_id,
                "from_entity_id": relation.from_entity_id,
                "to_entity_id": relation.to_entity_id,
                "relation_type": relation.relation_type
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加关系失败: {str(e)}")


@router.put("/{task_id}/relations/{relation_id}")
async def update_relation(
    task_id: str,
    relation_id: int,
    request_body: dict = Body(...),
    db: Session = Depends(get_db)
):
    """更新关系"""
    try:
        # 从请求体中提取参数
        from_entity_id = request_body.get('from_entity_id')
        to_entity_id = request_body.get('to_entity_id')
        relation_type = request_body.get('relation_type')
        
        # 查询任务
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 查询关系
        relation = db.query(Relation)\
            .filter(Relation.id == relation_id)\
            .filter(Relation.task_id == task.id)\
            .first()
        
        if not relation:
            raise HTTPException(status_code=404, detail="关系不存在")
        
        # 更新字段
        if from_entity_id is not None:
            # 验证实体存在
            entity = db.query(TextEntity)\
                .filter(TextEntity.entity_id == from_entity_id)\
                .filter(TextEntity.task_id == task.id)\
                .first()
            if not entity:
                raise HTTPException(status_code=400, detail="源实体不存在")
            relation.from_entity_id = from_entity_id
        
        if to_entity_id is not None:
            # 验证实体存在
            entity = db.query(TextEntity)\
                .filter(TextEntity.entity_id == to_entity_id)\
                .filter(TextEntity.task_id == task.id)\
                .first()
            if not entity:
                raise HTTPException(status_code=400, detail="目标实体不存在")
            relation.to_entity_id = to_entity_id
        
        if relation_type is not None:
            relation.relation_type = relation_type
        
        # 更新任务为手动标注
        if task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        db.refresh(relation)
        
        return {
            "success": True,
            "message": "关系更新成功",
            "data": {
                "id": relation.id,
                "relation_id": relation.relation_id,
                "from_entity_id": relation.from_entity_id,
                "to_entity_id": relation.to_entity_id,
                "relation_type": relation.relation_type
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新关系失败: {str(e)}")


@router.delete("/{task_id}/relations/{relation_id}")
async def delete_relation(
    task_id: str,
    relation_id: int,
    db: Session = Depends(get_db)
):
    """删除关系"""
    try:
        # 查询任务
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 查询关系
        relation = db.query(Relation)\
            .filter(Relation.id == relation_id)\
            .filter(Relation.task_id == task.id)\
            .first()
        
        if not relation:
            raise HTTPException(status_code=404, detail="关系不存在")
        
        # 删除关系
        db.delete(relation)
        
        # 更新任务为手动标注
        if task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        
        return {
            "success": True,
            "message": "关系删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除关系失败: {str(e)}")
