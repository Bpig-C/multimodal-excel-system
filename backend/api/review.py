"""
复核API
提供复核任务的REST API接口
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from services.review_service import ReviewService
from models.schemas import (
    ReviewTaskResponse, ReviewActionRequest, SuccessResponse
)
from models.db_models import ReviewTask, AnnotationTask
from api.users import get_current_user  # 添加导入


router = APIRouter(prefix="/api/v1/review", tags=["review"])


@router.post("/submit/{task_id}", response_model=ReviewTaskResponse)
def submit_for_review(
    task_id: str,
    request_body: dict = Body(default={}),
    db: Session = Depends(get_db)
):
    """
    提交标注任务进行复核
    
    Args:
        task_id: 标注任务ID
        request_body: 请求体，可包含reviewer_id
    
    Returns:
        ReviewTaskResponse: 创建的复核任务
    """
    reviewer_id = request_body.get('reviewer_id') if request_body else None
    
    # 查询标注任务
    task = db.query(AnnotationTask).filter(
        AnnotationTask.task_id == task_id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"标注任务不存在: {task_id}")
    
    # 创建复核服务
    service = ReviewService(db)
    
    try:
        review = service.submit_for_review(task.id, reviewer_id)
        
        return ReviewTaskResponse(
            review_id=review.review_id,
            task_id=task.task_id,
            status=review.status,
            reviewer_id=review.reviewer_id,
            review_comment=review.review_comment,
            reviewed_at=review.reviewed_at,
            created_at=review.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks", response_model=List[ReviewTaskResponse])
def get_review_tasks(
    status: Optional[str] = Query(None, description="复核状态筛选"),
    reviewer_id: Optional[int] = Query(None, description="复核人员ID筛选"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取复核任务列表
    
    权限：管理员和标注员可以访问
    - 管理员：可以看到所有复核任务
    - 标注员：只能看到他人标注的任务的复核
    
    Args:
        status: 复核状态筛选（pending/approved/rejected）
        reviewer_id: 复核人员ID筛选
        skip: 跳过记录数
        limit: 返回记录数
        current_user: 当前用户信息
    
    Returns:
        List[ReviewTaskResponse]: 复核任务列表
    """
    # 检查权限：只有管理员和标注员可以访问
    if current_user.get('role') not in ['admin', 'annotator']:
        raise HTTPException(
            status_code=403,
            detail="权限不足，只有管理员和标注员可以访问复核功能"
        )
    
    service = ReviewService(db)
    
    try:
        reviews, total = service.get_review_tasks(
            status=status,
            reviewer_id=reviewer_id,
            skip=skip,
            limit=limit
        )
        
        # 构建响应
        result = []
        for review in reviews:
            # 查询关联的标注任务
            task = db.query(AnnotationTask).filter(
                AnnotationTask.id == review.task_id
            ).first()
            
            # 如果是标注员，过滤掉自己标注的任务
            if current_user.get('role') == 'annotator':
                user_id = current_user.get('user_id')
                if task and task.assigned_to == user_id:
                    continue  # 跳过自己标注的任务
            
            result.append(ReviewTaskResponse(
                review_id=review.review_id,
                task_id=task.task_id if task else "",
                status=review.status,
                reviewer_id=review.reviewer_id,
                review_comment=review.review_comment,
                reviewed_at=review.reviewed_at,
                created_at=review.created_at
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{review_id}")
def get_review_detail(
    review_id: str,
    db: Session = Depends(get_db)
):
    """
    获取复核任务详情
    
    Args:
        review_id: 复核任务ID
    
    Returns:
        Dict: 复核任务详情，包含完整的标注数据
    """
    service = ReviewService(db)
    
    detail = service.get_review_task_detail(review_id)
    
    if not detail:
        raise HTTPException(status_code=404, detail=f"复核任务不存在: {review_id}")
    
    return detail


@router.post("/{review_id}/approve", response_model=ReviewTaskResponse)
def approve_review(
    review_id: str,
    request: ReviewActionRequest,
    db: Session = Depends(get_db)
):
    """
    批准复核任务
    
    Args:
        review_id: 复核任务ID
        request: 复核操作请求（包含复核意见和复核人员ID）
    
    Returns:
        ReviewTaskResponse: 更新后的复核任务
    """
    # 从请求体中获取 reviewer_id，默认为 1
    reviewer_id = getattr(request, 'reviewer_id', 1)
    
    service = ReviewService(db)
    
    try:
        review = service.approve_task(
            review_id=review_id,
            reviewer_id=reviewer_id,
            comment=request.review_comment
        )
        
        # 查询关联的标注任务
        task = db.query(AnnotationTask).filter(
            AnnotationTask.id == review.task_id
        ).first()
        
        return ReviewTaskResponse(
            review_id=review.review_id,
            task_id=task.task_id if task else "",
            status=review.status,
            reviewer_id=review.reviewer_id,
            review_comment=review.review_comment,
            reviewed_at=review.reviewed_at,
            created_at=review.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{review_id}/reject", response_model=ReviewTaskResponse)
def reject_review(
    review_id: str,
    request: ReviewActionRequest,
    db: Session = Depends(get_db)
):
    """
    驳回复核任务
    
    Args:
        review_id: 复核任务ID
        request: 复核操作请求（必须包含驳回原因和复核人员ID）
    
    Returns:
        ReviewTaskResponse: 更新后的复核任务
    """
    if not request.review_comment:
        raise HTTPException(status_code=400, detail="驳回任务时必须填写驳回原因")
    
    # 从请求体中获取 reviewer_id，默认为 1
    reviewer_id = getattr(request, 'reviewer_id', 1)
    
    service = ReviewService(db)
    
    try:
        review = service.reject_task(
            review_id=review_id,
            reviewer_id=reviewer_id,
            comment=request.review_comment
        )
        
        # 查询关联的标注任务
        task = db.query(AnnotationTask).filter(
            AnnotationTask.id == review.task_id
        ).first()
        
        return ReviewTaskResponse(
            review_id=review.review_id,
            task_id=task.task_id if task else "",
            status=review.status,
            reviewer_id=review.reviewer_id,
            review_comment=review.review_comment,
            reviewed_at=review.reviewed_at,
            created_at=review.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/dataset/{dataset_id}/statistics")
def get_dataset_statistics(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    获取数据集的质量统计
    
    Args:
        dataset_id: 数据集ID
    
    Returns:
        Dict: 质量统计指标
    """
    service = ReviewService(db)
    
    try:
        stats = service.calculate_quality_statistics(dataset_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dataset/{dataset_id}/summary")
def get_dataset_review_summary(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """
    获取数据集的复核摘要
    
    Args:
        dataset_id: 数据集ID
    
    Returns:
        Dict: 复核摘要信息
    """
    service = ReviewService(db)
    
    try:
        summary = service.get_dataset_review_summary(dataset_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
