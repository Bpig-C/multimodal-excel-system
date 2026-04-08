"""
Reward数据集生成服务
用于生成LLM自动标注与人工修正之间的差异数据，用于模型微调
"""
import json
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.db_models import (
    Dataset, AnnotationTask, TextEntity, ImageEntity, Relation,
    VersionHistory, Corpus
)


class RewardDatasetService:
    """Reward数据集生成服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_reward_dataset(
        self,
        dataset_id: int,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成Reward数据集
        
        Args:
            dataset_id: 数据集ID
            output_path: 输出文件路径（可选）
        
        Returns:
            Dict: 包含Reward数据和统计信息
                - reward_data: Reward数据列表
                - statistics: 修正频率统计
                - total_count: 总记录数
        """
        # 查询数据集
        dataset = self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError(f"数据集不存在: {dataset_id}")
        
        # 筛选存在人工修正的任务
        corrected_tasks = self._filter_corrected_tasks(dataset_id)
        
        # 生成Reward数据
        reward_records = []
        statistics = {
            'entity_added': 0,
            'entity_removed': 0,
            'entity_label_modified': 0,
            'relation_added': 0,
            'relation_removed': 0,
            'image_entity_added': 0,
            'image_entity_removed': 0,
            'image_entity_label_modified': 0
        }
        
        for task in corrected_tasks:
            # 获取原始标注和修正标注
            original_annotation = self._get_original_annotation(task)
            corrected_annotation = self._get_current_annotation(task)
            
            # 计算差异
            diff = self._calculate_diff(original_annotation, corrected_annotation)
            
            # 更新统计
            self._update_statistics(statistics, diff)
            
            # 构建Reward记录
            reward_record = {
                'task_id': task.task_id,
                'text': original_annotation.get('text', ''),
                'text_type': original_annotation.get('text_type'),
                'original_annotation': original_annotation,
                'corrected_annotation': corrected_annotation,
                'diff': diff
            }
            
            reward_records.append(reward_record)
        
        # 导出到文件
        if output_path:
            self._export_to_jsonl(reward_records, output_path)
        
        return {
            'reward_data': reward_records,
            'statistics': statistics,
            'total_count': len(reward_records)
        }
    
    def _filter_corrected_tasks(self, dataset_id: int) -> List[AnnotationTask]:
        """
        筛选存在人工修正的标注任务
        
        Args:
            dataset_id: 数据集ID
        
        Returns:
            List[AnnotationTask]: 存在修正的任务列表
        """
        # 查询数据集中的所有任务
        tasks = self.db.query(AnnotationTask).filter(
            AnnotationTask.dataset_id == dataset_id
        ).all()
        
        corrected_tasks = []
        
        for task in tasks:
            # 检查是否存在版本历史（版本号>1表示有修正）
            if task.current_version > 1:
                corrected_tasks.append(task)
            # 或者检查是否从automatic变为manual
            elif task.annotation_type == 'manual':
                # 查询是否有版本1的记录
                version1 = self.db.query(VersionHistory).filter(
                    and_(
                        VersionHistory.task_id == task.id,
                        VersionHistory.version == 1
                    )
                ).first()
                
                if version1:
                    corrected_tasks.append(task)
        
        return corrected_tasks
    
    def _get_original_annotation(self, task: AnnotationTask) -> Dict[str, Any]:
        """
        获取原始标注（版本1）
        
        Args:
            task: 标注任务
        
        Returns:
            Dict: 原始标注数据
        """
        # 查询版本1的历史记录
        version1_history = self.db.query(VersionHistory).filter(
            and_(
                VersionHistory.task_id == task.id,
                VersionHistory.version == 1
            )
        ).first()
        
        if version1_history and version1_history.snapshot_data:
            # 从快照中恢复
            snapshot = json.loads(version1_history.snapshot_data)
            return self._format_annotation_from_snapshot(task, snapshot)
        else:
            # 如果没有快照，查询版本1的实体和关系
            return self._query_annotation_by_version(task, 1)
    
    def _get_current_annotation(self, task: AnnotationTask) -> Dict[str, Any]:
        """
        获取当前标注（最新版本）
        
        Args:
            task: 标注任务
        
        Returns:
            Dict: 当前标注数据
        """
        return self._query_annotation_by_version(task, task.current_version)
    
    def _query_annotation_by_version(
        self,
        task: AnnotationTask,
        version: int
    ) -> Dict[str, Any]:
        """
        查询指定版本的标注数据
        
        Args:
            task: 标注任务
            version: 版本号
        
        Returns:
            Dict: 标注数据
        """
        # 查询语料
        corpus = self.db.query(Corpus).filter(
            Corpus.id == task.corpus_id
        ).first()
        
        # 查询文本实体
        text_entities = self.db.query(TextEntity).filter(
            and_(
                TextEntity.task_id == task.id,
                TextEntity.version == version
            )
        ).all()
        
        # 查询图片实体
        image_entities = self.db.query(ImageEntity).filter(
            and_(
                ImageEntity.task_id == task.id,
                ImageEntity.version == version
            )
        ).all()
        
        # 查询关系
        relations = self.db.query(Relation).filter(
            and_(
                Relation.task_id == task.id,
                Relation.version == version
            )
        ).all()
        
        return {
            'text': corpus.text if corpus else '',
            'text_type': corpus.text_type if corpus else None,
            'entities': [
                {
                    'id': e.entity_id,
                    'token': e.token,
                    'label': e.label,
                    'start_offset': e.start_offset,
                    'end_offset': e.end_offset
                }
                for e in text_entities
            ],
            'image_entities': [
                {
                    'id': ie.entity_id,
                    'image_id': ie.image_id,
                    'label': ie.label,
                    'bbox_x': ie.bbox_x,
                    'bbox_y': ie.bbox_y,
                    'bbox_width': ie.bbox_width,
                    'bbox_height': ie.bbox_height
                }
                for ie in image_entities
            ],
            'relations': [
                {
                    'from_id': r.from_entity_id,
                    'to_id': r.to_entity_id,
                    'type': r.relation_type
                }
                for r in relations
            ]
        }
    
    def _format_annotation_from_snapshot(
        self,
        task: AnnotationTask,
        snapshot: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        从快照格式化标注数据
        
        Args:
            task: 标注任务
            snapshot: 快照数据
        
        Returns:
            Dict: 格式化的标注数据
        """
        # 查询语料
        corpus = self.db.query(Corpus).filter(
            Corpus.id == task.corpus_id
        ).first()
        
        # 格式化实体，将entity_id重命名为id以保持一致性
        entities = []
        for e in snapshot.get('entities', []):
            entity = e.copy()
            if 'entity_id' in entity and 'id' not in entity:
                entity['id'] = entity['entity_id']
            entities.append(entity)
        
        # 格式化图片实体
        image_entities = []
        for ie in snapshot.get('image_entities', []):
            img_entity = ie.copy()
            if 'entity_id' in img_entity and 'id' not in img_entity:
                img_entity['id'] = img_entity['entity_id']
            image_entities.append(img_entity)
        
        return {
            'text': corpus.text if corpus else '',
            'text_type': corpus.text_type if corpus else None,
            'entities': entities,
            'image_entities': image_entities,
            'relations': snapshot.get('relations', [])
        }
    
    def _calculate_diff(
        self,
        original: Dict[str, Any],
        corrected: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        计算原始标注和修正标注之间的差异
        
        Args:
            original: 原始标注
            corrected: 修正标注
        
        Returns:
            Dict: 差异描述
        """
        def compare_entities(orig_list, corr_list):
            """比较实体列表"""
            orig_dict = {e['id']: e for e in orig_list}
            corr_dict = {e['id']: e for e in corr_list}
            
            added = [e for eid, e in corr_dict.items() if eid not in orig_dict]
            removed = [e for eid, e in orig_dict.items() if eid not in corr_dict]
            modified = []
            
            for eid in orig_dict:
                if eid in corr_dict:
                    orig_e = orig_dict[eid]
                    corr_e = corr_dict[eid]
                    
                    # 检查标签是否修改
                    if orig_e.get('label') != corr_e.get('label'):
                        modified.append({
                            'id': eid,
                            'old_label': orig_e.get('label'),
                            'new_label': corr_e.get('label'),
                            'token': corr_e.get('token', '')
                        })
            
            return {
                'added': added,
                'removed': removed,
                'modified': modified
            }
        
        def compare_relations(orig_list, corr_list):
            """比较关系列表"""
            # 使用(from_id, to_id)作为关系的唯一标识
            orig_set = {(r['from_id'], r['to_id']) for r in orig_list}
            corr_set = {(r['from_id'], r['to_id']) for r in corr_list}
            
            orig_dict = {(r['from_id'], r['to_id']): r for r in orig_list}
            corr_dict = {(r['from_id'], r['to_id']): r for r in corr_list}
            
            added = [corr_dict[k] for k in corr_set - orig_set]
            removed = [orig_dict[k] for k in orig_set - corr_set]
            
            return {
                'added': added,
                'removed': removed
            }
        
        # 比较文本实体
        entities_diff = compare_entities(
            original.get('entities', []),
            corrected.get('entities', [])
        )
        
        # 比较图片实体
        image_entities_diff = compare_entities(
            original.get('image_entities', []),
            corrected.get('image_entities', [])
        )
        
        # 比较关系
        relations_diff = compare_relations(
            original.get('relations', []),
            corrected.get('relations', [])
        )
        
        return {
            'entities': entities_diff,
            'image_entities': image_entities_diff,
            'relations': relations_diff
        }
    
    def _update_statistics(
        self,
        statistics: Dict[str, int],
        diff: Dict[str, Any]
    ):
        """
        更新修正频率统计
        
        Args:
            statistics: 统计字典
            diff: 差异数据
        """
        # 文本实体统计
        statistics['entity_added'] += len(diff['entities']['added'])
        statistics['entity_removed'] += len(diff['entities']['removed'])
        statistics['entity_label_modified'] += len(diff['entities']['modified'])
        
        # 图片实体统计
        statistics['image_entity_added'] += len(diff['image_entities']['added'])
        statistics['image_entity_removed'] += len(diff['image_entities']['removed'])
        statistics['image_entity_label_modified'] += len(diff['image_entities']['modified'])
        
        # 关系统计
        statistics['relation_added'] += len(diff['relations']['added'])
        statistics['relation_removed'] += len(diff['relations']['removed'])
    
    def _export_to_jsonl(
        self,
        reward_data: List[Dict[str, Any]],
        output_path: str
    ):
        """
        导出Reward数据到JSONL文件
        
        Args:
            reward_data: Reward数据列表
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for record in reward_data:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def get_correction_frequency_report(
        self,
        dataset_id: int
    ) -> Dict[str, Any]:
        """
        获取修正频率报告
        
        Args:
            dataset_id: 数据集ID
        
        Returns:
            Dict: 修正频率报告
        """
        result = self.generate_reward_dataset(dataset_id)
        
        statistics = result['statistics']
        total_corrections = sum(statistics.values())
        
        # 计算百分比
        frequency_report = {}
        for key, count in statistics.items():
            percentage = (count / total_corrections * 100) if total_corrections > 0 else 0
            frequency_report[key] = {
                'count': count,
                'percentage': round(percentage, 2)
            }
        
        return {
            'total_corrections': total_corrections,
            'total_corrected_tasks': result['total_count'],
            'frequency': frequency_report
        }
