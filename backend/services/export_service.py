"""
数据导出服务
实现标注数据的导出功能
"""
import json
import random
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.db_models import (
    Dataset, AnnotationTask, TextEntity, ImageEntity, Relation,
    Corpus, Image
)


class ExportService:
    """数据导出服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def export_dataset(
        self,
        dataset_id: int,
        status_filter: Optional[List[str]] = None,
        text_type_filter: Optional[List[str]] = None,
        train_test_split: Optional[float] = None,
        random_seed: int = 42
    ) -> Dict[str, Any]:
        """
        导出数据集为JSONL格式
        
        Args:
            dataset_id: 数据集ID
            status_filter: 状态筛选列表（如['approved', 'completed']）
            text_type_filter: 句子分类筛选列表
            train_test_split: 训练集比例（0-1之间），如0.8表示80%训练集，20%测试集
            random_seed: 随机种子
        
        Returns:
            Dict: 包含导出数据的字典
                - train_data: 训练集数据（如果指定了split）
                - test_data: 测试集数据（如果指定了split）
                - all_data: 所有数据（如果未指定split）
                - total_count: 总记录数
                - train_count: 训练集记录数
                - test_count: 测试集记录数
        """
        # 查询数据集
        dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError(f"数据集不存在: {dataset_id}")
        
        # 查询标注任务
        query = self.db.query(AnnotationTask).filter(
            AnnotationTask.dataset_id == dataset_id
        )
        
        # 状态筛选
        if status_filter:
            query = query.filter(AnnotationTask.status.in_(status_filter))
        
        tasks = query.all()
        
        # 构建导出数据
        export_records = []
        
        for task in tasks:
            # 查询语料
            corpus = self.db.query(Corpus).filter(
                Corpus.id == task.corpus_id
            ).first()
            
            if not corpus:
                continue
            
            # 句子分类筛选
            if text_type_filter and corpus.text_type not in text_type_filter:
                continue
            
            # 查询当前版本的实体和关系
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
            
            # 构建记录
            record = self._build_export_record(
                corpus, text_entities, image_entities, relations
            )
            
            export_records.append(record)
        
        # 训练集/测试集划分
        if train_test_split is not None:
            if not 0 < train_test_split < 1:
                raise ValueError("train_test_split必须在0和1之间")
            
            # 设置随机种子
            random.seed(random_seed)
            
            # 随机打乱
            random.shuffle(export_records)
            
            # 划分
            split_index = int(len(export_records) * train_test_split)
            train_data = export_records[:split_index]
            test_data = export_records[split_index:]
            
            return {
                "train_data": train_data,
                "test_data": test_data,
                "total_count": len(export_records),
                "train_count": len(train_data),
                "test_count": len(test_data)
            }
        else:
            return {
                "all_data": export_records,
                "total_count": len(export_records)
            }
    
    def _build_export_record(
        self,
        corpus: Corpus,
        text_entities: List[TextEntity],
        image_entities: List[ImageEntity],
        relations: List[Relation]
    ) -> Dict[str, Any]:
        """
        构建单条导出记录
        
        Args:
            corpus: 语料记录
            text_entities: 文本实体列表
            image_entities: 图片实体列表
            relations: 关系列表
        
        Returns:
            Dict: 导出记录
        """
        # 构建文本实体
        entities = []
        for entity in text_entities:
            entities.append({
                "id": entity.entity_id,
                "start_offset": entity.start_offset,
                "end_offset": entity.end_offset,
                "label": entity.label
            })
        
        # 构建关系（仅文本实体之间的关系）
        text_entity_ids = {e.entity_id for e in text_entities}
        text_relations = []
        
        for relation in relations:
            # 只包含文本实体之间的关系
            if (relation.from_entity_id in text_entity_ids and 
                relation.to_entity_id in text_entity_ids):
                text_relations.append({
                    "from_id": relation.from_entity_id,
                    "to_id": relation.to_entity_id,
                    "type": relation.relation_type
                })
        
        # 构建图片实体
        images = []
        image_entity_map = {}  # 映射图片实体ID到新ID
        
        for idx, img_entity in enumerate(image_entities):
            # 查询图片信息
            image = self.db.query(Image).filter(
                Image.id == img_entity.image_id
            ).first()
            
            if not image:
                continue
            
            # 生成新的图片实体ID（从100开始，避免与文本实体ID冲突）
            new_id = 100 + idx
            image_entity_map[img_entity.entity_id] = new_id
            
            # 构建边界框
            bbox = None
            if img_entity.bbox_x is not None:
                bbox = {
                    "x": img_entity.bbox_x,
                    "y": img_entity.bbox_y,
                    "width": img_entity.bbox_width,
                    "height": img_entity.bbox_height
                }
            
            images.append({
                "id": new_id,
                "image_path": image.file_path,
                "label": img_entity.label,
                "bbox": bbox
            })
        
        # 构建图片关系（文本实体到图片实体的关系）
        image_entity_ids = {e.entity_id for e in image_entities}
        image_relations = []
        
        for relation in relations:
            # 文本实体 -> 图片实体
            if (relation.from_entity_id in text_entity_ids and 
                relation.to_entity_id in image_entity_ids):
                image_relations.append({
                    "from_id": relation.from_entity_id,
                    "to_id": image_entity_map[relation.to_entity_id],
                    "type": relation.relation_type
                })
            # 图片实体 -> 文本实体
            elif (relation.from_entity_id in image_entity_ids and 
                  relation.to_entity_id in text_entity_ids):
                image_relations.append({
                    "from_id": image_entity_map[relation.from_entity_id],
                    "to_id": relation.to_entity_id,
                    "type": relation.relation_type
                })
        
        # 构建完整记录
        record = {
            "text": corpus.text,
            "text_type": corpus.text_type,
            "entities": entities,
            "relations": text_relations,
            "images": images,
            "image_relations": image_relations
        }
        
        return record
    
    def export_to_jsonl(
        self,
        data: List[Dict[str, Any]],
        output_path: str
    ) -> None:
        """
        将数据导出为JSONL文件
        
        Args:
            data: 导出数据列表
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for record in data:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def get_export_statistics(
        self,
        dataset_id: int,
        status_filter: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        获取导出统计信息
        
        Args:
            dataset_id: 数据集ID
            status_filter: 状态筛选列表
        
        Returns:
            Dict: 统计信息
        """
        # 查询标注任务
        query = self.db.query(AnnotationTask).filter(
            AnnotationTask.dataset_id == dataset_id
        )
        
        if status_filter:
            query = query.filter(AnnotationTask.status.in_(status_filter))
        
        tasks = query.all()
        
        # 统计
        total_tasks = len(tasks)
        total_entities = 0
        total_relations = 0
        total_images = 0
        text_type_distribution = {}
        
        for task in tasks:
            # 统计实体
            entity_count = self.db.query(TextEntity).filter(
                and_(
                    TextEntity.task_id == task.id,
                    TextEntity.version == task.current_version
                )
            ).count()
            total_entities += entity_count
            
            # 统计关系
            relation_count = self.db.query(Relation).filter(
                and_(
                    Relation.task_id == task.id,
                    Relation.version == task.current_version
                )
            ).count()
            total_relations += relation_count
            
            # 统计图片
            image_count = self.db.query(ImageEntity).filter(
                and_(
                    ImageEntity.task_id == task.id,
                    ImageEntity.version == task.current_version
                )
            ).count()
            total_images += image_count
            
            # 统计句子分类分布
            corpus = self.db.query(Corpus).filter(
                Corpus.id == task.corpus_id
            ).first()
            
            if corpus and corpus.text_type:
                text_type_distribution[corpus.text_type] = \
                    text_type_distribution.get(corpus.text_type, 0) + 1
        
        return {
            "total_tasks": total_tasks,
            "total_entities": total_entities,
            "total_relations": total_relations,
            "total_images": total_images,
            "average_entities_per_task": total_entities / total_tasks if total_tasks > 0 else 0,
            "average_relations_per_task": total_relations / total_tasks if total_tasks > 0 else 0,
            "text_type_distribution": text_type_distribution
        }
