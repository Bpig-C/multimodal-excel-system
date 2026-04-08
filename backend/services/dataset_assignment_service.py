"""
数据集分配服务
处理数据集级别的任务分配逻辑
"""
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from models.db_models import (
    Dataset, DatasetAssignment, User, AnnotationTask
)


class DatasetAssignmentService:
    """数据集分配服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def assign_full(
        self,
        dataset_id: int,
        user_id: int,
        role: str,
        assigned_by: int
    ) -> DatasetAssignment:
        """
        整体分配数据集
        
        Args:
            dataset_id: 数据集ID
            user_id: 用户ID
            role: 角色（annotator/reviewer）
            assigned_by: 分配人ID
        
        Returns:
            DatasetAssignment: 分配记录
        """
        # 验证数据集存在
        dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError(f"数据集不存在: {dataset_id}")
        
        # 验证用户存在
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"用户不存在: {user_id}")
        
        # 检查是否已经有活跃分配
        existing = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)\
            .filter(DatasetAssignment.user_id == user_id)\
            .filter(DatasetAssignment.role == role)\
            .filter(DatasetAssignment.is_active == True)\
            .first()
        
        if existing:
            raise ValueError(f"用户 {user.username} 已经被分配为 {role}")
        
        # 检查是否有其他用户的整体分配（同角色）
        existing_full = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)\
            .filter(DatasetAssignment.role == role)\
            .filter(DatasetAssignment.is_active == True)\
            .filter(DatasetAssignment.task_start_index.is_(None))\
            .filter(DatasetAssignment.task_end_index.is_(None))\
            .first()
        
        if existing_full:
            existing_user = self.db.query(User).filter(User.id == existing_full.user_id).first()
            raise ValueError(
                f"该数据集已有用户 {existing_user.username} 的整体分配（{role}），"
                f"请使用范围分配或先取消现有分配"
            )
        
        # 检查是否有任何范围分配（同角色）
        existing_range = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)\
            .filter(DatasetAssignment.role == role)\
            .filter(DatasetAssignment.is_active == True)\
            .filter(DatasetAssignment.task_start_index.isnot(None))\
            .first()
        
        if existing_range:
            raise ValueError(
                f"该数据集已有范围分配（{role}），无法进行整体分配。"
                f"请先取消所有范围分配，或使用范围分配功能"
            )
        
        # 创建分配记录（task_start_index 和 task_end_index 为 NULL 表示全部）
        assignment = DatasetAssignment(
            dataset_id=dataset_id,
            user_id=user_id,
            role=role,
            task_start_index=None,
            task_end_index=None,
            assigned_by=assigned_by,
            is_active=True
        )
        
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        
        return assignment

    
    def assign_range(
        self,
        dataset_id: int,
        user_id: int,
        role: str,
        start_index: int,
        end_index: int,
        assigned_by: int
    ) -> DatasetAssignment:
        """
        范围分配数据集
        
        Args:
            dataset_id: 数据集ID
            user_id: 用户ID
            role: 角色
            start_index: 起始任务索引（从1开始）
            end_index: 结束任务索引（包含）
            assigned_by: 分配人ID
        
        Returns:
            DatasetAssignment: 分配记录
        """
        # 验证范围有效性
        if start_index < 1 or end_index < start_index:
            raise ValueError(f"无效的任务范围: {start_index}-{end_index}")
        
        # 验证数据集存在
        dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError(f"数据集不存在: {dataset_id}")
        
        # 验证用户存在
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"用户不存在: {user_id}")
        
        # 获取数据集任务总数
        total_tasks = self.db.query(AnnotationTask)\
            .filter(AnnotationTask.dataset_id == dataset_id)\
            .count()
        
        if end_index > total_tasks:
            raise ValueError(f"结束索引 {end_index} 超出任务总数 {total_tasks}")
        
        # 检查范围是否重叠
        self._check_range_overlap(dataset_id, role, start_index, end_index)
        
        # 创建分配记录
        assignment = DatasetAssignment(
            dataset_id=dataset_id,
            user_id=user_id,
            role=role,
            task_start_index=start_index,
            task_end_index=end_index,
            assigned_by=assigned_by,
            is_active=True
        )
        
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        
        return assignment
    
    def _check_range_overlap(
        self,
        dataset_id: int,
        role: str,
        start_index: int,
        end_index: int,
        exclude_assignment_id: Optional[int] = None
    ):
        """
        检查任务范围是否与现有分配重叠
        
        Args:
            dataset_id: 数据集ID
            role: 角色
            start_index: 起始索引
            end_index: 结束索引
            exclude_assignment_id: 排除的分配ID（用于更新时）
        
        Raises:
            ValueError: 如果范围重叠
        """
        query = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)\
            .filter(DatasetAssignment.role == role)\
            .filter(DatasetAssignment.is_active == True)
        
        if exclude_assignment_id:
            query = query.filter(DatasetAssignment.id != exclude_assignment_id)
        
        # 查找重叠的分配
        overlapping = query.filter(
            or_(
                # 新范围的起始点在现有范围内
                and_(
                    DatasetAssignment.task_start_index <= start_index,
                    DatasetAssignment.task_end_index >= start_index
                ),
                # 新范围的结束点在现有范围内
                and_(
                    DatasetAssignment.task_start_index <= end_index,
                    DatasetAssignment.task_end_index >= end_index
                ),
                # 新范围包含现有范围
                and_(
                    DatasetAssignment.task_start_index >= start_index,
                    DatasetAssignment.task_end_index <= end_index
                ),
                # 整体分配（NULL范围）
                and_(
                    DatasetAssignment.task_start_index.is_(None),
                    DatasetAssignment.task_end_index.is_(None)
                )
            )
        ).first()
        
        if overlapping:
            user = self.db.query(User).filter(User.id == overlapping.user_id).first()
            if overlapping.task_start_index is None:
                raise ValueError(f"任务范围与用户 {user.username} 的整体分配重叠")
            else:
                raise ValueError(
                    f"任务范围 {start_index}-{end_index} 与用户 {user.username} "
                    f"的分配范围 {overlapping.task_start_index}-{overlapping.task_end_index} 重叠"
                )

    
    def assign_auto(
        self,
        dataset_id: int,
        user_ids: List[int],
        role: str,
        assigned_by: int
    ) -> List[DatasetAssignment]:
        """
        自动平均分配数据集
        
        Args:
            dataset_id: 数据集ID
            user_ids: 用户ID列表
            role: 角色
            assigned_by: 分配人ID
        
        Returns:
            List[DatasetAssignment]: 分配记录列表
        """
        if not user_ids:
            raise ValueError("用户列表不能为空")
        
        # 验证数据集存在
        dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError(f"数据集不存在: {dataset_id}")
        
        # 验证所有用户存在
        users = self.db.query(User).filter(User.id.in_(user_ids)).all()
        if len(users) != len(user_ids):
            raise ValueError("部分用户不存在")
        
        # 获取任务总数
        total_tasks = self.db.query(AnnotationTask)\
            .filter(AnnotationTask.dataset_id == dataset_id)\
            .count()
        
        if total_tasks == 0:
            raise ValueError("数据集没有任务")
        
        # 计算每人分配的任务数
        num_users = len(user_ids)
        tasks_per_user = total_tasks // num_users
        remainder = total_tasks % num_users
        
        # 创建分配记录
        assignments = []
        current_index = 1
        
        for i, user_id in enumerate(user_ids):
            # 前面的用户多分配1个任务（处理余数）
            count = tasks_per_user + (1 if i < remainder else 0)
            end_index = current_index + count - 1
            
            assignment = self.assign_range(
                dataset_id=dataset_id,
                user_id=user_id,
                role=role,
                start_index=current_index,
                end_index=end_index,
                assigned_by=assigned_by
            )
            
            assignments.append(assignment)
            current_index = end_index + 1
        
        return assignments

    
    def can_cancel_assignment(
        self,
        assignment_id: int
    ) -> Tuple[bool, str, Dict[str, int]]:
        """
        检查是否可以取消分配
        
        Args:
            assignment_id: 分配ID
        
        Returns:
            (是否可以取消, 原因说明, 统计信息)
        """
        assignment = self.db.query(DatasetAssignment).filter(
            DatasetAssignment.id == assignment_id
        ).first()
        
        if not assignment:
            raise ValueError(f"分配不存在: {assignment_id}")
        
        # 获取该分配范围内的任务
        tasks = self._get_tasks_in_range(
            assignment.dataset_id,
            assignment.task_start_index,
            assignment.task_end_index
        )
        
        # 统计任务状态
        completed_count = sum(1 for t in tasks if t.status == 'completed')
        in_review_count = sum(1 for t in tasks if t.status == 'in_review')
        processing_count = sum(1 for t in tasks if t.status == 'processing')
        pending_count = sum(1 for t in tasks if t.status == 'pending')
        
        stats = {
            "total_tasks": len(tasks),
            "completed_count": completed_count,
            "in_review_count": in_review_count,
            "processing_count": processing_count,
            "pending_count": pending_count
        }
        
        # 规则1：如果有任务已完成或在复核中，不能直接取消
        if completed_count > 0 or in_review_count > 0:
            return False, "该分配下有已完成或正在复核的任务，请使用转移功能", stats
        
        # 规则2：如果有任务正在处理中，给出警告但允许
        if processing_count > 0:
            return True, f"警告：该分配下有{processing_count}个正在处理的任务", stats
        
        # 规则3：所有任务都是pending，可以安全取消
        return True, "可以安全取消", stats
    
    def cancel_assignment(
        self,
        dataset_id: int,
        user_id: int,
        role: str,
        force: bool = False
    ) -> bool:
        """
        取消分配
        
        Args:
            dataset_id: 数据集ID
            user_id: 用户ID
            role: 角色
            force: 强制取消（跳过检查）
        
        Returns:
            bool: 是否成功
        """
        assignment = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)\
            .filter(DatasetAssignment.user_id == user_id)\
            .filter(DatasetAssignment.role == role)\
            .filter(DatasetAssignment.is_active == True)\
            .first()
        
        if not assignment:
            raise ValueError("分配不存在或已被取消")
        
        # 检查是否可以取消
        if not force:
            can_cancel, reason, stats = self.can_cancel_assignment(assignment.id)
            if not can_cancel:
                # 返回详细信息，让API层决定如何响应
                raise ValueError(f"{reason}|{stats}")
        
        # 删除分配记录
        self.db.delete(assignment)
        self.db.commit()
        
        return True
    
    def _get_tasks_in_range(
        self,
        dataset_id: int,
        start_index: Optional[int],
        end_index: Optional[int]
    ) -> List[AnnotationTask]:
        """
        获取指定范围内的任务
        
        Args:
            dataset_id: 数据集ID
            start_index: 起始索引（None表示从头开始）
            end_index: 结束索引（None表示到末尾）
        
        Returns:
            List[AnnotationTask]: 任务列表
        """
        query = self.db.query(AnnotationTask)\
            .filter(AnnotationTask.dataset_id == dataset_id)\
            .order_by(AnnotationTask.id)
        
        # 如果指定了范围，进行过滤
        if start_index is not None and end_index is not None:
            # 获取所有任务，然后按索引切片
            all_tasks = query.all()
            # 索引从1开始，所以需要减1
            return all_tasks[start_index-1:end_index]
        else:
            # 返回所有任务
            return query.all()

    
    def transfer_assignment(
        self,
        dataset_id: int,
        old_user_id: int,
        new_user_id: int,
        role: str,
        transfer_mode: str = 'all',
        transfer_reason: Optional[str] = None,
        transferred_by: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        转移分配
        
        Args:
            dataset_id: 数据集ID
            old_user_id: 原用户ID
            new_user_id: 新用户ID
            role: 角色
            transfer_mode: 转移模式 ('all', 'remaining', 'completed')
            transfer_reason: 转移原因
            transferred_by: 转移操作人
        
        Returns:
            dict: 转移结果
        """
        # 验证旧分配存在
        old_assignment = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)\
            .filter(DatasetAssignment.user_id == old_user_id)\
            .filter(DatasetAssignment.role == role)\
            .filter(DatasetAssignment.is_active == True)\
            .first()
        
        if not old_assignment:
            raise ValueError("原分配不存在或已被取消")
        
        # 验证新用户存在
        new_user = self.db.query(User).filter(User.id == new_user_id).first()
        if not new_user:
            raise ValueError(f"新用户不存在: {new_user_id}")
        
        # 验证新旧用户不同
        if old_user_id == new_user_id:
            raise ValueError("新用户不能与旧用户相同")
        
        # 根据转移模式执行不同的逻辑
        if transfer_mode == 'all':
            # 创建新分配，保持相同的任务范围
            new_assignment = DatasetAssignment(
                dataset_id=old_assignment.dataset_id,
                user_id=new_user_id,
                role=old_assignment.role,
                task_start_index=old_assignment.task_start_index,
                task_end_index=old_assignment.task_end_index,
                assigned_by=transferred_by,
                is_active=True
            )
            self.db.add(new_assignment)
            self.db.flush()
            
            # 禁用旧分配（不删除，保留历史）
            old_assignment.is_active = False
            old_assignment.transferred_to = new_user_id
            old_assignment.transferred_at = datetime.utcnow()
            old_assignment.transfer_reason = transfer_reason
            
            self.db.commit()
            self.db.refresh(new_assignment)
            
            # 统计转移的任务数
            transferred_tasks = self._count_tasks_in_range(
                old_assignment.dataset_id,
                old_assignment.task_start_index,
                old_assignment.task_end_index
            )
            
            # 获取旧用户信息
            old_user = self.db.query(User).filter(User.id == old_user_id).first()
            
            return {
                "old_assignment_id": old_assignment.id,
                "new_assignment_id": new_assignment.id,
                "old_user": {
                    "id": old_user_id,
                    "username": old_user.username if old_user else "未知"
                },
                "new_user": {
                    "id": new_user_id,
                    "username": new_user.username
                },
                "transferred_tasks": transferred_tasks,
                "transfer_mode": transfer_mode,
                "transferred_at": old_assignment.transferred_at.isoformat()
            }
        
        elif transfer_mode in ['remaining', 'completed']:
            # TODO: 实现部分转移逻辑
            # 这需要更复杂的范围计算，暂时不实现
            raise NotImplementedError(f"转移模式 '{transfer_mode}' 暂未实现")
        
        else:
            raise ValueError(f"不支持的转移模式: {transfer_mode}")
    
    def _count_tasks_in_range(
        self,
        dataset_id: int,
        start_index: Optional[int],
        end_index: Optional[int]
    ) -> int:
        """
        统计指定范围内的任务数量
        
        Args:
            dataset_id: 数据集ID
            start_index: 起始索引
            end_index: 结束索引
        
        Returns:
            int: 任务数量
        """
        if start_index is None or end_index is None:
            # 整体分配，返回所有任务数
            return self.db.query(AnnotationTask)\
                .filter(AnnotationTask.dataset_id == dataset_id)\
                .count()
        else:
            # 范围分配
            return end_index - start_index + 1

    
    def get_dataset_assignments(
        self,
        dataset_id: int,
        include_inactive: bool = False
    ) -> List[DatasetAssignment]:
        """
        获取数据集的所有分配
        
        Args:
            dataset_id: 数据集ID
            include_inactive: 是否包含不活跃的分配
        
        Returns:
            List[DatasetAssignment]: 分配列表
        """
        query = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)
        
        if not include_inactive:
            query = query.filter(DatasetAssignment.is_active == True)
        
        return query.order_by(DatasetAssignment.assigned_at.desc()).all()
    
    def get_user_datasets(
        self,
        user_id: int,
        role: Optional[str] = None
    ) -> List[Dataset]:
        """
        获取用户分配的数据集列表
        
        Args:
            user_id: 用户ID
            role: 角色筛选（可选）
        
        Returns:
            List[Dataset]: 数据集列表
        """
        query = self.db.query(Dataset)\
            .join(DatasetAssignment, Dataset.id == DatasetAssignment.dataset_id)\
            .filter(DatasetAssignment.user_id == user_id)\
            .filter(DatasetAssignment.is_active == True)
        
        if role:
            query = query.filter(DatasetAssignment.role == role)
        
        return query.distinct().all()
    
    def check_permission(
        self,
        user_id: int,
        dataset_id: int,
        required_role: str
    ) -> bool:
        """
        检查用户是否有权限访问数据集
        
        Args:
            user_id: 用户ID
            dataset_id: 数据集ID
            required_role: 需要的角色 ('annotator', 'reviewer', 'view')
        
        Returns:
            bool: 是否有权限
        """
        # 检查用户角色
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # 管理员有所有权限
        if user.role == 'admin':
            return True
        
        # 浏览员只能查看
        if user.role == 'viewer':
            return required_role == 'view'
        
        # 检查数据集分配
        assignment = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)\
            .filter(DatasetAssignment.user_id == user_id)\
            .filter(DatasetAssignment.role == required_role)\
            .filter(DatasetAssignment.is_active == True)\
            .first()
        
        return assignment is not None
    
    def get_user_task_range(
        self,
        user_id: int,
        dataset_id: int,
        role: str
    ) -> Optional[Tuple[Optional[int], Optional[int]]]:
        """
        获取用户在数据集中的任务范围
        
        Args:
            user_id: 用户ID
            dataset_id: 数据集ID
            role: 角色
        
        Returns:
            Optional[Tuple[start, end]]: 任务范围，None表示没有分配
        """
        assignment = self.db.query(DatasetAssignment)\
            .filter(DatasetAssignment.dataset_id == dataset_id)\
            .filter(DatasetAssignment.user_id == user_id)\
            .filter(DatasetAssignment.role == role)\
            .filter(DatasetAssignment.is_active == True)\
            .first()
        
        if not assignment:
            return None
        
        return (assignment.task_start_index, assignment.task_end_index)
