"""
标签管理服务
提供标签体系的CRUD、导入导出、版本管理等功能
"""
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.db_models import (
    EntityType, RelationType, LabelSchemaVersion, Dataset
)
from services.label_config_cache import LabelConfigCache


class LabelManagementService:
    """标签管理服务"""
    
    def __init__(self, db: Session):
        """
        初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    # ========================================================================
    # 实体类型管理
    # ========================================================================
    
    def create_entity_type(
        self,
        type_name: str,
        type_name_zh: str,
        color: str,
        description: Optional[str] = None,
        supports_bbox: bool = False
    ) -> EntityType:
        """
        创建实体类型
        
        Args:
            type_name: 类型名称(英文)
            type_name_zh: 类型名称(中文)
            color: 颜色代码
            description: 描述
            supports_bbox: 是否支持边界框
            
        Returns:
            EntityType: 创建的实体类型
        """
        entity_type = EntityType(
            type_name=type_name,
            type_name_zh=type_name_zh,
            color=color,
            description=description,
            supports_bbox=supports_bbox,
            is_active=True,
            is_reviewed=False  # 新创建的标签默认未审核
        )
        
        self.db.add(entity_type)
        self.db.commit()
        self.db.refresh(entity_type)
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return entity_type
    
    def update_entity_type(
        self,
        entity_type_id: int,
        **kwargs
    ) -> Optional[EntityType]:
        """
        更新实体类型
        
        Args:
            entity_type_id: 实体类型ID
            **kwargs: 要更新的字段
            
        Returns:
            Optional[EntityType]: 更新后的实体类型
        """
        entity_type = self.db.query(EntityType).filter(EntityType.id == entity_type_id).first()
        
        if not entity_type:
            return None
        
        # 更新字段
        for key, value in kwargs.items():
            if hasattr(entity_type, key):
                setattr(entity_type, key, value)
        
        # 更新时间戳
        entity_type.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(entity_type)
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return entity_type
    
    def delete_entity_type(self, entity_type_id: int) -> bool:
        """
        删除实体类型(软删除,设置为不活跃)
        
        Args:
            entity_type_id: 实体类型ID
            
        Returns:
            bool: 是否删除成功
        """
        entity_type = self.db.query(EntityType).filter(EntityType.id == entity_type_id).first()
        
        if not entity_type:
            return False
        
        # 软删除
        entity_type.is_active = False
        entity_type.updated_at = datetime.utcnow()
        
        self.db.commit()
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return True
    
    def get_entity_type(self, entity_type_id: int) -> Optional[EntityType]:
        """
        获取实体类型详情
        
        Args:
            entity_type_id: 实体类型ID
            
        Returns:
            Optional[EntityType]: 实体类型对象
        """
        return self.db.query(EntityType).filter(EntityType.id == entity_type_id).first()
    
    def list_entity_types(
        self,
        include_inactive: bool = False,
        include_unreviewed: bool = True
    ) -> List[EntityType]:
        """
        获取实体类型列表
        
        Args:
            include_inactive: 是否包含不活跃的类型
            include_unreviewed: 是否包含未审核的类型
            
        Returns:
            List[EntityType]: 实体类型列表
        """
        query = self.db.query(EntityType)
        
        if not include_inactive:
            query = query.filter(EntityType.is_active == True)
        
        if not include_unreviewed:
            query = query.filter(EntityType.is_reviewed == True)
        
        return query.order_by(EntityType.id).all()
    
    # ========================================================================
    # 关系类型管理
    # ========================================================================
    
    def create_relation_type(
        self,
        type_name: str,
        type_name_zh: str,
        color: str,
        description: Optional[str] = None
    ) -> RelationType:
        """
        创建关系类型
        
        Args:
            type_name: 类型名称(英文)
            type_name_zh: 类型名称(中文)
            color: 颜色代码
            description: 描述
            
        Returns:
            RelationType: 创建的关系类型
        """
        relation_type = RelationType(
            type_name=type_name,
            type_name_zh=type_name_zh,
            color=color,
            description=description,
            is_active=True,
            is_reviewed=False  # 新创建的标签默认未审核
        )
        
        self.db.add(relation_type)
        self.db.commit()
        self.db.refresh(relation_type)
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return relation_type
    
    def update_relation_type(
        self,
        relation_type_id: int,
        **kwargs
    ) -> Optional[RelationType]:
        """
        更新关系类型
        
        Args:
            relation_type_id: 关系类型ID
            **kwargs: 要更新的字段
            
        Returns:
            Optional[RelationType]: 更新后的关系类型
        """
        relation_type = self.db.query(RelationType).filter(RelationType.id == relation_type_id).first()
        
        if not relation_type:
            return None
        
        # 更新字段
        for key, value in kwargs.items():
            if hasattr(relation_type, key):
                setattr(relation_type, key, value)
        
        # 更新时间戳
        relation_type.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(relation_type)
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return relation_type
    
    def delete_relation_type(self, relation_type_id: int) -> bool:
        """
        删除关系类型(软删除,设置为不活跃)
        
        Args:
            relation_type_id: 关系类型ID
            
        Returns:
            bool: 是否删除成功
        """
        relation_type = self.db.query(RelationType).filter(RelationType.id == relation_type_id).first()
        
        if not relation_type:
            return False
        
        # 软删除
        relation_type.is_active = False
        relation_type.updated_at = datetime.utcnow()
        
        self.db.commit()
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return True
    
    def get_relation_type(self, relation_type_id: int) -> Optional[RelationType]:
        """
        获取关系类型详情
        
        Args:
            relation_type_id: 关系类型ID
            
        Returns:
            Optional[RelationType]: 关系类型对象
        """
        return self.db.query(RelationType).filter(RelationType.id == relation_type_id).first()
    
    def list_relation_types(
        self,
        include_inactive: bool = False,
        include_unreviewed: bool = True
    ) -> List[RelationType]:
        """
        获取关系类型列表
        
        Args:
            include_inactive: 是否包含不活跃的类型
            include_unreviewed: 是否包含未审核的类型
            
        Returns:
            List[RelationType]: 关系类型列表
        """
        query = self.db.query(RelationType)
        
        if not include_inactive:
            query = query.filter(RelationType.is_active == True)
        
        if not include_unreviewed:
            query = query.filter(RelationType.is_reviewed == True)
        
        return query.order_by(RelationType.id).all()
    
    # ========================================================================
    # 标签定义审核
    # ========================================================================
    
    def review_entity_type(
        self,
        entity_type_id: int,
        reviewed_by: int,
        definition: Optional[str] = None,
        examples: Optional[List[str]] = None,
        disambiguation: Optional[str] = None
    ) -> Optional[EntityType]:
        """
        审核实体类型定义
        
        Args:
            entity_type_id: 实体类型ID
            reviewed_by: 审核人ID
            definition: 定义(可选,用户可能编辑)
            examples: 示例列表(可选,用户可能编辑)
            disambiguation: 类别辨析(可选,用户可能编辑)
            
        Returns:
            Optional[EntityType]: 审核后的实体类型
        """
        entity_type = self.db.query(EntityType).filter(EntityType.id == entity_type_id).first()
        
        if not entity_type:
            return None
        
        # 更新定义(如果提供)
        if definition is not None:
            entity_type.definition = definition
        if examples is not None:
            entity_type.examples = json.dumps(examples, ensure_ascii=False)
        if disambiguation is not None:
            entity_type.disambiguation = disambiguation
        
        # 标记为已审核
        entity_type.is_reviewed = True
        entity_type.reviewed_by = reviewed_by
        entity_type.reviewed_at = datetime.utcnow()
        entity_type.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(entity_type)
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return entity_type
    
    def review_relation_type(
        self,
        relation_type_id: int,
        reviewed_by: int,
        definition: Optional[str] = None,
        direction_rule: Optional[str] = None,
        examples: Optional[List[str]] = None,
        disambiguation: Optional[str] = None
    ) -> Optional[RelationType]:
        """
        审核关系类型定义
        
        Args:
            relation_type_id: 关系类型ID
            reviewed_by: 审核人ID
            definition: 定义(可选,用户可能编辑)
            direction_rule: 方向规则(可选,用户可能编辑)
            examples: 示例列表(可选,用户可能编辑)
            disambiguation: 类别辨析(可选,用户可能编辑)
            
        Returns:
            Optional[RelationType]: 审核后的关系类型
        """
        relation_type = self.db.query(RelationType).filter(RelationType.id == relation_type_id).first()
        
        if not relation_type:
            return None
        
        # 更新定义(如果提供)
        if definition is not None:
            relation_type.definition = definition
        if direction_rule is not None:
            relation_type.direction_rule = direction_rule
        if examples is not None:
            relation_type.examples = json.dumps(examples, ensure_ascii=False)
        if disambiguation is not None:
            relation_type.disambiguation = disambiguation
        
        # 标记为已审核
        relation_type.is_reviewed = True
        relation_type.reviewed_by = reviewed_by
        relation_type.reviewed_at = datetime.utcnow()
        relation_type.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(relation_type)
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return relation_type
    
    # ========================================================================
    # 标签配置导入导出
    # ========================================================================
    
    def export_label_schema(self) -> Dict[str, Any]:
        """
        导出标签配置
        
        Returns:
            Dict: 标签配置JSON
        """
        entity_types = self.list_entity_types(include_inactive=False, include_unreviewed=True)
        relation_types = self.list_relation_types(include_inactive=False, include_unreviewed=True)
        
        return {
            'entity_types': [
                {
                    'type_name': et.type_name,
                    'type_name_zh': et.type_name_zh,
                    'color': et.color,
                    'description': et.description,
                    'definition': et.definition,
                    'examples': json.loads(et.examples) if et.examples else [],
                    'disambiguation': et.disambiguation,
                    'supports_bbox': et.supports_bbox,
                    'is_reviewed': et.is_reviewed
                }
                for et in entity_types
            ],
            'relation_types': [
                {
                    'type_name': rt.type_name,
                    'type_name_zh': rt.type_name_zh,
                    'color': rt.color,
                    'description': rt.description,
                    'definition': rt.definition,
                    'direction_rule': rt.direction_rule,
                    'examples': json.loads(rt.examples) if rt.examples else [],
                    'disambiguation': rt.disambiguation,
                    'is_reviewed': rt.is_reviewed
                }
                for rt in relation_types
            ],
            'metadata': {
                'exported_at': datetime.utcnow().isoformat(),
                'total_entity_types': len(entity_types),
                'total_relation_types': len(relation_types)
            }
        }
    
    def import_label_schema(
        self,
        schema_data: Dict[str, Any],
        merge: bool = False
    ) -> Dict[str, int]:
        """
        导入标签配置
        
        Args:
            schema_data: 标签配置JSON
            merge: 是否合并(True=合并, False=替换)
            
        Returns:
            Dict: 导入统计信息
        """
        stats = {
            'entity_types_created': 0,
            'entity_types_updated': 0,
            'relation_types_created': 0,
            'relation_types_updated': 0
        }
        
        # 如果不是合并模式,先禁用所有现有标签
        if not merge:
            self.db.query(EntityType).update({'is_active': False})
            self.db.query(RelationType).update({'is_active': False})
        
        # 导入实体类型
        for et_data in schema_data.get('entity_types', []):
            existing = self.db.query(EntityType).filter(
                EntityType.type_name == et_data['type_name']
            ).first()
            
            if existing:
                # 更新现有标签
                for key, value in et_data.items():
                    if key == 'examples' and isinstance(value, list):
                        value = json.dumps(value, ensure_ascii=False)
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.is_active = True
                existing.updated_at = datetime.utcnow()
                stats['entity_types_updated'] += 1
            else:
                # 创建新标签
                examples = et_data.get('examples', [])
                if isinstance(examples, list):
                    examples = json.dumps(examples, ensure_ascii=False)
                
                new_et = EntityType(
                    type_name=et_data['type_name'],
                    type_name_zh=et_data['type_name_zh'],
                    color=et_data['color'],
                    description=et_data.get('description'),
                    definition=et_data.get('definition'),
                    examples=examples,
                    disambiguation=et_data.get('disambiguation'),
                    supports_bbox=et_data.get('supports_bbox', False),
                    is_active=True,
                    is_reviewed=et_data.get('is_reviewed', False)
                )
                self.db.add(new_et)
                stats['entity_types_created'] += 1
        
        # 导入关系类型
        for rt_data in schema_data.get('relation_types', []):
            existing = self.db.query(RelationType).filter(
                RelationType.type_name == rt_data['type_name']
            ).first()
            
            if existing:
                # 更新现有标签
                for key, value in rt_data.items():
                    if key == 'examples' and isinstance(value, list):
                        value = json.dumps(value, ensure_ascii=False)
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.is_active = True
                existing.updated_at = datetime.utcnow()
                stats['relation_types_updated'] += 1
            else:
                # 创建新标签
                examples = rt_data.get('examples', [])
                if isinstance(examples, list):
                    examples = json.dumps(examples, ensure_ascii=False)
                
                new_rt = RelationType(
                    type_name=rt_data['type_name'],
                    type_name_zh=rt_data['type_name_zh'],
                    color=rt_data['color'],
                    description=rt_data.get('description'),
                    definition=rt_data.get('definition'),
                    direction_rule=rt_data.get('direction_rule'),
                    examples=examples,
                    disambiguation=rt_data.get('disambiguation'),
                    is_active=True,
                    is_reviewed=rt_data.get('is_reviewed', False)
                )
                self.db.add(new_rt)
                stats['relation_types_created'] += 1
        
        self.db.commit()
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return stats
    
    # ========================================================================
    # 版本管理
    # ========================================================================
    
    def create_version_snapshot(
        self,
        version_name: str,
        description: Optional[str],
        created_by: int
    ) -> LabelSchemaVersion:
        """
        创建标签体系版本快照
        
        Args:
            version_name: 版本名称
            description: 版本说明
            created_by: 创建人ID
            
        Returns:
            LabelSchemaVersion: 创建的版本对象
        """
        # 生成版本ID
        version_id = f"schema-{uuid.uuid4().hex[:12]}"
        
        # 导出当前配置
        schema_data = self.export_label_schema()
        
        # 创建版本记录
        version = LabelSchemaVersion(
            version_id=version_id,
            version_name=version_name,
            description=description,
            schema_data=json.dumps(schema_data, ensure_ascii=False),
            is_active=False,  # 新创建的版本默认不活跃
            created_by=created_by
        )
        
        self.db.add(version)
        self.db.commit()
        self.db.refresh(version)
        
        return version
    
    def list_versions(self) -> List[LabelSchemaVersion]:
        """
        获取版本列表
        
        Returns:
            List[LabelSchemaVersion]: 版本列表
        """
        return self.db.query(LabelSchemaVersion)\
            .order_by(LabelSchemaVersion.created_at.desc())\
            .all()
    
    def get_version(self, version_id: str) -> Optional[LabelSchemaVersion]:
        """
        获取版本详情
        
        Args:
            version_id: 版本ID
            
        Returns:
            Optional[LabelSchemaVersion]: 版本对象
        """
        return self.db.query(LabelSchemaVersion)\
            .filter(LabelSchemaVersion.version_id == version_id)\
            .first()
    
    def activate_version(self, version_id: str) -> Optional[LabelSchemaVersion]:
        """
        激活版本
        
        Args:
            version_id: 版本ID
            
        Returns:
            Optional[LabelSchemaVersion]: 激活的版本对象
        """
        version = self.get_version(version_id)
        
        if not version:
            return None
        
        # 取消其他版本的活跃状态
        self.db.query(LabelSchemaVersion).update({'is_active': False})
        
        # 激活当前版本
        version.is_active = True
        
        self.db.commit()
        self.db.refresh(version)
        
        # 清空缓存
        LabelConfigCache.invalidate_cache()
        
        return version
    
    def get_active_version(self) -> Optional[LabelSchemaVersion]:
        """
        获取当前活跃版本
        
        Returns:
            Optional[LabelSchemaVersion]: 活跃版本对象
        """
        return self.db.query(LabelSchemaVersion)\
            .filter(LabelSchemaVersion.is_active == True)\
            .first()
