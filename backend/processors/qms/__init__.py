"""QMS（不合格品记录）处理器"""
from ..base import BaseProcessor, ExportConfig, GraphConfig
from .config import (
    FIELD_MAPPING, DEFAULT_VALUES, COLUMN_MAPPINGS,
    ENTITY_FIELDS, RELATION_MAPPINGS, QA_QUERY, CLIP_FIELDS,
    NODE_TYPES, EDGE_LABELS
)
from .parser import process_qms_excel


class QMSProcessor(BaseProcessor):
    """不合格品记录处理器"""

    @property
    def name(self) -> str:
        return 'qms'

    @property
    def display_name(self) -> str:
        return '不合格品记录'

    @property
    def field_mapping(self):
        return FIELD_MAPPING

    @property
    def default_values(self):
        return DEFAULT_VALUES

    @property
    def column_mappings(self):
        return COLUMN_MAPPINGS

    def parse_excel(self, file_path, output_dir):
        return process_qms_excel(file_path, output_dir)

    def get_export_config(self):
        return ExportConfig(
            field_names={v: v for v in FIELD_MAPPING.values()},
            entity_fields=ENTITY_FIELDS,
            relation_mappings=RELATION_MAPPINGS,
            qa_query=QA_QUERY,
            clip_fields=CLIP_FIELDS,
            event_id_field='制令单号',
        )

    def get_graph_config(self):
        return GraphConfig(
            node_types=NODE_TYPES,
            edge_labels=EDGE_LABELS,
        )

    def extract_entities(self, record: dict, data_source: str = None) -> dict:
        """QMS 特有实体结构"""
        fm = self.field_mapping
        return {
            'event': {
                'id': record.get(fm.get('event_id', '')),
                'occurrence_time': record.get(fm.get('occurrence_time', '')),
                'images': self._extract_images(record.get(fm.get('images', ''), '')),
                'data_source': data_source,
                'status': record.get(fm.get('status', '')),
            },
            'customer': record.get(fm.get('customer', '')),
            'product': {
                'model': record.get(fm.get('product_model', '')),
                'barcode': record.get(fm.get('barcode', '')),
                'position': record.get(fm.get('position', '')),
            },
            'defect': record.get(fm.get('defect', '')),
            'production': {
                'workshop': record.get(fm.get('workshop', '')),
                'line': record.get(fm.get('production_line', '')),
                'station': record.get(fm.get('station', '')),
            },
            'inspection': {
                'node': record.get(fm.get('inspection_node', '')),
                'status': record.get(fm.get('status', '')),
            }
        }

    def build_entity_text(self, record: dict, data_source: str = None) -> str:
        """构建 QMS 实体文本（用于语料导出）"""
        fm = self.field_mapping
        parts = [
            f"制令单号为{record.get(fm['event_id'], '')}",
            f"录入时间为{record.get(fm['occurrence_time'], '')}",
        ]

        customer = record.get(fm.get('customer', ''), '')
        model = record.get(fm.get('product_model', ''), '')
        if customer and model:
            parts.append(f"客户为{customer}，型号为{model}")
        elif customer:
            parts.append(f"客户为{customer}")
        elif model:
            parts.append(f"型号为{model}")

        barcode = record.get(fm.get('barcode', ''), '')
        position = record.get(fm.get('position', ''), '')
        if barcode:
            parts.append(f"条码为{barcode}")
        if position:
            parts.append(f"位号为{position}")

        workshop = record.get(fm.get('workshop', ''), '')
        line = record.get(fm.get('production_line', ''), '')
        station = record.get(fm.get('station', ''), '')
        prod_parts = []
        if workshop:
            prod_parts.append(f"车间{workshop}")
        if line:
            prod_parts.append(f"产线{line}")
        if station:
            prod_parts.append(f"岗位{station}")
        if prod_parts:
            parts.append('，'.join(prod_parts))

        defect = record.get(fm.get('defect', ''), '')
        if defect:
            parts.append(f"不良项目为{defect}")

        inspection_node = record.get(fm.get('inspection_node', ''), '')
        status = record.get(fm.get('status', ''), '')
        if inspection_node:
            parts.append(f"质检节点为{inspection_node}")
        if status:
            parts.append(f"状态为{status}")

        return '，'.join(parts) + '。'
