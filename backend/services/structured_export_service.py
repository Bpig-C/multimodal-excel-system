"""
语料导出服务
将表格数据转换为机器学习训练格式，配置由处理器驱动
"""
import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

from config import settings

logger = logging.getLogger(__name__)


class StructuredExportService:
    """语料导出器 - 支持三种导出格式，配置由处理器驱动"""

    def __init__(self, processor_name: str = 'kf'):
        """初始化导出器"""
        from processors import get_processor
        self._processor = get_processor(processor_name)
        self.processor_name = processor_name
        self.config = self._processor.get_export_config()
        self.field_mapping = self._processor.field_mapping
        self.default_values = self._processor.default_values

    def _get_field_value(self, record: Dict, field_name: str, use_default: bool = False) -> str:
        """获取字段值"""
        value = record.get(field_name, '')
        if not value or value == 'None':
            if use_default:
                return self.default_values.get(field_name, '')
            else:
                return ''
        return value

    def _has_valid_value(self, record: Dict, field_name: str) -> bool:
        """检查字段是否有有效值（非空且非"未分类"）"""
        value = record.get(field_name, '')
        return value and value != 'None' and value != '未分类' and value.strip() != ''

    def _extract_image_path(self, markdown_img: str) -> Optional[str]:
        """从Markdown格式提取图片路径"""
        if not markdown_img:
            return None
        pattern = r'!\[.*?\]\((.*?)\)'
        match = re.search(pattern, markdown_img)
        if match:
            return match.group(1)
        return None

    def _generate_sample_id(self, record: Dict, index: int, format_type: str) -> str:
        """生成唯一样本ID"""
        event_id_field = self.config.event_id_field
        qr_id = record.get(event_id_field, 'unknown')
        return f"{format_type}_{qr_id}_{index:03d}"

    @staticmethod
    def _build_space_map(text: str):
        """
        预计算空格映射表，将无空格文本的索引映射回原文索引。
        返回 (text_clean, clean_to_orig) 其中 clean_to_orig[i] = 原文中第 i 个非空格字符的位置。
        一次构建，所有实体复用。
        """
        clean_to_orig = []
        chars = []
        for i, ch in enumerate(text):
            if ch != ' ':
                clean_to_orig.append(i)
                chars.append(ch)
        return ''.join(chars), clean_to_orig

    def _find_entity_offset(self, text: str, entity_value: str, start_search: int = 0,
                            space_map: tuple = None) -> tuple:
        """
        在文本中查找实体的精确位置。
        space_map: 可选的预计算结果 (text_clean, clean_to_orig)，避免每次重建。
        """
        if not entity_value or entity_value == 'None':
            return None

        # 快速路径：精确匹配
        index = text.find(entity_value, start_search)
        if index != -1:
            return (index, index + len(entity_value))

        # 慢速路径：去空格模糊匹配，使用预计算映射表 O(1) 回映
        entity_clean = entity_value.replace(' ', '')
        if not entity_clean:
            return None

        if space_map is None:
            text_clean, clean_to_orig = self._build_space_map(text)
        else:
            text_clean, clean_to_orig = space_map

        # 将 start_search 转换为 clean 索引
        clean_start = 0
        if start_search > 0 and clean_to_orig:
            # 二分查找第一个 >= start_search 的 clean 索引
            lo, hi = 0, len(clean_to_orig)
            while lo < hi:
                mid = (lo + hi) // 2
                if clean_to_orig[mid] < start_search:
                    lo = mid + 1
                else:
                    hi = mid
            clean_start = lo

        index_clean = text_clean.find(entity_clean, clean_start)
        if index_clean != -1 and index_clean + len(entity_clean) <= len(clean_to_orig):
            orig_start = clean_to_orig[index_clean]
            orig_end = clean_to_orig[index_clean + len(entity_clean) - 1] + 1
            return (orig_start, orig_end)

        return None

    def export_entity_text(self, json_data: List[Dict], data_source: str = None) -> List[Dict]:
        """导出实体标注文本格式"""
        results = []
        fm = self.field_mapping
        images_field = fm.get('images', '')
        event_id_field = fm.get('event_id', '')
        classification_field = fm.get('classification', '')
        problem_analysis_field = fm.get('problem_analysis', '')
        customer_field = fm.get('customer', '')
        product_model_field = fm.get('product_model', '')
        defect_field = fm.get('defect', '')
        short_term_field = fm.get('short_term_measure', '')
        long_term_field = fm.get('long_term_measure', '')
        four_m_field = fm.get('four_m_element', '')
        industry_field = fm.get('industry_category', '')
        product_cat_field = fm.get('product_category', '')
        process_field = fm.get('process_category', '')
        root_cause_field = fm.get('root_cause_category', '')
        occurrence_field = fm.get('occurrence_time', '')

        for idx, record in enumerate(json_data):
            try:
                record_data_source = record.get('_data_source', data_source or 'unknown')

                # 尝试由处理器构建文本
                processor_text = self._processor.build_entity_text(record, record_data_source)
                if processor_text:
                    text = processor_text
                else:
                    # 回退：KF 原有文本构建逻辑
                    # 提取图片路径
                    image_path = self._extract_image_path(record.get(images_field, ''))
                    full_image_path = f"{record_data_source}/{image_path}" if image_path else None

                    # 构建图片子句
                    if full_image_path:
                        image_clause = f'问题图片已记录在路径"{full_image_path}"。'
                    else:
                        image_clause = ''

                    # 构建分类子句
                    classification = record.get(classification_field)
                    if classification and classification != 'None':
                        classification_clause = f'该产品所属分类为{classification}。'
                    else:
                        classification_clause = ''

                    # 构建分类信息文本
                    classification_parts = []

                    if self._has_valid_value(record, four_m_field):
                        classification_parts.append(f"4M要素涉及{record.get(four_m_field)}")
                    if self._has_valid_value(record, industry_field):
                        classification_parts.append(f"行业类别为{record.get(industry_field)}")
                    if self._has_valid_value(record, product_cat_field):
                        classification_parts.append(f"产品分类为{record.get(product_cat_field)}")
                    if self._has_valid_value(record, process_field):
                        classification_parts.append(f"过程分类属于{record.get(process_field)}")
                    if self._has_valid_value(record, root_cause_field):
                        classification_parts.append(f"异常原因为{record.get(root_cause_field)}")

                    if classification_parts:
                        classification_text = '，'.join(classification_parts) + '。'
                    else:
                        classification_text = ''

                    # 填充模板
                    text_parts = [
                        f"本次质量异常的快反编号是{record.get(event_id_field, '')}",
                        f"发生时间为{record.get(occurrence_field, '')}"
                    ]

                    problem_analysis = record.get(problem_analysis_field, '')
                    if problem_analysis:
                        text_parts.append(f"问题原因及分析显示为{problem_analysis}")

                    if image_clause:
                        text_parts.append(image_clause.rstrip('。'))

                    if classification_text:
                        text_parts.append(classification_text.rstrip('。'))

                    customer = record.get(customer_field, '')
                    product_model = record.get(product_model_field, '')
                    if customer and product_model:
                        text_parts.append(f"客户为{customer}，产品型号为{product_model}")
                    elif customer:
                        text_parts.append(f"客户为{customer}")
                    elif product_model:
                        text_parts.append(f"产品型号为{product_model}")

                    defect = record.get(defect_field, '')
                    if defect:
                        text_parts.append(f"缺陷类型不良现象是{defect}")

                    short_term = record.get(short_term_field, '')
                    long_term = record.get(long_term_field, '')
                    if short_term and long_term:
                        text_parts.append(f"短期改善措施为{short_term}，长期改善措施是{long_term}")
                    elif short_term:
                        text_parts.append(f"短期改善措施为{short_term}")
                    elif long_term:
                        text_parts.append(f"长期改善措施是{long_term}")

                    if classification_clause:
                        text_parts.append(classification_clause.rstrip('。'))

                    text = '。'.join(text_parts) + '。'

                text = ' '.join(text.split())

                # 提取实体和关系
                entities = []
                relations = []
                entity_id = 0
                entity_map = {}

                # 预计算空格映射表，所有实体复用
                space_map = self._build_space_map(text)

                search_pos = 0
                for field_name, label in self.config.entity_fields:
                    value = record.get(field_name, '')
                    if value and value != 'None' and value != '未分类':
                        offset = self._find_entity_offset(text, value, search_pos, space_map=space_map)
                        if offset:
                            entity = {
                                'id': entity_id,
                                'start_offset': offset[0],
                                'end_offset': offset[1],
                                'label': label,
                                'text': value
                            }
                            entities.append(entity)
                            entity_map[field_name] = entity_id
                            entity_id += 1
                            search_pos = offset[1]

                # 构建关系
                relation_id = 0
                event_id_entity = entity_map.get(event_id_field)

                if event_id_entity is not None:
                    for field_name, relation_type in self.config.relation_mappings:
                        target_id = entity_map.get(field_name)
                        if target_id is not None:
                            relations.append({
                                'id': relation_id,
                                'from_id': event_id_entity,
                                'to_id': target_id,
                                'type': relation_type
                            })
                            relation_id += 1

                result = {
                    'sample_id': self._generate_sample_id(record, idx, 'entity_text'),
                    'quick_response_id': record.get(event_id_field, ''),
                    'data_source': record_data_source,
                    'text': text,
                    'entities': entities,
                    'relations': relations
                }

                results.append(result)

            except Exception as e:
                logger.error(f"处理记录失败 {record.get(event_id_field)}: {str(e)}", exc_info=True)
                continue

        return results

    def export_clip_alignment(self, json_data: List[Dict], data_source: str = None) -> List[Dict]:
        """导出CLIP风格的图文对齐格式"""
        results = []
        images_field = self.field_mapping.get('images', '')
        event_id_field = self.config.event_id_field

        for idx, record in enumerate(json_data):
            try:
                record_data_source = record.get('_data_source', data_source or 'unknown')

                image_path = self._extract_image_path(record.get(images_field, ''))
                if not image_path:
                    continue

                full_image_path = f"{record_data_source}/{image_path}"

                # 构建caption - 使用配置中的字段顺序
                caption_parts = []
                for field_key in self.config.clip_fields:
                    value = record.get(field_key, '')
                    if value and value != 'None' and value != '未分类':
                        caption_parts.append(f"{field_key}：{value}")

                caption = '，'.join(caption_parts)

                result = {
                    'sample_id': self._generate_sample_id(record, idx, 'clip'),
                    'quick_response_id': record.get(event_id_field, ''),
                    'data_source': record_data_source,
                    'image_info': {
                        'path': full_image_path,
                        'caption': caption
                    }
                }

                results.append(result)

            except Exception as e:
                logger.error(f"处理记录失败 {record.get(event_id_field)}: {str(e)}")
                continue

        return results

    def export_qa_alignment(self, json_data: List[Dict], data_source: str = None) -> List[Dict]:
        """导出Q&A风格的多模态对齐格式"""
        results = []
        fm = self.field_mapping
        images_field = fm.get('images', '')
        event_id_field = self.config.event_id_field
        defect_field = fm.get('defect', '')
        process_field = fm.get('process_category', '')
        root_cause_field = fm.get('root_cause_category', '')
        short_term_field = fm.get('short_term_measure', '')
        long_term_field = fm.get('long_term_measure', '')

        for idx, record in enumerate(json_data):
            try:
                record_data_source = record.get('_data_source', data_source or 'unknown')

                image_path = self._extract_image_path(record.get(images_field, ''))
                full_image_path = f"{record_data_source}/{image_path}" if image_path else None

                # 构建assistant回答
                answer_parts = []

                if self._has_valid_value(record, defect_field):
                    answer_parts.append(f"缺陷类型为{record.get(defect_field)}")

                classification_info = []
                if self._has_valid_value(record, process_field):
                    classification_info.append(f"属于{record.get(process_field)}")
                if self._has_valid_value(record, root_cause_field):
                    classification_info.append(f"{record.get(root_cause_field)}导致")
                if classification_info:
                    answer_parts.append('，'.join(classification_info))

                measures = []
                short_term = record.get(short_term_field, '')
                long_term = record.get(long_term_field, '')
                if short_term and short_term != 'None':
                    measures.append(f"短期改善措施为{short_term}")
                if long_term and long_term != 'None':
                    measures.append(f"长期改善措施是{long_term}")
                if measures:
                    answer_parts.append('，'.join(measures))

                if answer_parts:
                    assistant_text = '。'.join(answer_parts) + '。'
                else:
                    assistant_text = '暂无详细信息。'

                assistant_text = ' '.join(assistant_text.split())

                result = {
                    'sample_id': self._generate_sample_id(record, idx, 'qa'),
                    'quick_response_id': record.get(event_id_field, ''),
                    'data_source': record_data_source,
                    'query': self.config.qa_query,
                    'assistant': assistant_text
                }

                if full_image_path:
                    result['image_info'] = {
                        'path': full_image_path
                    }

                results.append(result)

            except Exception as e:
                logger.error(f"处理记录失败 {record.get(event_id_field)}: {str(e)}")
                continue

        return results

    def batch_export(self, json_data: List[Dict], export_formats: List[str], include_images: bool = False) -> Dict:
        """
        批量导出多种格式

        Args:
            json_data: 解析后的JSON数据列表
            export_formats: 要导出的格式列表 ['entity_text', 'clip_alignment', 'qa_alignment']
            include_images: 是否在ZIP中包含图片文件

        Returns:
            包含各格式结果的字典，include_images=True 时额外包含 'image_files' 列表
            每项为 (zip内路径, 本地绝对路径)
        """
        results = {}

        for fmt in export_formats:
            if fmt == 'entity_text':
                results['entity_text'] = self.export_entity_text(json_data)
            elif fmt == 'clip_alignment':
                results['clip_alignment'] = self.export_clip_alignment(json_data)
            elif fmt == 'qa_alignment':
                results['qa_alignment'] = self.export_qa_alignment(json_data)

        if include_images:
            images_field = self.field_mapping.get('images', '')
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
            collected: Dict[str, Path] = {}  # zip内路径 → 本地路径，去重

            for record in json_data:
                data_source = record.get('_data_source', '')
                if not data_source:
                    continue

                # 优先从记录的图片字段提取具体文件名
                raw_img = record.get(images_field, '')
                img_rel = self._extract_image_path(raw_img)  # e.g. "imgs/ID_xxx.png"

                if img_rel:
                    local_path = settings.PROCESSED_DIR / self.processor_name / data_source / img_rel
                    if local_path.exists():
                        zip_path = f"images/{data_source}/{img_rel}"
                        collected[zip_path] = local_path
                else:
                    # 没有具体文件名时，把整个 imgs/ 目录下的图片全部打包
                    imgs_dir = settings.PROCESSED_DIR / self.processor_name / data_source / 'imgs'
                    if imgs_dir.exists():
                        for f in imgs_dir.iterdir():
                            if f.is_file() and f.suffix.lower() in image_extensions:
                                zip_path = f"images/{data_source}/imgs/{f.name}"
                                collected[zip_path] = f

            results['image_files'] = [(zp, str(lp)) for zp, lp in collected.items()]
            logger.info(f"[BATCH_EXPORT] 收集到图片 {len(results['image_files'])} 张")

        return results
