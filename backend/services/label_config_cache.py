"""
标签配置缓存服务
提供标签配置的缓存机制,减少数据库查询
"""
import threading
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.db_models import EntityType, RelationType


class LabelConfigCache:
    """
    标签配置缓存
    
    使用版本号机制检测配置变化,自动失效缓存
    线程安全的单例模式
    """
    
    _entity_types_cache: Optional[List[EntityType]] = None
    _relation_types_cache: Optional[List[RelationType]] = None
    _cache_version: int = 0
    _cache_lock = threading.Lock()
    
    @classmethod
    def get_entity_types(cls, db_session: Session, version_id: Optional[int] = None) -> List[EntityType]:
        """
        获取实体类型配置(带缓存)
        
        Args:
            db_session: 数据库会话
            version_id: 标签体系版本ID(可选,默认使用活跃版本)
            
        Returns:
            List[EntityType]: 实体类型列表
        """
        with cls._cache_lock:
            current_version = cls._get_config_version(db_session)
            
            # 检查缓存是否有效
            if current_version != cls._cache_version or cls._entity_types_cache is None:
                # 重新加载配置
                active_query = db_session.query(EntityType).filter(EntityType.is_active == True)

                # 优先使用已审核标签；若为空则回退到全部活跃标签（便于当前阶段直接投入使用）
                reviewed_items = active_query.filter(EntityType.is_reviewed == True).order_by(EntityType.id).all()
                if reviewed_items:
                    items = reviewed_items
                else:
                    items = active_query.order_by(EntityType.id).all()
                # 将对象从Session解绑，避免跨Session/commit后的DetachedInstanceError
                for item in items:
                    db_session.expunge(item)
                cls._entity_types_cache = items
                cls._cache_version = current_version
            
            return cls._entity_types_cache
    
    @classmethod
    def get_relation_types(cls, db_session: Session, version_id: Optional[int] = None) -> List[RelationType]:
        """
        获取关系类型配置(带缓存)
        
        Args:
            db_session: 数据库会话
            version_id: 标签体系版本ID(可选,默认使用活跃版本)
            
        Returns:
            List[RelationType]: 关系类型列表
        """
        with cls._cache_lock:
            current_version = cls._get_config_version(db_session)
            
            # 检查缓存是否有效
            if current_version != cls._cache_version or cls._relation_types_cache is None:
                # 重新加载配置
                active_query = db_session.query(RelationType).filter(RelationType.is_active == True)

                # 优先使用已审核标签；若为空则回退到全部活跃标签（便于当前阶段直接投入使用）
                reviewed_items = active_query.filter(RelationType.is_reviewed == True).order_by(RelationType.id).all()
                if reviewed_items:
                    items = reviewed_items
                else:
                    items = active_query.order_by(RelationType.id).all()
                # 将对象从Session解绑，避免跨Session/commit后的DetachedInstanceError
                for item in items:
                    db_session.expunge(item)
                cls._relation_types_cache = items
                cls._cache_version = current_version
            
            return cls._relation_types_cache
    
    @classmethod
    def invalidate_cache(cls):
        """
        清空缓存
        
        在标签配置更新时调用,强制下次查询时重新加载
        """
        with cls._cache_lock:
            cls._entity_types_cache = None
            cls._relation_types_cache = None
            cls._cache_version += 1
    
    @classmethod
    def _get_config_version(cls, db_session: Session) -> int:
        """
        获取配置版本号
        
        基于标签配置的最后更新时间生成版本号
        
        Args:
            db_session: 数据库会话
            
        Returns:
            int: 版本号(时间戳)
        """
        try:
            # 查询实体类型的最后更新时间
            entity_max = db_session.query(func.max(EntityType.updated_at)).scalar()
            
            # 查询关系类型的最后更新时间
            relation_max = db_session.query(func.max(RelationType.updated_at)).scalar()
            
            # 使用最新的时间戳作为版本号
            if entity_max and relation_max:
                latest_time = max(entity_max, relation_max)
                return int(latest_time.timestamp())
            elif entity_max:
                return int(entity_max.timestamp())
            elif relation_max:
                return int(relation_max.timestamp())
            else:
                return 0
        except Exception:
            # 如果查询失败,返回0(会触发重新加载)
            return 0
    
    @classmethod
    def get_cache_stats(cls) -> dict:
        """
        获取缓存统计信息
        
        Returns:
            dict: 缓存统计信息
        """
        with cls._cache_lock:
            return {
                'entity_types_cached': cls._entity_types_cache is not None,
                'relation_types_cached': cls._relation_types_cache is not None,
                'cache_version': cls._cache_version,
                'entity_types_count': len(cls._entity_types_cache) if cls._entity_types_cache else 0,
                'relation_types_count': len(cls._relation_types_cache) if cls._relation_types_cache else 0
            }
