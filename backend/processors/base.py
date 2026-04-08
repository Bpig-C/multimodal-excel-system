"""处理器抽象基类"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import re


@dataclass
class ExportConfig:
    """导出配置"""
    # 字段名映射 {标准键: 源字段名}
    field_names: Dict[str, str]
    # 实体字段列表 [(源字段名, 实体标签)]
    entity_fields: List[Tuple[str, str]]
    # 关系映射 [(源字段名, 关系类型)]
    relation_mappings: List[Tuple[str, str]]
    # Q&A 查询模板
    qa_query: str
    # CLIP 导出字段顺序
    clip_fields: List[str]
    # 事件ID字段名
    event_id_field: str


@dataclass
class GraphConfig:
    """前端图谱可视化配置"""
    # 节点类型 {类型名: {label, color}}
    node_types: Dict[str, dict]
    # 边标签 {边类型: 显示标签}
    edge_labels: Dict[str, str]


class BaseProcessor(ABC):
    """表格处理器基类，定义处理器插件接口"""

    @property
    @abstractmethod
    def name(self) -> str:
        """处理器唯一标识"""
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        """显示名称"""
        ...

    @property
    @abstractmethod
    def field_mapping(self) -> Dict[str, str]:
        """
        源字段名 → 标准实体字段名映射

        标准字段:
        - event_id, occurrence_time, problem_analysis, images, data_source
        - short_term_measure, long_term_measure, classification
        - customer, product_model, product_category, industry_category
        - defect, root_cause_category, process_category, four_m_element
        - workshop, production_line, station, inspection_node, status, barcode, position
        """
        ...

    @property
    @abstractmethod
    def default_values(self) -> Dict[str, str]:
        """缺失字段默认值，键为源字段名"""
        ...

    @property
    @abstractmethod
    def column_mappings(self) -> Dict[str, str]:
        """Excel 列名重映射（旧列名 → 标准列名）"""
        ...

    @abstractmethod
    def parse_excel(self, file_path: str, output_dir: str) -> dict:
        """解析 Excel 文件，输出 JSON"""
        ...

    @abstractmethod
    def get_export_config(self) -> ExportConfig:
        """返回导出配置"""
        ...

    @abstractmethod
    def get_graph_config(self) -> GraphConfig:
        """返回图谱可视化配置"""
        ...

    def extract_entities(self, record: Dict, data_source: str = None) -> Dict:
        """
        从解析后的记录中提取标准实体，默认实现使用 field_mapping。
        子类可覆写以实现自定义逻辑。
        """
        fm = self.field_mapping
        dv = self.default_values
        return {
            'event': {
                'id': record.get(fm.get('event_id', '')),
                'occurrence_time': record.get(fm.get('occurrence_time', '')),
                'problem_analysis': record.get(fm.get('problem_analysis', '')),
                'images': self._extract_images(record.get(fm.get('images', ''), '')),
                'data_source': data_source,
                'short_term_measure': record.get(fm.get('short_term_measure', '')),
                'long_term_measure': record.get(fm.get('long_term_measure', '')),
                'classification': record.get(fm.get('classification', ''))
            },
            'customer': record.get(fm.get('customer', '')),
            'product': {
                'model': record.get(fm.get('product_model', '')),
                'category': record.get(fm.get('product_category', '')) or dv.get(fm.get('product_category', ''), '未分类'),
                'industry': record.get(fm.get('industry_category', '')) or dv.get(fm.get('industry_category', ''), '未分类'),
            },
            'defect': record.get(fm.get('defect', '')),
            'root_cause': {
                'category': record.get(fm.get('root_cause_category', '')) or dv.get(fm.get('root_cause_category', ''), '未分类'),
                'process': record.get(fm.get('process_category', '')) or dv.get(fm.get('process_category', ''), '未分类'),
            },
            'four_m': record.get(fm.get('four_m_element', '')) or dv.get(fm.get('four_m_element', ''), '未分类')
        }

    def _extract_images(self, image_text: str) -> List[str]:
        """从 Markdown 格式提取图片路径"""
        if not image_text:
            return []
        return re.findall(r'!\[.*?\]\((.*?)\)', image_text)

    def build_entity_text(self, record: Dict, data_source: str = None) -> str:
        """
        构建实体文本描述，供 corpus_exporter 使用。
        子类可覆写以提供处理器特定的文本模板。
        默认实现返回空字符串（由 corpus_exporter 自行构建）。
        """
        return ''
