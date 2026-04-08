"""
数据集管理API
提供数据集的CRUD操作和导出功能
"""
from collections import Counter
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import (
    DatasetCreateRequest,
    DatasetUpdateRequest,
    DatasetResponse,
    DatasetListResponse,
    DatasetStatisticsResponse,
    DatasetExportRequest,
    SuccessResponse,
    ErrorResponse
)
from services.dataset_service import DatasetService
from api.users import get_current_user

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])


class AddTasksRequest(BaseModel):
    """向数据集添加语料的请求体"""
    corpus_ids: List[int]


@router.post("", response_model=DatasetResponse)
async def create_dataset(
    request: DatasetCreateRequest,
    db: Session = Depends(get_db)
):
    """
    创建数据集
    
    - 创建数据集记录
    - 关联语料
    - 自动创建标注任务
    - 绑定标签体系版本
    """
    try:
        service = DatasetService(db)
        dataset = service.create_dataset(
            name=request.name,
            description=request.description,
            corpus_ids=request.corpus_ids,
            created_by=request.created_by,
            label_schema_version_id=request.label_schema_version_id
        )
        
        return DatasetResponse(
            success=True,
            message="数据集创建成功",
            data={
                "id": dataset.id,
                "dataset_id": dataset.dataset_id,
                "name": dataset.name,
                "description": dataset.description,
                "label_schema_version_id": dataset.label_schema_version_id,
                "created_by": dataset.created_by,
                "created_at": dataset.created_at.isoformat(),
                "updated_at": dataset.updated_at.isoformat()
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建数据集失败: {str(e)}")


@router.get("", response_model=DatasetListResponse)
async def list_datasets(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="数据集名称筛选"),
    created_by: Optional[int] = Query(None, description="创建人ID筛选"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取数据集列表
    
    权限：
    - 管理员：查看所有数据集
    - 标注员/复核员：只能查看分配给自己的数据集（应使用 /datasets/my 接口）
    - 浏览员：查看所有数据集（只读）
    
    - 支持分页
    - 支持按名称筛选
    - 支持按创建人筛选
    """
    try:
        user_role = current_user['role']
        user_id = current_user['user_id']
        
        # 标注员和复核员应该使用 /datasets/my 接口
        if user_role in ['annotator', 'reviewer']:
            return DatasetListResponse(
                success=True,
                message="标注员和复核员请使用 GET /datasets/my 接口查看分配给您的数据集",
                data={
                    "items": [],
                    "total": 0,
                    "page": page,
                    "page_size": page_size
                }
            )
        
        # 管理员和浏览员可以查看所有数据集
        service = DatasetService(db)
        datasets, total = service.list_datasets(
            page=page,
            page_size=page_size,
            name=name,
            created_by=created_by
        )
        
        # 构建响应数据
        items = []
        for dataset in datasets:
            # 内联计算统计信息（复用已加载的 annotation_tasks 关系）
            status_counts = Counter(task.status for task in dataset.annotation_tasks)
            total_tasks = len(dataset.annotation_tasks)
            statistics = {
                "total_tasks": total_tasks,
                "completed_tasks": (
                    status_counts.get('completed', 0)
                    + status_counts.get('completed_with_errors', 0)
                ),
                "reviewed_tasks": status_counts.get('reviewed', 0),
                "pending_tasks": status_counts.get('pending', 0),
                "processing_tasks": status_counts.get('processing', 0),
                "failed_tasks": status_counts.get('failed', 0),
            }
            items.append({
                "id": dataset.id,
                "dataset_id": dataset.dataset_id,
                "name": dataset.name,
                "description": dataset.description,
                "label_schema_version_id": dataset.label_schema_version_id,
                "created_by": dataset.created_by,
                "created_at": dataset.created_at.isoformat(),
                "updated_at": dataset.updated_at.isoformat(),
                "corpus_count": len(dataset.corpus_associations),
                "task_count": total_tasks,
                "statistics": statistics
            })
        
        return DatasetListResponse(
            success=True,
            message="获取数据集列表成功",
            data={
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据集列表失败: {str(e)}")


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    """
    获取数据集详情
    
    - 返回数据集基本信息
    - 返回关联的语料列表
    - 返回标注任务列表
    """
    try:
        service = DatasetService(db)
        dataset = service.get_dataset(dataset_id)
        
        if not dataset:
            raise HTTPException(status_code=404, detail="数据集不存在")
        
        # 构建语料列表
        corpus_list = []
        for assoc in dataset.corpus_associations:
            corpus = assoc.corpus
            corpus_list.append({
                "id": corpus.id,
                "text_id": corpus.text_id,
                "text": corpus.text,
                "text_type": corpus.text_type,
                "has_images": corpus.has_images
            })
        
        # 构建任务列表
        task_list = []
        for task in dataset.annotation_tasks:
            task_list.append({
                "id": task.id,
                "task_id": task.task_id,
                "corpus_id": task.corpus_id,
                "status": task.status,
                "annotation_type": task.annotation_type,
                "current_version": task.current_version
            })

        # 内联计算统计信息
        status_counts = Counter(task.status for task in dataset.annotation_tasks)
        total_tasks = len(dataset.annotation_tasks)
        statistics = {
            "total_tasks": total_tasks,
            "completed_tasks": (
                status_counts.get('completed', 0)
                + status_counts.get('completed_with_errors', 0)
            ),
            "reviewed_tasks": status_counts.get('reviewed', 0),
            "pending_tasks": status_counts.get('pending', 0),
            "processing_tasks": status_counts.get('processing', 0),
            "failed_tasks": status_counts.get('failed', 0),
        }

        return DatasetResponse(
            success=True,
            message="获取数据集详情成功",
            data={
                "id": dataset.id,
                "dataset_id": dataset.dataset_id,
                "name": dataset.name,
                "description": dataset.description,
                "label_schema_version_id": dataset.label_schema_version_id,
                "created_by": dataset.created_by,
                "created_at": dataset.created_at.isoformat(),
                "updated_at": dataset.updated_at.isoformat(),
                "corpus_list": corpus_list,
                "task_list": task_list,
                "statistics": statistics
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据集详情失败: {str(e)}")


@router.put("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(
    dataset_id: str,
    request: DatasetUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    更新数据集
    
    - 更新数据集名称和描述
    """
    try:
        service = DatasetService(db)
        dataset = service.get_dataset(dataset_id)
        
        if not dataset:
            raise HTTPException(status_code=404, detail="数据集不存在")
        
        # 更新字段
        if request.name is not None:
            dataset.name = request.name
        if request.description is not None:
            dataset.description = request.description
        
        db.commit()
        db.refresh(dataset)
        
        return DatasetResponse(
            success=True,
            message="数据集更新成功",
            data={
                "id": dataset.id,
                "dataset_id": dataset.dataset_id,
                "name": dataset.name,
                "description": dataset.description,
                "label_schema_version_id": dataset.label_schema_version_id,
                "created_by": dataset.created_by,
                "created_at": dataset.created_at.isoformat(),
                "updated_at": dataset.updated_at.isoformat()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新数据集失败: {str(e)}")


@router.delete("/{dataset_id}", response_model=SuccessResponse)
async def delete_dataset(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    """
    删除数据集
    
    - 级联删除所有关联数据
    - 删除标注任务
    - 删除实体和关系
    """
    try:
        service = DatasetService(db)
        success = service.delete_dataset(dataset_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="数据集不存在")
        
        return SuccessResponse(
            success=True,
            message="数据集删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除数据集失败: {str(e)}")


@router.get("/{dataset_id}/statistics", response_model=DatasetStatisticsResponse)
async def get_dataset_statistics(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    """
    获取数据集统计信息
    
    - 任务数量统计
    - 完成率统计
    - 实体和关系数量统计
    """
    try:
        service = DatasetService(db)
        stats = service.get_dataset_statistics(dataset_id)
        
        if not stats:
            raise HTTPException(status_code=404, detail="数据集不存在")
        
        return DatasetStatisticsResponse(
            success=True,
            message="获取统计信息成功",
            data=stats
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


@router.get("/{dataset_id}/tasks")
async def get_dataset_tasks(
    dataset_id: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取数据集的标注任务列表
    
    权限：
    - 管理员：返回该数据集的所有任务
    - 标注员：返回该数据集中分配给该标注员的任务
    - 浏览员：返回该数据集中状态为已完成的任务
    
    - 支持分页
    - 支持按状态筛选
    - 返回任务详情包括语料文本、实体数、关系数等
    """
    try:
        from models.db_models import Dataset, AnnotationTask, Corpus
        from services.task_query_service import TaskQueryService
        
        # 验证数据集是否存在
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="数据集不存在")
        
        # 获取当前用户信息
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        # 使用 TaskQueryService 进行权限过滤
        task_query_service = TaskQueryService(db)
        
        # 获取用户可访问的任务列表（传入数据集ID进行筛选）
        tasks, total = task_query_service.get_user_tasks(
            user_id=user_id,
            user_role=user_role,
            dataset_id=dataset.id,
            status=status,
            page=page,
            page_size=page_size,
            sort_by="status_priority",
            sort_order="asc"
        )
        
        # 构建响应数据
        items = []
        for task in tasks:
            # 获取语料文本
            corpus = db.query(Corpus).filter(Corpus.id == task.corpus_id).first()
            corpus_text = corpus.text if corpus else ""
            
            items.append({
                "id": task.id,
                "task_id": task.task_id,
                "corpus_id": task.corpus_id,
                "corpus_text": corpus_text,
                "status": task.status,
                "annotation_type": task.annotation_type,
                "entity_count": len([e for e in task.text_entities if e.version == task.current_version]),
                "relation_count": len([r for r in task.relations if r.version == task.current_version]),
                "current_version": task.current_version,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
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
        raise HTTPException(status_code=500, detail=f"获取任务列表失败: {str(e)}")


@router.post("/{dataset_id}/tasks", response_model=SuccessResponse)
async def add_tasks_to_dataset(
    dataset_id: str,
    request: AddTasksRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    向已有数据集添加语料（自动创建标注任务，重复添加自动跳过）
    
    - 检测重复语料（已在数据集中的跳过）
    - 自动为新增语料创建 pending 状态的标注任务
    """
    try:
        service = DatasetService(db)
        result = service.add_tasks_to_dataset(dataset_id, request.corpus_ids)
        return SuccessResponse(
            success=True,
            message=f"添加完成：新增 {result['added']} 条，跳过重复 {result['skipped']} 条",
            data=result
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加语料失败: {str(e)}")


@router.delete("/{dataset_id}/tasks/{task_id}", response_model=SuccessResponse)
async def remove_task_from_dataset(
    dataset_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    从数据集中删除一个标注任务及其关联语料绑定和全部标注数据
    """
    try:
        service = DatasetService(db)
        success = service.remove_task(dataset_id, task_id)
        if not success:
            raise HTTPException(status_code=404, detail="任务不存在或不属于该数据集")
        return SuccessResponse(
            success=True,
            message="任务删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")


@router.post("/{dataset_id}/export")
async def export_dataset(
    dataset_id: str,
    request: Optional[DatasetExportRequest] = Body(default=None),
    db: Session = Depends(get_db)
):
    """
    导出数据集
    
    - 导出为JSONL格式
    - 支持按状态筛选
    - 返回导出文件路径
    """
    try:
        service = DatasetService(db)
        # 默认只导出已完成和已复核的任务
        status_filter = None
        if request and request.status_filter:
            status_filter = request.status_filter
        else:
            status_filter = ["completed", "reviewed"]
        export_path = service.export_dataset(
            dataset_id=dataset_id,
            output_path=request.output_path if request else None,
            status_filter=status_filter
        )

        if not export_path:
            raise HTTPException(status_code=404, detail="数据集不存在或无数据可导出")

        # 确保路径存在并返回文件以触发浏览器下载（带 Content-Disposition: attachment）
        import os
        from pathlib import Path

        file_path = Path(export_path)
        if not file_path.exists():
            # 有时候 service 返回相对路径，从项目根尝试解析
            file_path = Path(os.getcwd()) / export_path
            if not file_path.exists():
                raise HTTPException(status_code=500, detail=f"导出文件未找到: {export_path}")

        return FileResponse(
            path=str(file_path),
            media_type='application/octet-stream',
            filename=file_path.name
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出数据集失败: {str(e)}")
