"""
复核服务
实现标注任务的复核流程管理
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
import uuid

from models.db_models import (
    ReviewTask, AnnotationTask, TextEntity, ImageEntity, Relation, User
)
from models.schemas import ReviewStatus


class ReviewService:
    """复核服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def can_user_review_task(self, user_id: int, task_id: int) -> tuple[bool, str]:
        """
        检查用户是否可以复核指定任务
        
        Args:
            user_id: 用户ID
            task_id: 标注任务ID
        
        Returns:
            tuple: (是否可以复核, 原因说明)
        """
        # 查询用户
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "用户不存在"
        
        # 查询任务
        task = self.db.query(AnnotationTask).filter(AnnotationTask.id == task_id).first()
        if not task:
            return False, "任务不存在"
        
        # 管理员可以复核所有任务
        if user.role == 'admin':
            return True, "管理员权限"
        
        # 标注员可以复核他人的任务
        if user.role == 'annotator':
            # 检查任务是否是自己标注的
            if task.assigned_to == user_id:
                return False, "不能复核自己标注的任务"
            return True, "可以复核他人的任务"
        
        # 浏览员不能复核
        if user.role == 'viewer':
            return False, "浏览员没有复核权限"
        
        return False, "角色权限不足"
    
    def submit_for_review(
        self,
        task_id: int,
        reviewer_id: Optional[int] = None
    ) -> ReviewTask:
        """
        提交标注任务进行复核
        
        Args:
            task_id: 标注任务ID
            reviewer_id: 指定的复核人员ID（可选）
        
        Returns:
            ReviewTask: 创建的复核任务
        
        Raises:
            ValueError: 任务不存在或状态不允许提交复核
        """
        # 查询标注任务
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.id == task_id
        ).first()
        
        if not task:
            raise ValueError(f"标注任务不存在: {task_id}")
        
        # 验证任务状态
        if task.status != 'completed':
            raise ValueError(f"任务状态必须为completed才能提交复核，当前状态: {task.status}")
        
        # 检查是否已有待处理的复核任务
        existing_review = self.db.query(ReviewTask).filter(
            and_(
                ReviewTask.task_id == task_id,
                ReviewTask.status == 'pending'
            )
        ).first()
        
        if existing_review:
            raise ValueError(f"任务已有待处理的复核任务: {existing_review.review_id}")
        
        # 创建复核任务
        review_id = f"REV_{uuid.uuid4().hex[:12].upper()}"
        review_task = ReviewTask(
            review_id=review_id,
            task_id=task_id,
            status='pending',
            reviewer_id=reviewer_id
        )
        
        self.db.add(review_task)
        
        # 更新标注任务状态为待复核
        task.status = 'under_review'
        task.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(review_task)
        
        return review_task
    
    def get_review_tasks(
        self,
        status: Optional[str] = None,
        reviewer_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[ReviewTask], int]:
        """
        查询复核任务列表
        
        Args:
            status: 复核状态筛选（pending/approved/rejected）
            reviewer_id: 复核人员ID筛选
            skip: 跳过记录数
            limit: 返回记录数
        
        Returns:
            tuple: (复核任务列表, 总数)
        """
        query = self.db.query(ReviewTask)
        
        # 状态筛选
        if status:
            query = query.filter(ReviewTask.status == status)
        
        # 复核人员筛选
        if reviewer_id:
            query = query.filter(ReviewTask.reviewer_id == reviewer_id)
        
        # 获取总数
        total = query.count()
        
        # 分页查询
        reviews = query.order_by(ReviewTask.created_at.desc()).offset(skip).limit(limit).all()
        
        return reviews, total

    
    def approve_task(
        self,
        review_id: str,
        reviewer_id: int,
        comment: Optional[str] = None
    ) -> ReviewTask:
        """
        批准标注任务
        
        Args:
            review_id: 复核任务ID
            reviewer_id: 复核人员ID
            comment: 复核意见（可选）
        
        Returns:
            ReviewTask: 更新后的复核任务
        
        Raises:
            ValueError: 复核任务不存在或状态不允许批准
        """
        # 查询复核任务
        review = self.db.query(ReviewTask).filter(
            ReviewTask.review_id == review_id
        ).first()
        
        if not review:
            raise ValueError(f"复核任务不存在: {review_id}")
        
        if review.status != 'pending':
            raise ValueError(f"复核任务状态必须为pending才能批准，当前状态: {review.status}")
        
        # 更新复核任务
        review.status = 'approved'
        review.reviewer_id = reviewer_id
        review.review_comment = comment
        review.reviewed_at = datetime.utcnow()
        
        # 更新标注任务状态
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.id == review.task_id
        ).first()
        
        if task:
            task.status = 'approved'
            task.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(review)
        
        return review
    
    def reject_task(
        self,
        review_id: str,
        reviewer_id: int,
        comment: str
    ) -> ReviewTask:
        """
        驳回标注任务
        
        Args:
            review_id: 复核任务ID
            reviewer_id: 复核人员ID
            comment: 驳回原因（必填）
        
        Returns:
            ReviewTask: 更新后的复核任务
        
        Raises:
            ValueError: 复核任务不存在、状态不允许驳回或缺少驳回原因
        """
        if not comment or not comment.strip():
            raise ValueError("驳回任务时必须填写驳回原因")
        
        # 查询复核任务
        review = self.db.query(ReviewTask).filter(
            ReviewTask.review_id == review_id
        ).first()
        
        if not review:
            raise ValueError(f"复核任务不存在: {review_id}")
        
        if review.status != 'pending':
            raise ValueError(f"复核任务状态必须为pending才能驳回，当前状态: {review.status}")
        
        # 更新复核任务
        review.status = 'rejected'
        review.reviewer_id = reviewer_id
        review.review_comment = comment
        review.reviewed_at = datetime.utcnow()
        
        # 更新标注任务状态为待修改
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.id == review.task_id
        ).first()
        
        if task:
            task.status = 'rejected'
            task.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(review)
        
        return review
    
    def get_review_task_detail(self, review_id: str) -> Optional[Dict[str, Any]]:
        """
        获取复核任务详情（包含标注数据）
        
        Args:
            review_id: 复核任务ID
        
        Returns:
            Dict: 复核任务详情，包含标注任务和所有标注数据
        """
        # 查询复核任务
        review = self.db.query(ReviewTask).filter(
            ReviewTask.review_id == review_id
        ).first()
        
        if not review:
            return None
        
        # 查询标注任务
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.id == review.task_id
        ).first()
        
        if not task:
            return None
        
        # 查询当前版本的所有实体和关系
        text_entities = self.db.query(TextEntity).filter(
            and_(
                TextEntity.task_id == task.id,
                TextEntity.version == task.current_version
            )
        ).all()
        
        image_entities = self.db.query(ImageEntity).filter(
            and_(
                ImageEntity.task_id == task.id,
                ImageEntity.version == task.current_version
            )
        ).all()
        
        relations = self.db.query(Relation).filter(
            and_(
                Relation.task_id == task.id,
                Relation.version == task.current_version
            )
        ).all()
        
        # 组装返回数据
        return {
            "review_id": review.review_id,
            "status": review.status,
            "reviewer_id": review.reviewer_id,
            "review_comment": review.review_comment,
            "reviewed_at": review.reviewed_at,
            "created_at": review.created_at,
            "task": {
                "task_id": task.task_id,
                "status": task.status,
                "annotation_type": task.annotation_type,
                "current_version": task.current_version,
                "text_entities": [
                    {
                        "id": e.entity_id,
                        "token": e.token,
                        "label": e.label,
                        "start_offset": e.start_offset,
                        "end_offset": e.end_offset,
                        "confidence": e.confidence
                    }
                    for e in text_entities
                ],
                "image_entities": [
                    {
                        "id": e.entity_id,
                        "image_id": e.image_id,
                        "label": e.label,
                        "bbox": {
                            "x": e.bbox_x,
                            "y": e.bbox_y,
                            "width": e.bbox_width,
                            "height": e.bbox_height
                        } if e.bbox_x is not None else None,
                        "confidence": e.confidence
                    }
                    for e in image_entities
                ],
                "relations": [
                    {
                        "id": r.relation_id,
                        "from_entity_id": r.from_entity_id,
                        "to_entity_id": r.to_entity_id,
                        "relation_type": r.relation_type
                    }
                    for r in relations
                ]
            }
        }

    
    def record_review_modifications(
        self,
        review_id: str,
        modifications: Dict[str, Any]
    ) -> None:
        """
        记录复核过程中的修改差异
        
        Args:
            review_id: 复核任务ID
            modifications: 修改记录，包含added/removed/modified实体和关系
        
        Raises:
            ValueError: 复核任务不存在
        """
        # 查询复核任务
        review = self.db.query(ReviewTask).filter(
            ReviewTask.review_id == review_id
        ).first()
        
        if not review:
            raise ValueError(f"复核任务不存在: {review_id}")
        
        # 将修改记录存储到review_comment字段（JSON格式）
        import json
        
        # 如果已有comment，追加修改记录
        if review.review_comment:
            try:
                existing_data = json.loads(review.review_comment)
                if isinstance(existing_data, dict) and 'modifications' in existing_data:
                    existing_data['modifications'] = modifications
                else:
                    existing_data = {
                        'comment': review.review_comment,
                        'modifications': modifications
                    }
                review.review_comment = json.dumps(existing_data, ensure_ascii=False)
            except json.JSONDecodeError:
                # 原有comment不是JSON，保留原comment并添加modifications
                review.review_comment = json.dumps({
                    'comment': review.review_comment,
                    'modifications': modifications
                }, ensure_ascii=False)
        else:
            review.review_comment = json.dumps({
                'modifications': modifications
            }, ensure_ascii=False)
        
        self.db.commit()
    
    def calculate_quality_statistics(
        self,
        dataset_id: int
    ) -> Dict[str, Any]:
        """
        计算数据集的质量统计指标
        
        Args:
            dataset_id: 数据集ID
        
        Returns:
            Dict: 质量统计指标
        """
        # 查询数据集的所有标注任务
        tasks = self.db.query(AnnotationTask).filter(
            AnnotationTask.dataset_id == dataset_id
        ).all()
        
        if not tasks:
            return {
                "total_tasks": 0,
                "completed_tasks": 0,
                "under_review_tasks": 0,
                "approved_tasks": 0,
                "rejected_tasks": 0,
                "completion_rate": 0.0,
                "approval_rate": 0.0,
                "rejection_rate": 0.0,
                "average_entities_per_task": 0.0,
                "average_relations_per_task": 0.0
            }
        
        total_tasks = len(tasks)
        task_ids = [t.id for t in tasks]
        
        # 统计各状态任务数
        completed_tasks = sum(1 for t in tasks if t.status == 'completed')
        under_review_tasks = sum(1 for t in tasks if t.status == 'under_review')
        approved_tasks = sum(1 for t in tasks if t.status == 'approved')
        rejected_tasks = sum(1 for t in tasks if t.status == 'rejected')
        
        # 计算比率
        completion_rate = (completed_tasks + under_review_tasks + approved_tasks) / total_tasks if total_tasks > 0 else 0.0
        approval_rate = approved_tasks / total_tasks if total_tasks > 0 else 0.0
        rejection_rate = rejected_tasks / total_tasks if total_tasks > 0 else 0.0
        
        # 统计实体和关系数量
        total_entities = 0
        total_relations = 0
        
        for task in tasks:
            # 统计当前版本的实体数
            text_entity_count = self.db.query(func.count(TextEntity.id)).filter(
                and_(
                    TextEntity.task_id == task.id,
                    TextEntity.version == task.current_version
                )
            ).scalar() or 0
            
            image_entity_count = self.db.query(func.count(ImageEntity.id)).filter(
                and_(
                    ImageEntity.task_id == task.id,
                    ImageEntity.version == task.current_version
                )
            ).scalar() or 0
            
            relation_count = self.db.query(func.count(Relation.id)).filter(
                and_(
                    Relation.task_id == task.id,
                    Relation.version == task.current_version
                )
            ).scalar() or 0
            
            total_entities += (text_entity_count + image_entity_count)
            total_relations += relation_count
        
        # 计算平均值
        avg_entities = total_entities / total_tasks if total_tasks > 0 else 0.0
        avg_relations = total_relations / total_tasks if total_tasks > 0 else 0.0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "under_review_tasks": under_review_tasks,
            "approved_tasks": approved_tasks,
            "rejected_tasks": rejected_tasks,
            "completion_rate": round(completion_rate, 4),
            "approval_rate": round(approval_rate, 4),
            "rejection_rate": round(rejection_rate, 4),
            "average_entities_per_task": round(avg_entities, 2),
            "average_relations_per_task": round(avg_relations, 2),
            "total_entities": total_entities,
            "total_relations": total_relations
        }
    
    def get_dataset_review_summary(
        self,
        dataset_id: int
    ) -> Dict[str, Any]:
        """
        获取数据集的复核摘要信息
        
        Args:
            dataset_id: 数据集ID
        
        Returns:
            Dict: 复核摘要信息
        """
        # 查询数据集的所有复核任务
        reviews = self.db.query(ReviewTask).join(
            AnnotationTask,
            ReviewTask.task_id == AnnotationTask.id
        ).filter(
            AnnotationTask.dataset_id == dataset_id
        ).all()
        
        if not reviews:
            return {
                "total_reviews": 0,
                "pending_reviews": 0,
                "approved_reviews": 0,
                "rejected_reviews": 0,
                "average_review_time_hours": 0.0
            }
        
        total_reviews = len(reviews)
        pending_reviews = sum(1 for r in reviews if r.status == 'pending')
        approved_reviews = sum(1 for r in reviews if r.status == 'approved')
        rejected_reviews = sum(1 for r in reviews if r.status == 'rejected')
        
        # 计算平均复核时间（仅统计已完成的复核）
        completed_reviews = [r for r in reviews if r.reviewed_at]
        if completed_reviews:
            total_hours = sum(
                (r.reviewed_at - r.created_at).total_seconds() / 3600
                for r in completed_reviews
            )
            avg_review_time = total_hours / len(completed_reviews)
        else:
            avg_review_time = 0.0
        
        return {
            "total_reviews": total_reviews,
            "pending_reviews": pending_reviews,
            "approved_reviews": approved_reviews,
            "rejected_reviews": rejected_reviews,
            "average_review_time_hours": round(avg_review_time, 2)
        }
