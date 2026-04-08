"""
任务查询服务
提供基于角色的任务查询和权限检查功能
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
import logging
from sqlalchemy import and_, or_, func, case

from models.db_models import (
    AnnotationTask, DatasetAssignment, User, Dataset, Corpus
)
from services.dataset_assignment_service import DatasetAssignmentService


class TaskQueryService:
    """任务查询服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assignment_service = DatasetAssignmentService(db)
        self.logger = logging.getLogger(__name__)
    
    def get_user_tasks(
        self,
        user_id: int,
        user_role: str,
        dataset_id: Optional[int] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[AnnotationTask], int]:
        """
        获取用户可访问的任务列表
        
        Args:
            user_id: 用户ID
            user_role: 用户角色 (admin/annotator/viewer)
            dataset_id: 数据集ID筛选（可选）
            status: 状态筛选（可选）
            page: 页码
            page_size: 每页数量
            sort_by: 排序字段
            sort_order: 排序方向
        
        Returns:
            (任务列表, 总数)
        """
        # 构建基础查询
        query = self._build_task_query(dataset_id, status)
        
        # 应用权限过滤
        query = self._apply_permission_filter(query, user_id, user_role, dataset_id)
        
        # 获取总数
        # 特殊排序：状态优先，本地排序以避免不同数据库的兼容性问题
        if sort_by == "status_priority":
            tasks_all = query.all()
            total = len(tasks_all)

            def _priority(t: AnnotationTask):
                order = {
                    "processing": 1,
                    "pending": 2,
                    "failed": 3,
                    "completed": 4,
                    "completed_with_errors": 4,
                    "reviewed": 5,
                }
                return (order.get(t.status, 6), -t.created_at.timestamp())

            tasks_all.sort(key=_priority)
            offset = (page - 1) * page_size
            tasks = tasks_all[offset:offset + page_size]
            return tasks, total

        total = query.count()
        query = self._apply_sorting(query, sort_by, sort_order)
        offset = (page - 1) * page_size
        tasks = query.offset(offset).limit(page_size).all()
        return tasks, total
    
    def check_task_permission(
        self,
        user_id: int,
        user_role: str,
        task_id: int
    ) -> bool:
        """
        检查用户是否有权限访问指定任务
        
        Args:
            user_id: 用户ID
            user_role: 用户角色
            task_id: 任务ID
        
        Returns:
            是否有权限
        """
        # 获取任务
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.id == task_id
        ).first()
        
        if not task:
            return False
        
        # 管理员有所有权限
        if user_role == 'admin':
            return True
        
        # 浏览员只能访问已完成的任务
        if user_role == 'viewer':
            return task.status == 'completed'
        
        # 标注员需要检查分配
        if user_role == 'annotator':
            return self._check_annotator_task_permission(user_id, task)
        
        return False
    
    def _build_task_query(
        self,
        dataset_id: Optional[int] = None,
        status: Optional[str] = None
    ):
        """
        构建基础任务查询
        
        Args:
            dataset_id: 数据集ID筛选
            status: 状态筛选
        
        Returns:
            Query对象
        """
        query = self.db.query(AnnotationTask)
        
        # 数据集筛选
        if dataset_id is not None:
            query = query.filter(AnnotationTask.dataset_id == dataset_id)
        
        # 状态筛选
        if status:
            query = query.filter(AnnotationTask.status == status)
        
        return query
    
    def _apply_permission_filter(
        self,
        query,
        user_id: int,
        user_role: str,
        dataset_id: Optional[int] = None
    ):
        """
        应用权限过滤
        
        Args:
            query: 查询对象
            user_id: 用户ID
            user_role: 用户角色
            dataset_id: 数据集ID（可选）
        
        Returns:
            过滤后的查询对象
        """
        # 管理员可以访问所有任务
        if user_role == 'admin':
            return query
        
        # 浏览员只能访问已完成的任务
        if user_role == 'viewer':
            return query.filter(AnnotationTask.status == 'completed')
        
        # 标注员只能访问分配给他们的任务
        if user_role == 'annotator':
            return self._apply_annotator_filter(query, user_id, dataset_id)
        
        # 其他角色无权限，返回空查询
        return query.filter(False)
    
    def _apply_annotator_filter(
        self,
        query,
        user_id: int,
        dataset_id: Optional[int] = None
    ):
        """
        应用标注员权限过滤
        
        Args:
            query: 查询对象
            user_id: 用户ID
            dataset_id: 数据集ID（可选）
        
        Returns:
            过滤后的查询对象
        """
        # 获取用户的所有活跃分配
        assignments_query = self.db.query(DatasetAssignment).filter(
            DatasetAssignment.user_id == user_id,
            DatasetAssignment.role == 'annotator',
            DatasetAssignment.is_active == True
        )
        
        # 如果指定了数据集，只获取该数据集的分配
        if dataset_id is not None:
            assignments_query = assignments_query.filter(
                DatasetAssignment.dataset_id == dataset_id
            )
        
        assignments = assignments_query.all()
        
        if not assignments:
            # 没有分配，返回空查询
            return query.filter(False)
        
        # 构建权限条件
        permission_conditions = []
        
        for assignment in assignments:
            # 如果是整体分配（task_start_index 和 task_end_index 为 NULL）
            if assignment.task_start_index is None and assignment.task_end_index is None:
                # 该数据集的所有任务
                permission_conditions.append(
                    AnnotationTask.dataset_id == assignment.dataset_id
                )
            else:
                # 范围分配，需要使用子查询来计算任务索引
                # 使用窗口函数 ROW_NUMBER() 来计算任务在数据集中的索引
                permission_conditions.append(
                    self._create_range_condition(
                        assignment.dataset_id,
                        assignment.task_start_index,
                        assignment.task_end_index
                    )
                )
        
        # 应用权限条件（OR关系）
        if permission_conditions:
            query = query.filter(or_(*permission_conditions))
        else:
            query = query.filter(False)
        
        return query
    
    def _create_range_condition(
        self,
        dataset_id: int,
        start_index: int,
        end_index: int
    ):
        """
        创建任务范围条件
        
        Args:
            dataset_id: 数据集ID
            start_index: 起始索引
            end_index: 结束索引
        
        Returns:
            条件表达式
        """
        # 获取该数据集中指定范围的任务ID列表
        # 按ID排序后取指定范围
        tasks_in_range = self.db.query(AnnotationTask.id)\
            .filter(AnnotationTask.dataset_id == dataset_id)\
            .order_by(AnnotationTask.id)\
            .offset(start_index - 1)\
            .limit(end_index - start_index + 1)\
            .all()
        
        task_ids = [task.id for task in tasks_in_range]
        
        if task_ids:
            return AnnotationTask.id.in_(task_ids)
        else:
            return False
    
    def _check_annotator_task_permission(
        self,
        user_id: int,
        task: AnnotationTask
    ) -> bool:
        """
        检查标注员是否有权限访问指定任务
        
        Args:
            user_id: 用户ID
            task: 任务对象
        
        Returns:
            是否有权限
        """
        # 获取用户在该数据集的分配
        task_range = self.assignment_service.get_user_task_range(
            user_id=user_id,
            dataset_id=task.dataset_id,
            role='annotator'
        )
        
        if not task_range:
            return False
        
        start_index, end_index = task_range
        
        # 如果是整体分配
        if start_index is None and end_index is None:
            return True
        
        # 如果是范围分配，需要计算任务在数据集中的索引
        task_index = self._get_task_index_in_dataset(task.id, task.dataset_id)
        
        if task_index is None:
            return False
        
        # 检查任务索引是否在分配范围内
        return start_index <= task_index <= end_index
    
    def _get_task_index_in_dataset(
        self,
        task_id: int,
        dataset_id: int
    ) -> Optional[int]:
        """
        获取任务在数据集中的索引（从1开始）
        
        Args:
            task_id: 任务ID
            dataset_id: 数据集ID
        
        Returns:
            任务索引，如果任务不存在返回None
        """
        # 获取该数据集的所有任务ID（按ID排序）
        task_ids = self.db.query(AnnotationTask.id)\
            .filter(AnnotationTask.dataset_id == dataset_id)\
            .order_by(AnnotationTask.id)\
            .all()
        
        task_ids = [t.id for t in task_ids]
        
        try:
            # 索引从1开始
            return task_ids.index(task_id) + 1
        except ValueError:
            return None
    
    def _apply_sorting(
        self,
        query,
        sort_by: str,
        sort_order: str
    ):
        """
        应用排序
        
        Args:
            query: 查询对象
            sort_by: 排序字段
            sort_order: 排序方向
        
        Returns:
            排序后的查询对象
        """
        # 自定义状态优先级排序：processing -> pending -> failed -> completed -> reviewed
        if sort_by == 'status_priority':
            try:
                priority = case(
                    [
                        (AnnotationTask.status == 'processing', 1),
                        (AnnotationTask.status == 'pending', 2),
                        (AnnotationTask.status == 'failed', 3),
                        (AnnotationTask.status == 'completed', 4),
                        (AnnotationTask.status == 'completed_with_errors', 4),
                        (AnnotationTask.status == 'reviewed', 5),
                    ],
                    else_=6,
                )
                # 状态优先，次序按创建时间倒序
                return query.order_by(priority, AnnotationTask.created_at.desc())
            except Exception as e:
                # 若排序构造异常则降级为按创建时间倒序
                self.logger.warning(f"status_priority sorting failed, fallback to created_at desc: {e}")
                sort_by = 'created_at'
        
        # 验证排序字段
        valid_sort_fields = ['created_at', 'updated_at', 'status', 'id']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        
        # 获取排序字段
        sort_field = getattr(AnnotationTask, sort_by)
        
        # 应用排序方向
        if sort_order.lower() == 'asc':
            query = query.order_by(sort_field.asc())
        else:
            query = query.order_by(sort_field.desc())
        
        return query
