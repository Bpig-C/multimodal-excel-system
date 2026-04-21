"""
数据集分配API
提供数据集级别的任务分配功能
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from services.dataset_assignment_service import DatasetAssignmentService
from models.schemas import (
    AssignmentRequest,
    AutoAssignmentRequest,
    BatchAssignmentRequest,
    TransferAssignmentRequest,
    AssignmentResponse,
    AutoAssignmentResponse,
    AssignmentListResponse,
    MyDatasetsResponse,
    TransferAssignmentResponse,
    SuccessResponse
)
from models.db_models import Dataset, User, DatasetAssignment
from api.users import get_current_user, require_admin

router = APIRouter(prefix="/api/v1/datasets", tags=["dataset-assignment"])


# ============================================================================
# 辅助函数
# ============================================================================

def get_assignment_service(db: Session = Depends(get_db)) -> DatasetAssignmentService:
    """获取数据集分配服务实例"""
    return DatasetAssignmentService(db)


def format_task_range(start: Optional[int], end: Optional[int]) -> str:
    """格式化任务范围"""
    if start is None or end is None:
        return "全部"
    return f"{start}-{end}"


def get_assignment_info(assignment, db: Session):
    """构建分配信息"""
    # 获取用户信息
    user = db.query(User).filter(User.id == assignment.user_id).first()
    
    # 获取数据集信息
    dataset = db.query(Dataset).filter(Dataset.id == assignment.dataset_id).first()
    
    # 统计任务进度
    service = DatasetAssignmentService(db)
    tasks = service._get_tasks_in_range(
        assignment.dataset_id,
        assignment.task_start_index,
        assignment.task_end_index
    )
    
    completed_count = sum(1 for t in tasks if t.status == 'completed')
    in_review_count = sum(1 for t in tasks if t.status == 'in_review')
    
    # 获取转移目标用户信息
    transferred_to_username = None
    if assignment.transferred_to:
        transferred_user = db.query(User).filter(User.id == assignment.transferred_to).first()
        if transferred_user:
            transferred_to_username = transferred_user.username
    
    return {
        "assignment_id": assignment.id,
        "dataset_id": dataset.dataset_id if dataset else "",
        "user_id": assignment.user_id,
        "username": user.username if user else "未知",
        "role": assignment.role,
        "task_range": format_task_range(assignment.task_start_index, assignment.task_end_index),
        "task_count": len(tasks),
        "completed_count": completed_count,
        "in_review_count": in_review_count,
        "is_active": assignment.is_active,
        "transferred_to": assignment.transferred_to,
        "transferred_to_username": transferred_to_username,
        "transferred_at": assignment.transferred_at,
        "transfer_reason": assignment.transfer_reason,
        "assigned_by": assignment.assigned_by,
        "assigned_at": assignment.assigned_at
    }



# ============================================================================
# API端点
# ============================================================================

@router.post("/{dataset_id}/assign", response_model=AssignmentResponse)
async def assign_dataset(
    dataset_id: str,
    request: AssignmentRequest,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    分配数据集（整体或范围）
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        request: 分配请求
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        AssignmentResponse: 分配响应
    """
    try:
        # 获取数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail=f"数据集不存在: {dataset_id}")
        
        # 根据模式执行分配
        if request.mode == "full":
            assignment = service.assign_full(
                dataset_id=dataset.id,
                user_id=request.user_id,
                role=request.role.value,
                assigned_by=admin['user_id']
            )
        elif request.mode == "range":
            if request.start_index is None or request.end_index is None:
                raise HTTPException(
                    status_code=400,
                    detail="范围模式下必须指定 start_index 和 end_index"
                )
            
            assignment = service.assign_range(
                dataset_id=dataset.id,
                user_id=request.user_id,
                role=request.role.value,
                start_index=request.start_index,
                end_index=request.end_index,
                assigned_by=admin['user_id']
            )
        else:
            raise HTTPException(status_code=400, detail=f"不支持的分配模式: {request.mode}")
        
        # 构建响应
        assignment_info = get_assignment_info(assignment, db)
        
        return AssignmentResponse(
            success=True,
            message="分配成功",
            data=assignment_info
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分配失败: {str(e)}")


@router.post("/{dataset_id}/assign/auto", response_model=AutoAssignmentResponse)
async def auto_assign_dataset(
    dataset_id: str,
    request: AutoAssignmentRequest,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    自动平均分配数据集
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        request: 自动分配请求
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        AutoAssignmentResponse: 自动分配响应
    """
    try:
        # 获取数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail=f"数据集不存在: {dataset_id}")
        
        # 执行自动分配
        assignments = service.assign_auto(
            dataset_id=dataset.id,
            user_ids=request.user_ids,
            role=request.role.value,
            assigned_by=admin['user_id']
        )
        
        # 构建响应
        assignment_list = []
        total_tasks = 0
        
        for assignment in assignments:
            user = db.query(User).filter(User.id == assignment.user_id).first()
            task_count = service._count_tasks_in_range(
                assignment.dataset_id,
                assignment.task_start_index,
                assignment.task_end_index
            )
            
            assignment_list.append({
                "user_id": assignment.user_id,
                "username": user.username if user else "未知",
                "task_range": format_task_range(assignment.task_start_index, assignment.task_end_index),
                "task_count": task_count
            })
            
            total_tasks += task_count
        
        return AutoAssignmentResponse(
            success=True,
            message="自动分配成功",
            data={
                "assignments": assignment_list,
                "total_tasks": total_tasks
            }
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"自动分配失败: {str(e)}")



@router.delete("/{dataset_id}/assign/{user_id}", response_model=SuccessResponse)
async def cancel_assignment(
    dataset_id: str,
    user_id: int,
    role: str = Query(..., description="角色（annotator/reviewer）"),
    force: bool = Query(False, description="强制取消（跳过检查）"),
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    取消分配（带条件检查）
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        user_id: 用户ID
        role: 角色
        force: 强制取消
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        SuccessResponse: 成功响应
    
    Raises:
        HTTPException: 如果不能取消（有已完成任务）
    """
    try:
        # 获取数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail=f"数据集不存在: {dataset_id}")
        
        # 尝试取消分配
        service.cancel_assignment(
            dataset_id=dataset.id,
            user_id=user_id,
            role=role,
            force=force
        )
        
        return SuccessResponse(
            success=True,
            message="取消分配成功"
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        error_msg = str(e)
        
        # 检查是否是因为有已完成任务而无法取消
        if "|" in error_msg:
            # 解析错误信息和统计数据
            parts = error_msg.split("|")
            reason = parts[0]
            
            # 返回特殊错误，提示使用转移功能
            raise HTTPException(
                status_code=400,
                detail={
                    "message": reason,
                    "action": "transfer",
                    "has_completed": True
                }
            )
        else:
            raise HTTPException(status_code=400, detail=error_msg)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消分配失败: {str(e)}")


@router.post("/{dataset_id}/assignments/batch", response_model=SuccessResponse)
async def batch_assign(
    dataset_id: str,
    request: BatchAssignmentRequest,
    force: bool = Query(False, description="强制分配（跳过已完成任务检查）"),
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    批量分配数据集
    
    权限：仅管理员
    
    用于两阶段分配：前端规划完成后，批量提交所有分配
    
    Args:
        dataset_id: 数据集ID
        request: 批量分配请求
        force: 强制分配（跳过已完成任务检查）
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        SuccessResponse: 成功响应
    """
    try:
        # 获取数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail=f"数据集不存在: {dataset_id}")
        
        # 清空现有分配（使用删除而不是更新，避免唯一约束冲突）
        if request.clear_existing:
            query = db.query(DatasetAssignment)\
                .filter(DatasetAssignment.dataset_id == dataset.id)\
                .filter(DatasetAssignment.is_active == True)
            
            if request.role_filter:
                query = query.filter(DatasetAssignment.role == request.role_filter.value)
            
            existing_assignments = query.all()
            
            # 检查是否有已完成的任务（除非强制）
            if not force and existing_assignments:
                assignments_with_progress = []
                for assignment in existing_assignments:
                    can_cancel, reason, stats = service.can_cancel_assignment(assignment.id)
                    if not can_cancel:
                        assignments_with_progress.append({
                            'username': assignment.user.username if assignment.user else '未知',
                            'role': assignment.role,
                            'completed': stats.get('completed_count', 0),
                            'in_review': stats.get('in_review_count', 0)
                        })
                
                if assignments_with_progress:
                    # 构建详细错误信息
                    details = []
                    for item in assignments_with_progress[:3]:  # 最多显示3个
                        details.append(
                            f"{item['username']}({item['role']}): "
                            f"已完成{item['completed']}个, 复核中{item['in_review']}个"
                        )
                    
                    error_msg = (
                        f"无法清空分配，以下用户已有标注进度：\n" +
                        "\n".join(details)
                    )
                    
                    if len(assignments_with_progress) > 3:
                        error_msg += f"\n...还有 {len(assignments_with_progress) - 3} 个用户"
                    
                    error_msg += "\n\n如需强制清空，请使用转移功能或联系管理员。"
                    
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "message": error_msg,
                            "assignments_with_progress": assignments_with_progress,
                            "can_force": True
                        }
                    )
            
            # 删除分配
            query.delete(synchronize_session=False)
        
        # 批量创建分配
        created_count = 0
        for item in request.assignments:
            # 验证用户存在
            user = db.query(User).filter(User.id == item.user_id).first()
            if not user:
                raise ValueError(f"用户ID {item.user_id} 不存在")
            
            # 创建分配
            assignment = DatasetAssignment(
                dataset_id=dataset.id,
                user_id=item.user_id,
                role=item.role.value,
                task_start_index=item.start_index if item.mode.value == 'range' else None,
                task_end_index=item.end_index if item.mode.value == 'range' else None,
                assigned_by=admin['user_id'],
                is_active=True
            )
            db.add(assignment)
            created_count += 1
        
        db.commit()
        
        return SuccessResponse(
            success=True,
            message=f"批量分配成功，共创建 {created_count} 个分配"
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"批量分配失败: {str(e)}")


@router.delete("/{dataset_id}/assignments/clear", response_model=SuccessResponse)
async def clear_assignments(
    dataset_id: str,
    role: Optional[str] = Query(None, description="角色筛选（annotator/reviewer），不指定则清空所有"),
    force: bool = Query(False, description="强制清空（跳过检查）"),
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    批量清空数据集的所有分配
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        role: 角色筛选（可选）
        force: 强制清空
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        SuccessResponse: 成功响应，包含清空数量
    """
    try:
        print(f"[清空分配] 开始处理: dataset_id={dataset_id}, role={role}, force={force}")
        
        # 获取数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            print(f"[清空分配] 数据集不存在: {dataset_id}")
            raise HTTPException(status_code=404, detail=f"数据集不存在: {dataset_id}")
        
        print(f"[清空分配] 找到数据集: id={dataset.id}, name={dataset.name}")
        
        # 获取要清空的分配
        query = db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset.id)\
            .filter(DatasetAssignment.is_active == True)
        
        if role:
            query = query.filter(DatasetAssignment.role == role)
        
        existing_assignments = query.all()
        count = len(existing_assignments)
        print(f"[清空分配] 找到 {count} 个活跃分配")
        
        if count == 0:
            return SuccessResponse(
                success=True,
                message="没有需要清空的分配"
            )
        
        # 检查是否有已完成的任务（除非强制）
        if not force:
            assignments_with_progress = []
            for assignment in existing_assignments:
                can_cancel, reason, stats = service.can_cancel_assignment(assignment.id)
                if not can_cancel:
                    assignments_with_progress.append({
                        'username': assignment.user.username if assignment.user else '未知',
                        'role': assignment.role,
                        'completed': stats.get('completed_count', 0),
                        'in_review': stats.get('in_review_count', 0)
                    })
            
            if assignments_with_progress:
                # 构建详细错误信息
                details = []
                for item in assignments_with_progress[:3]:  # 最多显示3个
                    details.append(
                        f"{item['username']}({item['role']}): "
                        f"已完成{item['completed']}个, 复核中{item['in_review']}个"
                    )
                
                error_msg = (
                    f"无法清空分配，以下用户已有标注进度：\n" +
                    "\n".join(details)
                )
                
                if len(assignments_with_progress) > 3:
                    error_msg += f"\n...还有 {len(assignments_with_progress) - 3} 个用户"
                
                error_msg += "\n\n如需强制清空，请使用转移功能或联系管理员。"
                
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": error_msg,
                        "assignments_with_progress": assignments_with_progress,
                        "can_force": True
                    }
                )
        
        # 直接删除而不是更新is_active（避免唯一约束冲突）
        query.delete(synchronize_session=False)
        db.commit()
        
        print(f"[清空分配] 成功清空 {count} 个分配")
        
        return SuccessResponse(
            success=True,
            message=f"已清空 {count} 个分配"
        )
    
    except Exception as e:
        import traceback
        print(f"[清空分配] 发生错误:")
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"清空分配失败: {str(e)}")


@router.delete("/{dataset_id}/assign/{user_id}", response_model=SuccessResponse)
async def cancel_assignment(
    dataset_id: str,
    user_id: int,
    role: str = Query(..., description="角色（annotator/reviewer）"),
    force: bool = Query(False, description="强制取消（跳过检查）"),
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    取消分配（带条件检查）
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        user_id: 用户ID
        role: 角色
        force: 强制取消
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        SuccessResponse: 成功响应
    
    Raises:
        HTTPException: 如果不能取消（有已完成任务）
    """
    try:
        # 获取数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail=f"数据集不存在: {dataset_id}")
        
        # 尝试取消分配
        service.cancel_assignment(
            dataset_id=dataset.id,
            user_id=user_id,
            role=role,
            force=force
        )
        
        return SuccessResponse(
            success=True,
            message="取消分配成功"
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        error_msg = str(e)
        
        # 检查是否是因为有已完成任务而无法取消
        if "|" in error_msg:
            # 解析错误信息和统计数据
            parts = error_msg.split("|")
            reason = parts[0]
            
            # 返回特殊错误，提示使用转移功能
            raise HTTPException(
                status_code=400,
                detail={
                    "message": reason,
                    "action": "transfer",
                    "has_completed": True
                }
            )
        else:
            raise HTTPException(status_code=400, detail=error_msg)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消分配失败: {str(e)}")


@router.post("/{dataset_id}/assign/transfer", response_model=TransferAssignmentResponse)
async def transfer_assignment(
    dataset_id: str,
    request: TransferAssignmentRequest,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_admin),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    转移分配
    
    权限：仅管理员
    
    Args:
        dataset_id: 数据集ID
        request: 转移请求
        db: 数据库会话
        admin: 管理员用户
        service: 分配服务
    
    Returns:
        TransferAssignmentResponse: 转移响应
    """
    try:
        # 获取数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail=f"数据集不存在: {dataset_id}")
        
        # 执行转移
        result = service.transfer_assignment(
            dataset_id=dataset.id,
            old_user_id=request.old_user_id,
            new_user_id=request.new_user_id,
            role=request.role.value,
            transfer_mode=request.transfer_mode.value,
            transfer_reason=request.transfer_reason,
            transferred_by=admin['user_id']
        )
        
        return TransferAssignmentResponse(
            success=True,
            message="转移分配成功",
            data=result
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转移分配失败: {str(e)}")



@router.get("/{dataset_id}/assignments", response_model=AssignmentListResponse)
async def get_dataset_assignments(
    dataset_id: str,
    include_inactive: bool = Query(False, description="是否包含不活跃的分配"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    获取数据集分配情况
    
    权限：管理员或已分配用户
    
    Args:
        dataset_id: 数据集ID
        include_inactive: 是否包含不活跃的分配
        db: 数据库会话
        current_user: 当前用户
        service: 分配服务
    
    Returns:
        AssignmentListResponse: 分配列表响应
    """
    try:
        # 获取数据集
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail=f"数据集不存在: {dataset_id}")
        
        # 权限检查：管理员或已分配用户
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        if user_role != 'admin':
            # 检查是否有分配
            has_assignment = service.check_permission(user_id, dataset.id, 'annotator') or \
                           service.check_permission(user_id, dataset.id, 'reviewer')
            
            if not has_assignment:
                raise HTTPException(status_code=403, detail="无权限访问该数据集的分配信息")
        
        # 获取分配列表
        assignments = service.get_dataset_assignments(dataset.id, include_inactive)
        
        # 构建响应
        assignment_list = []
        for assignment in assignments:
            assignment_info = get_assignment_info(assignment, db)
            assignment_list.append(assignment_info)
        
        # 统计信息
        total_tasks = db.query(Dataset).filter(Dataset.id == dataset.id).first()
        task_count = len(total_tasks.annotation_tasks) if total_tasks else 0
        
        assigned_tasks = sum(
            a['task_count'] for a in assignment_list if a['is_active']
        )
        unassigned_count = task_count - assigned_tasks
        
        annotator_count = len([a for a in assignment_list if a['role'] == 'annotator' and a['is_active']])
        reviewer_count = len([a for a in assignment_list if a['role'] == 'reviewer' and a['is_active']])
        
        return AssignmentListResponse(
            success=True,
            message="获取分配列表成功",
            data={
                "dataset_id": dataset.dataset_id,
                "dataset_name": dataset.name,
                "total_tasks": task_count,
                "assignments": assignment_list,
                "unassigned_count": unassigned_count,
                "annotator_count": annotator_count,
                "reviewer_count": reviewer_count
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分配列表失败: {str(e)}")


# 注意：这个路由必须在 /{dataset_id} 之前注册！
@router.get("/my", response_model=MyDatasetsResponse)
async def get_my_datasets(
    role: Optional[str] = Query(None, description="角色筛选（annotator/reviewer）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    service: DatasetAssignmentService = Depends(get_assignment_service)
):
    """
    获取我的数据集
    
    权限：标注员、复核员
    
    Args:
        role: 角色筛选
        page: 页码
        page_size: 每页数量
        db: 数据库会话
        current_user: 当前用户
        service: 分配服务
    
    Returns:
        MyDatasetsResponse: 我的数据集列表响应
    """
    try:
        user_id = current_user['user_id']
        user_role = current_user['role']
        
        # 管理员和浏览员不使用此接口
        if user_role in ['admin', 'viewer']:
            return MyDatasetsResponse(
                success=True,
                message="管理员和浏览员请使用 GET /datasets 接口",
                data={
                    "items": [],
                    "total": 0,
                    "page": page,
                    "page_size": page_size
                }
            )
        
        # 获取用户的数据集
        datasets = service.get_user_datasets(user_id, role)
        
        # 构建响应
        items = []
        for dataset in datasets:
            # 获取用户在该数据集的分配信息
            from models.db_models import DatasetAssignment, AnnotationTask
            
            query = db.query(DatasetAssignment)\
                .filter(DatasetAssignment.dataset_id == dataset.id)\
                .filter(DatasetAssignment.user_id == user_id)\
                .filter(DatasetAssignment.is_active == True)
            
            if role:
                query = query.filter(DatasetAssignment.role == role)
            
            assignment = query.first()
            
            if assignment:
                # 优化：使用SQL COUNT查询而不是加载所有任务
                task_query = db.query(AnnotationTask)\
                    .filter(AnnotationTask.dataset_id == assignment.dataset_id)
                
                # 如果指定了范围，进行过滤
                if assignment.task_start_index is not None and assignment.task_end_index is not None:
                    # 获取所有任务ID，然后按索引切片
                    all_task_ids = [t.id for t in task_query.order_by(AnnotationTask.id).all()]
                    # 索引从1开始，所以需要减1
                    task_ids_in_range = all_task_ids[assignment.task_start_index-1:assignment.task_end_index]
                    
                    # 统计任务数和完成数
                    my_task_count = len(task_ids_in_range)
                    my_completed_count = db.query(AnnotationTask)\
                        .filter(AnnotationTask.id.in_(task_ids_in_range))\
                        .filter(AnnotationTask.status == 'completed')\
                        .count()
                else:
                    # 全部任务
                    my_task_count = task_query.count()
                    my_completed_count = task_query.filter(AnnotationTask.status == 'completed').count()
                
                items.append({
                    "dataset_id": dataset.dataset_id,
                    "name": dataset.name,
                    "description": dataset.description,
                    "my_role": assignment.role,
                    "my_task_range": format_task_range(assignment.task_start_index, assignment.task_end_index),
                    "my_task_count": my_task_count,
                    "my_completed_count": my_completed_count,
                    "total_tasks": len(dataset.annotation_tasks),
                    "assigned_at": assignment.assigned_at
                })
        
        # 分页
        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_items = items[start:end]
        
        return MyDatasetsResponse(
            success=True,
            message="获取我的数据集成功",
            data={
                "items": paginated_items,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取我的数据集失败: {str(e)}")
