"""
批量标注服务
提供批量自动标注功能,支持异步执行和进度跟踪
"""
import logging
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.db_models import (
    Dataset, AnnotationTask, BatchJob, Corpus,
    TextEntity, Relation
)
from agents.entity_extraction import EntityExtractionAgent
from agents.relation_extraction import RelationExtractionAgent
from services.label_config_cache import LabelConfigCache
from services.offset_correction import OffsetCorrectionService

logger = logging.getLogger(__name__)


class BatchAnnotationService:
    """批量标注服务"""
    
    def __init__(self, db: Session):
        """
        初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.entity_agent = EntityExtractionAgent()
        self.relation_agent = RelationExtractionAgent()
        self.offset_service = OffsetCorrectionService()
    
    def create_batch_job(
        self,
        dataset_id: str,
        created_by: Optional[int] = None,
        user_role: str = 'admin',
        task_ids: Optional[list] = None
    ) -> BatchJob:
        """
        创建批量标注任务
        
        Args:
            dataset_id: 数据集ID
            created_by: 创建人ID
            user_role: 用户角色
            task_ids: 指定要标注的任务ID列表（可选）
            
        Returns:
            BatchJob: 批量任务对象
        """
        # 查询数据集
        dataset = self.db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        
        if not dataset:
            raise ValueError(f"数据集 {dataset_id} 不存在")
        
        # 构建基础查询
        query = self.db.query(AnnotationTask)\
            .filter(AnnotationTask.dataset_id == dataset.id)\
            .filter(AnnotationTask.status == 'pending')
        
        # 如果指定了任务ID列表，只查询这些任务
        if task_ids:
            query = query.filter(AnnotationTask.task_id.in_(task_ids))
        
        # 应用权限过滤（标注员只能标注分配给自己的任务）
        if user_role == 'annotator' and created_by:
            from models.db_models import DatasetAssignment
            
            # 查询用户的数据集分配
            assignment = self.db.query(DatasetAssignment).filter(
                DatasetAssignment.dataset_id == dataset.id,
                DatasetAssignment.user_id == created_by,
                DatasetAssignment.role == 'annotator',
                DatasetAssignment.is_active == True
            ).first()
            
            if assignment:
                # 如果有任务范围限制
                if assignment.task_start_index is not None and assignment.task_end_index is not None:
                    # 获取任务范围内的任务ID
                    all_tasks = self.db.query(AnnotationTask)\
                        .filter(AnnotationTask.dataset_id == dataset.id)\
                        .order_by(AnnotationTask.id)\
                        .all()
                    
                    # 计算范围内的任务
                    start_idx = assignment.task_start_index - 1  # 转换为0-based索引
                    end_idx = assignment.task_end_index
                    range_tasks = all_tasks[start_idx:end_idx]
                    range_task_ids = [t.id for t in range_tasks]
                    
                    # 应用范围过滤
                    query = query.filter(AnnotationTask.id.in_(range_task_ids))
                # 如果没有范围限制，标注员可以标注该数据集的所有任务
        
        # 统计任务数量
        total_tasks = query.count()
        
        if total_tasks == 0:
            if task_ids:
                raise ValueError("指定的任务不存在或您没有权限标注这些任务")
            elif user_role == 'annotator':
                raise ValueError("没有分配给您的待标注任务")
            else:
                raise ValueError("没有待标注的任务")
        
        # 生成任务ID
        job_id = f"batch-{uuid.uuid4().hex[:12]}"
        
        # 创建批量任务记录
        batch_job = BatchJob(
            job_id=job_id,
            dataset_id=dataset.id,
            status='pending',
            total_tasks=total_tasks,
            completed_tasks=0,
            failed_tasks=0,
            progress=0.0,
            created_by=created_by
        )
        
        self.db.add(batch_job)
        self.db.commit()
        self.db.refresh(batch_job)
        
        return batch_job
    
    def get_batch_job(self, job_id: str) -> Optional[BatchJob]:
        """
        获取批量任务详情
        
        Args:
            job_id: 任务ID
            
        Returns:
            Optional[BatchJob]: 批量任务对象
        """
        return self.db.query(BatchJob).filter(BatchJob.job_id == job_id).first()
    
    def update_batch_job_status(
        self,
        job_id: str,
        status: str,
        completed_tasks: Optional[int] = None,
        failed_tasks: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> Optional[BatchJob]:
        """
        更新批量任务状态
        
        Args:
            job_id: 任务ID
            status: 状态
            completed_tasks: 完成任务数
            failed_tasks: 失败任务数
            error_message: 错误信息
            
        Returns:
            Optional[BatchJob]: 更新后的批量任务对象
        """
        batch_job = self.get_batch_job(job_id)
        
        if not batch_job:
            return None
        
        # 更新状态
        batch_job.status = status
        
        if completed_tasks is not None:
            batch_job.completed_tasks = completed_tasks
        
        if failed_tasks is not None:
            batch_job.failed_tasks = failed_tasks
        
        # 计算进度
        if batch_job.total_tasks > 0:
            batch_job.progress = (batch_job.completed_tasks + batch_job.failed_tasks) / batch_job.total_tasks
        
        # 更新时间戳
        if status == 'processing' and not batch_job.started_at:
            batch_job.started_at = datetime.utcnow()
        elif status in ['completed', 'completed_with_errors', 'failed']:
            batch_job.completed_at = datetime.utcnow()
        
        if error_message:
            batch_job.error_message = error_message
        
        self.db.commit()
        self.db.refresh(batch_job)
        
        return batch_job
    
    def execute_batch_annotation(
        self,
        job_id: str,
        user_id: Optional[int] = None,
        user_role: str = 'admin',
        task_ids: Optional[list] = None
    ):
        """
        执行批量标注(异步)
        
        Args:
            job_id: 任务ID
            user_id: 用户ID
            user_role: 用户角色
        """
        batch_job = self.get_batch_job(job_id)
        
        if not batch_job:
            raise ValueError(f"批量任务 {job_id} 不存在")
        
        try:
            # 更新状态为处理中
            self.update_batch_job_status(job_id, 'processing')
            
            # 构建查询 - 获取创建批量任务时确定的任务列表
            query = self.db.query(AnnotationTask)\
                .filter(AnnotationTask.dataset_id == batch_job.dataset_id)\
                .filter(AnnotationTask.status == 'pending')

            # 如果指定了任务ID列表（选中标注），只处理这些任务
            if task_ids:
                query = query.filter(AnnotationTask.task_id.in_(task_ids))

            # 应用权限过滤（与create_batch_job保持一致）
            if user_role == 'annotator' and user_id:
                from models.db_models import DatasetAssignment
                
                assignment = self.db.query(DatasetAssignment).filter(
                    DatasetAssignment.dataset_id == batch_job.dataset_id,
                    DatasetAssignment.user_id == user_id,
                    DatasetAssignment.role == 'annotator',
                    DatasetAssignment.is_active == True
                ).first()
                
                if assignment:
                    if assignment.task_start_index is not None and assignment.task_end_index is not None:
                        all_tasks = self.db.query(AnnotationTask)\
                            .filter(AnnotationTask.dataset_id == batch_job.dataset_id)\
                            .order_by(AnnotationTask.id)\
                            .all()
                        
                        start_idx = assignment.task_start_index - 1
                        end_idx = assignment.task_end_index
                        range_tasks = all_tasks[start_idx:end_idx]
                        range_task_ids = [t.id for t in range_tasks]
                        
                        query = query.filter(AnnotationTask.id.in_(range_task_ids))
            
            # 获取任务列表
            tasks = query.all()
            
            completed_count = 0
            failed_count = 0
            
            # 逐个处理任务
            for task in tasks:
                try:
                    # 标注单个任务
                    self._annotate_single_task(task)
                    completed_count += 1
                except Exception as e:
                    # 记录失败
                    task.status = 'failed'
                    task.error_message = str(e)
                    failed_count += 1
                
                # 更新进度
                self.update_batch_job_status(
                    job_id,
                    'processing',
                    completed_tasks=completed_count,
                    failed_tasks=failed_count
                )
                
                self.db.commit()
            
            # 更新最终状态
            final_status = 'completed' if failed_count == 0 else 'completed_with_errors'
            self.update_batch_job_status(
                job_id,
                final_status,
                completed_tasks=completed_count,
                failed_tasks=failed_count
            )
            
        except Exception as e:
            # 批量任务失败
            self.update_batch_job_status(
                job_id,
                'failed',
                error_message=str(e)
            )
            raise
    
    def _annotate_single_task(self, task: AnnotationTask):
        """
        标注单个任务
        
        Args:
            task: 标注任务对象
        """
        # 获取语料
        corpus = self.db.query(Corpus).filter(Corpus.id == task.corpus_id).first()
        
        if not corpus:
            raise ValueError(f"语料 {task.corpus_id} 不存在")

        # 检测图片类语料（仅含图片 Markdown，如 ![图片](ID_...)）无法进行文本实体抽取
        corpus_text_stripped = (corpus.text or '').strip()
        if corpus_text_stripped.startswith('!['):
            logger.info(
                f"[批量标注] task={task.task_id} 检测到图片类语料，跳过自动标注"
            )
            task.status = 'completed'
            task.annotation_type = 'automatic'
            task.error_message = '图片类语料，已跳过自动标注'
            self.db.commit()
            return

        # 更新任务状态
        task.status = 'processing'
        task.annotation_type = 'automatic'
        self.db.commit()
        
        try:
            # 1. 实体抽取
            active_entity_types = LabelConfigCache.get_entity_types(self.db)
            logger.info(f"[批量标注] task={task.task_id} 加载实体类型数={len(active_entity_types)}")
            entity_result = self.entity_agent.extract_entities(
                text_id=corpus.text_id,
                text=corpus.text,
                entity_types=active_entity_types
            )

            # 基于当前生效标签体系（active+reviewed）构建中英文映射
            entity_label_map = self._build_entity_label_map()
            relation_label_map = self._build_relation_label_map()
            allowed_entity_labels = self._get_allowed_entity_labels()
            allowed_relation_labels = self._get_allowed_relation_labels()
            logger.info(f"[批量标注] task={task.task_id} 允许实体标签集合={allowed_entity_labels}")
            
            # 保存实体
            entity_id_map = {}  # 临时ID -> 数据库ID的映射
            saved_count = 0
            for entity in entity_result.entities:
                normalized_label = self._normalize_entity_label(entity.label, entity_label_map)
                if normalized_label not in allowed_entity_labels:
                    logger.warning(f"[批量标注] task={task.task_id} 实体标签 '{entity.label}'->规范化后'{normalized_label}' 不在允许列表，已过滤")
                    continue
                entity.label = normalized_label
                entity_confidence = getattr(entity, 'confidence', None)
                text_entity = TextEntity(
                    task_id=task.id,
                    entity_id=f"entity-{uuid.uuid4().hex[:8]}",
                    token=entity.token,
                    label=entity.label,
                    start_offset=entity.start_offset,
                    end_offset=entity.end_offset,
                    confidence=entity_confidence,
                    version=task.current_version
                )
                self.db.add(text_entity)
                self.db.flush()
                saved_count += 1
                
                # 记录映射关系
                entity_id_map[entity.id] = text_entity.entity_id
            
            logger.info(f"[批量标注] task={task.task_id} 实体入库数={saved_count}")
            
            # 2. 关系抽取
            # 直接使用ExtractedEntity对象列表（relation_agent依赖实体属性访问）
            entities_for_relation = entity_result.entities
            
            if entities_for_relation:
                active_relation_types = LabelConfigCache.get_relation_types(self.db)
                relation_result = self.relation_agent.extract_relations(
                    text_id=corpus.text_id,
                    text=corpus.text,
                    entities=entities_for_relation,
                    relation_types=active_relation_types
                )
                
                # 保存关系
                for relation in relation_result.relations:
                    # 映射临时ID到数据库ID
                    from_entity_id = entity_id_map.get(relation.from_id)
                    to_entity_id = entity_id_map.get(relation.to_id)
                    
                    if from_entity_id and to_entity_id:
                        normalized_relation_type = self._normalize_relation_label(
                            relation.type,
                            relation_label_map
                        )
                        if normalized_relation_type not in allowed_relation_labels:
                            continue
                        text_relation = Relation(
                            task_id=task.id,
                            relation_id=f"relation-{uuid.uuid4().hex[:8]}",
                            from_entity_id=from_entity_id,
                            to_entity_id=to_entity_id,
                            relation_type=normalized_relation_type,
                            version=task.current_version
                        )
                        self.db.add(text_relation)
            
            # 更新任务状态为完成
            task.status = 'completed'
            task.error_message = None
            
            self.db.commit()
            
        except Exception as e:
            # 标注失败
            task.status = 'failed'
            task.error_message = str(e)
            self.db.commit()
            raise

    def _build_entity_label_map(self) -> Dict[str, str]:
        """构建实体标签映射：英文名/中文名（大小写不敏感） -> 中文名。"""
        entity_types = LabelConfigCache.get_entity_types(self.db)
        label_map: Dict[str, str] = {}

        for entity_type in entity_types:
            target_label = (entity_type.type_name_zh or '').strip()
            if not target_label:
                continue

            for source_label in [entity_type.type_name, entity_type.type_name_zh]:
                normalized_key = self._normalize_label_key(source_label)
                if normalized_key:
                    label_map[normalized_key] = target_label

        return label_map

    @staticmethod
    def _normalize_label_key(label: Optional[str]) -> Optional[str]:
        """标准化标签键（去空格+小写）用于匹配。"""
        if not label:
            return None
        normalized = label.strip()
        if not normalized:
            return None
        return normalized.casefold()

    def _normalize_entity_label(self, label: str, label_map: Dict[str, str]) -> str:
        """将实体标签标准化为当前生效标签体系中的中文标签。"""
        normalized_key = self._normalize_label_key(label)
        if not normalized_key:
            return label
        return label_map.get(normalized_key, label)

    def _build_relation_label_map(self) -> Dict[str, str]:
        """构建关系标签映射：英文名/中文名（大小写不敏感） -> 中文名。"""
        relation_types = LabelConfigCache.get_relation_types(self.db)
        label_map: Dict[str, str] = {}

        for relation_type in relation_types:
            target_label = (relation_type.type_name_zh or '').strip()
            if not target_label:
                continue

            for source_label in [relation_type.type_name, relation_type.type_name_zh]:
                normalized_key = self._normalize_label_key(source_label)
                if normalized_key:
                    label_map[normalized_key] = target_label

        return label_map

    def _normalize_relation_label(self, label: str, label_map: Dict[str, str]) -> str:
        """将关系标签标准化为当前生效标签体系中的中文标签。"""
        normalized_key = self._normalize_label_key(label)
        if not normalized_key:
            return label
        return label_map.get(normalized_key, label)

    def _get_allowed_entity_labels(self) -> set[str]:
        """获取允许落库的实体中文标签集合。"""
        entity_types = LabelConfigCache.get_entity_types(self.db)
        return {
            (entity_type.type_name_zh or '').strip()
            for entity_type in entity_types
            if (entity_type.type_name_zh or '').strip()
        }

    def _get_allowed_relation_labels(self) -> set[str]:
        """获取允许落库的关系中文标签集合。"""
        relation_types = LabelConfigCache.get_relation_types(self.db)
        return {
            (relation_type.type_name_zh or '').strip()
            for relation_type in relation_types
            if (relation_type.type_name_zh or '').strip()
        }
    
    def cancel_batch_job(self, job_id: str) -> bool:
        """
        取消批量任务
        
        Args:
            job_id: 任务ID
            
        Returns:
            bool: 是否取消成功
        """
        batch_job = self.get_batch_job(job_id)
        
        if not batch_job:
            return False
        
        # 只能取消pending或processing状态的任务
        if batch_job.status not in ['pending', 'processing']:
            return False
        
        # 更新状态为已取消
        batch_job.status = 'cancelled'
        batch_job.completed_at = datetime.utcnow()
        
        self.db.commit()
        
        return True
    
    def get_batch_job_statistics(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        获取批量任务统计信息
        
        Args:
            job_id: 任务ID
            
        Returns:
            Optional[Dict]: 统计信息
        """
        batch_job = self.get_batch_job(job_id)
        
        if not batch_job:
            return None
        
        # 计算耗时
        duration = None
        if batch_job.started_at:
            end_time = batch_job.completed_at or datetime.utcnow()
            duration = (end_time - batch_job.started_at).total_seconds()
        
        return {
            'job_id': job_id,
            'status': batch_job.status,
            'total_tasks': batch_job.total_tasks,
            'completed_tasks': batch_job.completed_tasks,
            'failed_tasks': batch_job.failed_tasks,
            'pending_tasks': batch_job.total_tasks - batch_job.completed_tasks - batch_job.failed_tasks,
            'progress': batch_job.progress,
            'duration_seconds': duration,
            'started_at': batch_job.started_at.isoformat() if batch_job.started_at else None,
            'completed_at': batch_job.completed_at.isoformat() if batch_job.completed_at else None,
            'error_message': batch_job.error_message
        }
