"""
数据集管理服务
负责数据集的创建、查询、删除和导出
"""
import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from config import settings
from models.db_models import (
    Dataset, DatasetCorpus, Corpus, AnnotationTask,
    TextEntity, Relation, LabelSchemaVersion
)


class DatasetService:
    """数据集管理服务"""
    
    def __init__(self, db: Session):
        """
        初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create_dataset(
        self,
        name: str,
        description: Optional[str],
        corpus_ids: List[int],
        created_by: int,
        label_schema_version_id: Optional[int] = None
    ) -> Dataset:
        """
        创建数据集
        
        Args:
            name: 数据集名称
            description: 数据集描述
            corpus_ids: 语料ID列表
            created_by: 创建人ID
            label_schema_version_id: 标签体系版本ID（可选，默认使用当前活跃版本）
            
        Returns:
            Dataset: 创建的数据集对象
        """
        # 生成数据集ID
        dataset_id = f"ds-{uuid.uuid4().hex[:12]}"
        
        # 如果未指定标签体系版本，使用当前活跃版本
        if label_schema_version_id is None:
            active_version = self.db.query(LabelSchemaVersion)\
                .filter(LabelSchemaVersion.is_active == True)\
                .first()
            if active_version:
                label_schema_version_id = active_version.id
        
        # 创建数据集
        dataset = Dataset(
            dataset_id=dataset_id,
            name=name,
            description=description,
            created_by=created_by,
            label_schema_version_id=label_schema_version_id
        )
        self.db.add(dataset)
        self.db.flush()  # 获取dataset.id
        
        # 关联语料
        for corpus_id in corpus_ids:
            # 验证语料是否存在
            corpus = self.db.query(Corpus).filter(Corpus.id == corpus_id).first()
            if not corpus:
                raise ValueError(f"语料ID {corpus_id} 不存在")
            
            # 创建关联
            association = DatasetCorpus(
                dataset_id=dataset.id,
                corpus_id=corpus_id
            )
            self.db.add(association)
            
            # 为每个语料创建标注任务
            task_id = f"task-{uuid.uuid4().hex[:12]}"
            task = AnnotationTask(
                task_id=task_id,
                dataset_id=dataset.id,
                corpus_id=corpus_id,
                status='pending'
            )
            self.db.add(task)
        
        self.db.commit()
        self.db.refresh(dataset)
        
        return dataset
    
    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        """
        获取数据集详情
        
        Args:
            dataset_id: 数据集ID
            
        Returns:
            Dataset: 数据集对象，如果不存在返回None
        """
        dataset = self.db.query(Dataset)\
            .filter(Dataset.dataset_id == dataset_id)\
            .first()
        return dataset
    
    def list_datasets(
        self,
        page: int = 1,
        page_size: int = 20,
        name: Optional[str] = None,
        created_by: Optional[int] = None
    ) -> tuple[List[Dataset], int]:
        """
        获取数据集列表
        
        Args:
            page: 页码（从1开始）
            page_size: 每页数量
            name: 数据集名称筛选（可选）
            created_by: 创建人ID（可选，用于筛选）
            
        Returns:
            tuple[List[Dataset], int]: (数据集列表, 总数)
        """
        query = self.db.query(Dataset)
        
        # 筛选条件
        if name is not None:
            query = query.filter(Dataset.name.like(f"%{name}%"))
        
        if created_by is not None:
            query = query.filter(Dataset.created_by == created_by)
        
        # 获取总数
        total = query.count()
        
        # 分页
        skip = (page - 1) * page_size
        datasets = query.order_by(Dataset.created_at.desc())\
            .offset(skip)\
            .limit(page_size)\
            .all()
        
        return datasets, total
    
    def delete_dataset(self, dataset_id: str) -> bool:
        """
        删除数据集（级联删除关联的任务和标注）
        
        Args:
            dataset_id: 数据集ID
            
        Returns:
            bool: 是否删除成功
        """
        dataset = self.db.query(Dataset)\
            .filter(Dataset.dataset_id == dataset_id)\
            .first()
        
        if not dataset:
            return False
        
        # SQLAlchemy会自动级联删除关联的记录（因为设置了cascade="all, delete-orphan"）
        self.db.delete(dataset)
        self.db.commit()
        
        return True

    def add_tasks_to_dataset(
        self,
        dataset_id: str,
        corpus_ids: List[int]
    ) -> Dict[str, int]:
        """
        向已有数据集添加语料并创建标注任务（自动去重）
        
        Args:
            dataset_id: 数据集ID（字符串形式）
            corpus_ids: 要添加的语料ID列表
            
        Returns:
            Dict: {"added": 新增任务数, "skipped": 重复跳过数}
        """
        dataset = self.db.query(Dataset)\
            .filter(Dataset.dataset_id == dataset_id)\
            .first()
        if not dataset:
            raise ValueError(f"数据集 {dataset_id} 不存在")

        # 查询已关联的语料ID集合（用于去重）
        existing_corpus_ids: set = {
            assoc.corpus_id for assoc in dataset.corpus_associations
        }

        added = 0
        skipped = 0
        for corpus_id in corpus_ids:
            if corpus_id in existing_corpus_ids:
                skipped += 1
                continue

            corpus = self.db.query(Corpus).filter(Corpus.id == corpus_id).first()
            if not corpus:
                raise ValueError(f"语料ID {corpus_id} 不存在")

            # 创建关联
            association = DatasetCorpus(
                dataset_id=dataset.id,
                corpus_id=corpus_id
            )
            self.db.add(association)

            # 创建标注任务
            task_id = f"task-{uuid.uuid4().hex[:12]}"
            task = AnnotationTask(
                task_id=task_id,
                dataset_id=dataset.id,
                corpus_id=corpus_id,
                status='pending'
            )
            self.db.add(task)

            existing_corpus_ids.add(corpus_id)
            added += 1

        self.db.commit()
        return {"added": added, "skipped": skipped}

    def remove_task(self, dataset_id: str, task_id: str) -> bool:
        """
        从数据集中删除一个标注任务及其关联语料绑定

        Args:
            dataset_id: 数据集ID（字符串形式）
            task_id: 任务ID（字符串形式，如 task-xxxx）

        Returns:
            bool: 成功则True，任务不存在则False
        """
        dataset = self.db.query(Dataset)\
            .filter(Dataset.dataset_id == dataset_id)\
            .first()
        if not dataset:
            raise ValueError(f"数据集 {dataset_id} 不存在")

        task = self.db.query(AnnotationTask)\
            .filter(
                AnnotationTask.task_id == task_id,
                AnnotationTask.dataset_id == dataset.id
            )\
            .first()

        if not task:
            return False

        corpus_id = task.corpus_id

        # 删除任务（cascade 会自动删除 text_entities / relations / image_entities）
        self.db.delete(task)

        # 删除数据集-语料关联
        assoc = self.db.query(DatasetCorpus)\
            .filter(
                DatasetCorpus.dataset_id == dataset.id,
                DatasetCorpus.corpus_id == corpus_id
            )\
            .first()
        if assoc:
            self.db.delete(assoc)

        self.db.commit()
        return True
    
    def get_dataset_statistics(self, dataset_id: str) -> Dict[str, Any]:
        """
        获取数据集统计信息
        
        Args:
            dataset_id: 数据集ID
            
        Returns:
            Dict: 统计信息
        """
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            raise ValueError(f"数据集 {dataset_id} 不存在")
        
        # 统计任务状态
        task_stats = self.db.query(
            AnnotationTask.status,
            func.count(AnnotationTask.id).label('count')
        ).filter(
            AnnotationTask.dataset_id == dataset.id
        ).group_by(AnnotationTask.status).all()
        
        status_counts = {status: count for status, count in task_stats}
        
        # 统计总数
        total_tasks = sum(status_counts.values())
        completed_tasks = status_counts.get('completed', 0)
        
        # 统计实体和关系数量
        entity_count = self.db.query(func.count(TextEntity.id))\
            .join(AnnotationTask)\
            .filter(AnnotationTask.dataset_id == dataset.id)\
            .scalar() or 0
        
        relation_count = self.db.query(func.count(Relation.id))\
            .join(AnnotationTask)\
            .filter(AnnotationTask.dataset_id == dataset.id)\
            .scalar() or 0
        
        return {
            'dataset_id': dataset_id,
            'name': dataset.name,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks + status_counts.get('completed_with_errors', 0),
            'reviewed_tasks': status_counts.get('reviewed', 0),
            'pending_tasks': status_counts.get('pending', 0),
            'processing_tasks': status_counts.get('processing', 0),
            'failed_tasks': status_counts.get('failed', 0),
            'entity_count': entity_count,
            'relation_count': relation_count,
            'avg_entities_per_task': (entity_count / total_tasks) if total_tasks > 0 else 0,
            'avg_relations_per_task': (relation_count / total_tasks) if total_tasks > 0 else 0,
            'completion_rate': (completed_tasks / total_tasks) if total_tasks > 0 else 0
        }
    
    def export_dataset(
        self,
        dataset_id: str,
        output_path: Optional[str] = None,
        status_filter: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        导出数据集为JSONL格式
        
        Args:
            dataset_id: 数据集ID
            output_path: 导出路径（可选，默认为data/exports目录）
            status_filter: 状态筛选（可选，如['completed', 'reviewed']）
            
        Returns:
            Optional[str]: 导出文件路径，如果数据集不存在返回None
        """
        import os
        from pathlib import Path
        
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            return None
        
        # 查询任务
        query = self.db.query(AnnotationTask)\
            .filter(AnnotationTask.dataset_id == dataset.id)
        
        if status_filter:
            query = query.filter(AnnotationTask.status.in_(status_filter))
        
        tasks = query.all()
        
        # 生成JSONL内容
        lines = []
        for sample_index, task in enumerate(tasks):
            # 获取语料
            corpus = self.db.query(Corpus)\
                .filter(Corpus.id == task.corpus_id)\
                .first()
            
            if not corpus:
                continue
            
            # 获取实体
            entities = self.db.query(TextEntity)\
                .filter(TextEntity.task_id == task.id)\
                .filter(TextEntity.version == task.current_version)\
                .all()
            
            # 获取关系
            relations = self.db.query(Relation)\
                .filter(Relation.task_id == task.id)\
                .filter(Relation.version == task.current_version)\
                .all()

            # 仅导出文本实体与文本关系
            sorted_entities = sorted(
                entities,
                key=lambda e: (e.start_offset, e.end_offset, e.token or "", e.label or "")
            )

            entity_id_map = {
                entity.entity_id: idx for idx, entity in enumerate(sorted_entities)
            }

            export_entities = []
            for idx, entity in enumerate(sorted_entities):
                export_entities.append({
                    'id': idx,
                    'start_offset': entity.start_offset,
                    'end_offset': entity.end_offset,
                    'label': entity.label,
                    'text': entity.token
                })

            export_relations = []
            for relation in relations:
                if relation.from_entity_id not in entity_id_map:
                    continue
                if relation.to_entity_id not in entity_id_map:
                    continue

                export_relations.append({
                    'id': len(export_relations),
                    'from_id': entity_id_map[relation.from_entity_id],
                    'to_id': entity_id_map[relation.to_entity_id],
                    'type': relation.relation_type
                })

            quick_response_id = self._extract_quick_response_id(corpus)
            sample_id = f"entity_text_{quick_response_id}_{sample_index:03d}"

            # 构建文本导出记录
            record = {
                'sample_id': sample_id,
                'quick_response_id': quick_response_id,
                'data_source': self._build_data_source(corpus),
                'text': corpus.text,
                'entities': export_entities,
                'relations': export_relations
            }
            
            lines.append(json.dumps(record, ensure_ascii=False))
        
        # 确定输出路径
        if output_path is None:
            output_path = str(settings.EXPORT_DIR / f"{dataset_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")
        else:
            # 确保目录存在
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return output_path

    @staticmethod
    def _extract_quick_response_id(corpus: Corpus) -> str:
        """从语料中提取快反编号，提取失败时回退到text_id。"""
        text_id = (corpus.text_id or "").strip()
        if text_id:
            fr_match = re.search(r"FR\d+", text_id, re.IGNORECASE)
            if fr_match:
                return fr_match.group(0).upper()
            return text_id

        return f"CORPUS_{corpus.id}"

    @staticmethod
    def _build_data_source(corpus: Corpus) -> str:
        """优先使用来源文件名+行号构建数据来源标识。"""
        source_file = (corpus.source_file or "").strip()
        source_field = (corpus.source_field or "").strip()

        if source_file:
            from pathlib import Path
            file_stem = Path(source_file).stem or source_file
            if corpus.source_row is not None:
                return f"{file_stem}_{corpus.source_row}"
            return file_stem

        if source_field:
            if corpus.source_row is not None:
                return f"{source_field}_{corpus.source_row}"
            return source_field

        if corpus.source_row is not None:
            return f"row_{corpus.source_row}"

        return "unknown"
