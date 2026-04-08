"""
数据序列化服务（简化版）
提供标注数据的序列化和反序列化功能
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from models.db_models import (
    TextEntity,
    ImageEntity,
    Relation,
    AnnotationTask
)


class SerializationService:
    """数据序列化服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ========================================================================
    # 文本实体序列化
    # ========================================================================
    
    @staticmethod
    def serialize_text_entity(entity: TextEntity) -> Dict[str, Any]:
        """
        序列化文本实体
        
        Args:
            entity: 文本实体对象
        
        Returns:
            Dict: 序列化后的字典，包含id、start_offset、end_offset、label字段
        """
        return {
            "id": entity.id,
            "start_offset": entity.start_offset,
            "end_offset": entity.end_offset,
            "label": entity.label,
            "token": entity.token  # 额外包含token字段便于调试
        }
    
    @staticmethod
    def deserialize_text_entity(data: Dict[str, Any], task_id: int, entity_id: int = 0, version: int = 1) -> TextEntity:
        """
        反序列化文本实体
        
        Args:
            data: 序列化的字典数据
            task_id: 关联的任务ID（整数）
            entity_id: 实体在任务内的ID
            version: 版本号
        
        Returns:
            TextEntity: 文本实体对象
        """
        return TextEntity(
            task_id=task_id,
            entity_id=entity_id,
            version=version,
            token=data.get("token", ""),
            label=data["label"],
            start_offset=data["start_offset"],
            end_offset=data["end_offset"]
        )
    
    # ========================================================================
    # 图片实体序列化
    # ========================================================================
    
    @staticmethod
    def serialize_image_entity(entity: ImageEntity) -> Dict[str, Any]:
        """
        序列化图片实体（支持整图和区域）
        
        Args:
            entity: 图片实体对象
        
        Returns:
            Dict: 序列化后的字典
            - 整图实体: id, image_path, label, bbox=null
            - 区域实体: id, image_path, label, bbox={x, y, width, height}
        """
        result = {
            "id": entity.id,
            "image_path": entity.image_id,  # 使用image_id作为路径标识
            "label": entity.label
        }
        
        # 处理边界框
        if entity.bbox_x is not None and entity.bbox_y is not None:
            # 区域实体
            result["bbox"] = {
                "x": entity.bbox_x,
                "y": entity.bbox_y,
                "width": entity.bbox_width,
                "height": entity.bbox_height
            }
        else:
            # 整图实体
            result["bbox"] = None
        
        return result
    
    @staticmethod
    def deserialize_image_entity(data: Dict[str, Any], task_id: int, entity_id: int = 0, version: int = 1) -> ImageEntity:
        """
        反序列化图片实体
        
        Args:
            data: 序列化的字典数据
            task_id: 关联的任务ID（整数）
            entity_id: 实体在任务内的ID
            version: 版本号
        
        Returns:
            ImageEntity: 图片实体对象
        """
        bbox = data.get("bbox")
        
        # 注意：image_id 在数据库中是整数外键，这里简化处理
        # 实际使用时需要先查找或创建对应的 Image 记录
        return ImageEntity(
            task_id=task_id,
            entity_id=entity_id,
            version=version,
            image_id=1,  # 简化：使用固定值，实际应该查找对应的图片ID
            label=data["label"],
            bbox_x=bbox["x"] if bbox else None,
            bbox_y=bbox["y"] if bbox else None,
            bbox_width=bbox["width"] if bbox else None,
            bbox_height=bbox["height"] if bbox else None
        )
    
    # ========================================================================
    # 关系序列化
    # ========================================================================
    
    @staticmethod
    def serialize_relation(relation: Relation) -> Dict[str, Any]:
        """
        序列化关系
        
        Args:
            relation: 关系对象
        
        Returns:
            Dict: 序列化后的字典，包含from_id、to_id、type字段
        """
        return {
            "from_id": relation.from_entity_id,
            "to_id": relation.to_entity_id,
            "type": relation.relation_type
        }
    
    @staticmethod
    def deserialize_relation(data: Dict[str, Any], task_id: int, relation_id: int = 0, version: int = 1) -> Relation:
        """
        反序列化关系
        
        Args:
            data: 序列化的字典数据
            task_id: 关联的任务ID（整数）
            relation_id: 关系在任务内的ID
            version: 版本号
        
        Returns:
            Relation: 关系对象
        """
        return Relation(
            task_id=task_id,
            relation_id=relation_id,
            version=version,
            from_entity_id=data["from_id"],
            to_entity_id=data["to_id"],
            relation_type=data.get("type", "relates_to")
        )
    
    # ========================================================================
    # 完整标注任务序列化
    # ========================================================================
    
    def serialize_annotation_task(
        self,
        task: AnnotationTask,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        序列化完整的标注任务
        
        Args:
            task: 标注任务对象
            include_metadata: 是否包含元数据（任务ID、状态等）
        
        Returns:
            Dict: 序列化后的完整数据
        """
        # 获取语料信息
        from models.db_models import Corpus
        corpus = self.db.query(Corpus).filter(
            Corpus.id == task.corpus_id
        ).first()
        
        # 获取所有实体和关系
        text_entities = self.db.query(TextEntity).filter(
            TextEntity.task_id == task.id
        ).all()
        
        image_entities = self.db.query(ImageEntity).filter(
            ImageEntity.task_id == task.id
        ).all()
        
        relations = self.db.query(Relation).filter(
            Relation.task_id == task.id
        ).all()
        
        # 序列化数据
        result = {
            "text": corpus.text if corpus else "",
            "text_type": corpus.text_type if corpus else None,
            "entities": [self.serialize_text_entity(e) for e in text_entities],
            "images": [self.serialize_image_entity(e) for e in image_entities],
            "relations": [self.serialize_relation(r) for r in relations]
        }
        
        # 可选的元数据
        if include_metadata:
            result["task_id"] = task.task_id
            result["status"] = task.status
            result["annotation_type"] = task.annotation_type
            result["current_version"] = task.current_version
        
        return result
    
    def deserialize_annotation_task(
        self,
        data: Dict[str, Any],
        task_id: int,
        create_entities: bool = True
    ) -> Dict[str, List[Any]]:
        """
        反序列化标注任务数据
        
        Args:
            data: 序列化的字典数据
            task_id: 任务ID（整数）
            create_entities: 是否创建实体和关系对象（否则只返回数据）
        
        Returns:
            Dict: 包含entities、images、relations列表的字典
        """
        result = {
            "text_entities": [],
            "image_entities": [],
            "relations": []
        }
        
        if not create_entities:
            # 只返回原始数据
            result["text_entities"] = data.get("entities", [])
            result["image_entities"] = data.get("images", [])
            result["relations"] = data.get("relations", [])
            return result
        
        # 创建实体对象
        for idx, entity_data in enumerate(data.get("entities", [])):
            entity = self.deserialize_text_entity(entity_data, task_id, entity_id=idx)
            result["text_entities"].append(entity)
        
        for idx, image_data in enumerate(data.get("images", [])):
            entity = self.deserialize_image_entity(image_data, task_id, entity_id=idx)
            result["image_entities"].append(entity)
        
        for idx, relation_data in enumerate(data.get("relations", [])):
            relation = self.deserialize_relation(relation_data, task_id, relation_id=idx)
            result["relations"].append(relation)
        
        return result
    
    # ========================================================================
    # 批量序列化
    # ========================================================================
    
    def serialize_multiple_tasks(
        self,
        task_ids: List[str],
        include_metadata: bool = False
    ) -> List[Dict[str, Any]]:
        """
        批量序列化多个标注任务
        
        Args:
            task_ids: 任务ID列表
            include_metadata: 是否包含元数据
        
        Returns:
            List[Dict]: 序列化后的任务列表
        """
        tasks = self.db.query(AnnotationTask).filter(
            AnnotationTask.task_id.in_(task_ids)
        ).all()
        
        return [
            self.serialize_annotation_task(task, include_metadata)
            for task in tasks
        ]
    
    # ========================================================================
    # 工具方法
    # ========================================================================
    
    @staticmethod
    def validate_serialized_data(data: Dict[str, Any]) -> bool:
        """
        验证序列化数据的格式是否正确
        
        Args:
            data: 序列化的数据
        
        Returns:
            bool: 数据格式是否有效
        """
        # 检查必需字段
        required_fields = ["text", "entities", "relations"]
        for field in required_fields:
            if field not in data:
                return False
        
        # 验证实体格式
        for entity in data.get("entities", []):
            if not all(k in entity for k in ["id", "start_offset", "end_offset", "label"]):
                return False
        
        # 验证图片实体格式
        for image in data.get("images", []):
            if not all(k in image for k in ["id", "image_path", "label", "bbox"]):
                return False
        
        # 验证关系格式
        for relation in data.get("relations", []):
            if not all(k in relation for k in ["from_id", "to_id", "type"]):
                return False
        
        return True
