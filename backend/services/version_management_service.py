"""
版本管理服务
提供标注任务的版本控制功能,包括版本创建、历史查询、回滚和比较
"""
import uuid
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.db_models import (
    AnnotationTask, VersionHistory, TextEntity, 
    ImageEntity, Relation
)


class VersionManagementService:
    """版本管理服务"""
    
    def __init__(self, db: Session):
        """
        初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create_version(
        self,
        task_id: str,
        change_type: str,
        change_description: Optional[str] = None,
        changed_by: Optional[int] = None
    ) -> VersionHistory:
        """
        创建版本快照
        
        Args:
            task_id: 任务ID
            change_type: 变更类型 ('create', 'update', 'delete')
            change_description: 变更描述
            changed_by: 变更人ID
            
        Returns:
            VersionHistory: 版本历史对象
        """
        # 查询任务
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.task_id == task_id
        ).first()
        
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")
        
        # 生成版本ID
        history_id = f"version-{uuid.uuid4().hex[:12]}"
        
        # 获取当前版本号
        current_version = task.current_version
        
        # 创建快照数据
        snapshot_data = self._create_snapshot(task, current_version)
        
        # 创建版本历史记录
        version_history = VersionHistory(
            history_id=history_id,
            task_id=task.id,
            version=current_version,
            change_type=change_type,
            change_description=change_description,
            changed_by=changed_by,
            snapshot_data=json.dumps(snapshot_data, ensure_ascii=False)
        )
        
        self.db.add(version_history)
        self.db.commit()
        self.db.refresh(version_history)
        
        return version_history
    
    def get_version_history(
        self,
        task_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        获取版本历史
        
        Args:
            task_id: 任务ID
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 版本历史列表
        """
        # 查询任务
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.task_id == task_id
        ).first()
        
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")
        
        # 查询版本历史
        query = self.db.query(VersionHistory)\
            .filter(VersionHistory.task_id == task.id)\
            .order_by(desc(VersionHistory.version))
        
        if limit:
            query = query.limit(limit)
        
        histories = query.all()
        
        # 格式化返回数据
        result = []
        for history in histories:
            result.append({
                'history_id': history.history_id,
                'version': history.version,
                'change_type': history.change_type,
                'change_description': history.change_description,
                'changed_by': history.changed_by,
                'created_at': history.created_at.isoformat(),
                'is_current': history.version == task.current_version
            })
        
        return result
    
    def rollback_to_version(
        self,
        task_id: str,
        target_version: int,
        changed_by: Optional[int] = None
    ) -> bool:
        """
        回滚到指定版本
        
        Args:
            task_id: 任务ID
            target_version: 目标版本号
            changed_by: 操作人ID
            
        Returns:
            bool: 是否回滚成功
        """
        # 查询任务
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.task_id == task_id
        ).first()
        
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")
        
        # 查询目标版本
        target_history = self.db.query(VersionHistory)\
            .filter(VersionHistory.task_id == task.id)\
            .filter(VersionHistory.version == target_version)\
            .first()
        
        if not target_history:
            raise ValueError(f"版本 {target_version} 不存在")
        
        # 如果已经是当前版本,无需回滚
        if task.current_version == target_version:
            return True
        
        # 先创建当前版本的快照(作为回滚前的备份)
        self.create_version(
            task_id=task_id,
            change_type='update',
            change_description=f'回滚前备份(从版本{task.current_version})',
            changed_by=changed_by
        )
        
        # 解析目标版本的快照数据
        snapshot_data = json.loads(target_history.snapshot_data)
        
        # 恢复数据
        self._restore_snapshot(task, snapshot_data, target_version)
        
        # 更新任务的当前版本号
        task.current_version = target_version
        
        # 创建回滚记录
        self.create_version(
            task_id=task_id,
            change_type='update',
            change_description=f'回滚到版本{target_version}',
            changed_by=changed_by
        )
        
        self.db.commit()
        
        return True
    
    def compare_versions(
        self,
        task_id: str,
        version1: int,
        version2: int
    ) -> Dict[str, Any]:
        """
        比较两个版本的差异
        
        Args:
            task_id: 任务ID
            version1: 版本1
            version2: 版本2
            
        Returns:
            Dict: 版本差异信息
        """
        # 查询任务
        task = self.db.query(AnnotationTask).filter(
            AnnotationTask.task_id == task_id
        ).first()
        
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")
        
        # 查询两个版本
        history1 = self.db.query(VersionHistory)\
            .filter(VersionHistory.task_id == task.id)\
            .filter(VersionHistory.version == version1)\
            .first()
        
        history2 = self.db.query(VersionHistory)\
            .filter(VersionHistory.task_id == task.id)\
            .filter(VersionHistory.version == version2)\
            .first()
        
        if not history1:
            raise ValueError(f"版本 {version1} 不存在")
        if not history2:
            raise ValueError(f"版本 {version2} 不存在")
        
        # 解析快照数据
        snapshot1 = json.loads(history1.snapshot_data)
        snapshot2 = json.loads(history2.snapshot_data)
        
        # 计算差异
        diff = self._calculate_diff(snapshot1, snapshot2)
        
        return {
            'task_id': task_id,
            'version1': version1,
            'version2': version2,
            'diff': diff,
            'summary': {
                'entities_added': len(diff['entities']['added']),
                'entities_removed': len(diff['entities']['removed']),
                'entities_modified': len(diff['entities']['modified']),
                'relations_added': len(diff['relations']['added']),
                'relations_removed': len(diff['relations']['removed']),
                'relations_modified': len(diff['relations']['modified']),
                'image_entities_added': len(diff['image_entities']['added']),
                'image_entities_removed': len(diff['image_entities']['removed']),
                'image_entities_modified': len(diff['image_entities']['modified'])
            }
        }
    
    def _create_snapshot(
        self,
        task: AnnotationTask,
        version: int
    ) -> Dict[str, Any]:
        """
        创建任务快照
        
        Args:
            task: 标注任务对象
            version: 版本号
            
        Returns:
            Dict: 快照数据
        """
        # 查询文本实体
        text_entities = self.db.query(TextEntity)\
            .filter(TextEntity.task_id == task.id)\
            .filter(TextEntity.version == version)\
            .all()
        
        # 查询图片实体
        image_entities = self.db.query(ImageEntity)\
            .filter(ImageEntity.task_id == task.id)\
            .filter(ImageEntity.version == version)\
            .all()
        
        # 查询关系
        relations = self.db.query(Relation)\
            .filter(Relation.task_id == task.id)\
            .filter(Relation.version == version)\
            .all()
        
        # 构建快照数据
        snapshot = {
            'version': version,
            'task_info': {
                'task_id': task.task_id,
                'status': task.status,
                'annotation_type': task.annotation_type
            },
            'entities': [
                {
                    'entity_id': e.entity_id,
                    'token': e.token,
                    'label': e.label,
                    'start_offset': e.start_offset,
                    'end_offset': e.end_offset,
                    'confidence': e.confidence
                }
                for e in text_entities
            ],
            'image_entities': [
                {
                    'entity_id': ie.entity_id,
                    'image_id': ie.image_id,
                    'label': ie.label,
                    'bbox_x': ie.bbox_x,
                    'bbox_y': ie.bbox_y,
                    'bbox_width': ie.bbox_width,
                    'bbox_height': ie.bbox_height,
                    'confidence': ie.confidence
                }
                for ie in image_entities
            ],
            'relations': [
                {
                    'relation_id': r.relation_id,
                    'from_entity_id': r.from_entity_id,
                    'to_entity_id': r.to_entity_id,
                    'relation_type': r.relation_type
                }
                for r in relations
            ]
        }
        
        return snapshot
    
    def _restore_snapshot(
        self,
        task: AnnotationTask,
        snapshot_data: Dict[str, Any],
        target_version: int
    ):
        """
        恢复快照数据
        
        Args:
            task: 标注任务对象
            snapshot_data: 快照数据
            target_version: 目标版本号
        """
        # 删除当前版本的所有数据
        self.db.query(TextEntity)\
            .filter(TextEntity.task_id == task.id)\
            .filter(TextEntity.version == task.current_version)\
            .delete()
        
        self.db.query(ImageEntity)\
            .filter(ImageEntity.task_id == task.id)\
            .filter(ImageEntity.version == task.current_version)\
            .delete()
        
        self.db.query(Relation)\
            .filter(Relation.task_id == task.id)\
            .filter(Relation.version == task.current_version)\
            .delete()
        
        # 恢复文本实体
        for entity_data in snapshot_data.get('entities', []):
            entity = TextEntity(
                task_id=task.id,
                entity_id=entity_data['entity_id'],
                token=entity_data['token'],
                label=entity_data['label'],
                start_offset=entity_data['start_offset'],
                end_offset=entity_data['end_offset'],
                confidence=entity_data.get('confidence'),
                version=target_version
            )
            self.db.add(entity)
        
        # 恢复图片实体
        for ie_data in snapshot_data.get('image_entities', []):
            image_entity = ImageEntity(
                task_id=task.id,
                entity_id=ie_data['entity_id'],
                image_id=ie_data['image_id'],
                label=ie_data['label'],
                bbox_x=ie_data.get('bbox_x'),
                bbox_y=ie_data.get('bbox_y'),
                bbox_width=ie_data.get('bbox_width'),
                bbox_height=ie_data.get('bbox_height'),
                confidence=ie_data.get('confidence'),
                version=target_version
            )
            self.db.add(image_entity)
        
        # 恢复关系
        for relation_data in snapshot_data.get('relations', []):
            relation = Relation(
                task_id=task.id,
                relation_id=relation_data['relation_id'],
                from_entity_id=relation_data['from_entity_id'],
                to_entity_id=relation_data['to_entity_id'],
                relation_type=relation_data['relation_type'],
                version=target_version
            )
            self.db.add(relation)
        
        # 更新任务信息
        task_info = snapshot_data.get('task_info', {})
        if 'status' in task_info:
            task.status = task_info['status']
        if 'annotation_type' in task_info:
            task.annotation_type = task_info['annotation_type']
    
    def _calculate_diff(
        self,
        snapshot1: Dict[str, Any],
        snapshot2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        计算两个快照的差异
        
        Args:
            snapshot1: 快照1
            snapshot2: 快照2
            
        Returns:
            Dict: 差异信息
        """
        def compare_lists(list1, list2, id_key):
            """比较两个列表的差异"""
            dict1 = {item[id_key]: item for item in list1}
            dict2 = {item[id_key]: item for item in list2}
            
            added = [dict2[k] for k in dict2 if k not in dict1]
            removed = [dict1[k] for k in dict1 if k not in dict2]
            modified = []
            
            for k in dict1:
                if k in dict2 and dict1[k] != dict2[k]:
                    modified.append({
                        'old': dict1[k],
                        'new': dict2[k]
                    })
            
            return {
                'added': added,
                'removed': removed,
                'modified': modified
            }
        
        # 比较实体
        entities_diff = compare_lists(
            snapshot1.get('entities', []),
            snapshot2.get('entities', []),
            'entity_id'
        )
        
        # 比较图片实体
        image_entities_diff = compare_lists(
            snapshot1.get('image_entities', []),
            snapshot2.get('image_entities', []),
            'entity_id'
        )
        
        # 比较关系
        relations_diff = compare_lists(
            snapshot1.get('relations', []),
            snapshot2.get('relations', []),
            'relation_id'
        )
        
        return {
            'entities': entities_diff,
            'image_entities': image_entities_diff,
            'relations': relations_diff
        }
