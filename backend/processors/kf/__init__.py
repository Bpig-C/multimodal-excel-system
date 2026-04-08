"""KF（快反问题记录）处理器"""
from ..base import BaseProcessor, ExportConfig, GraphConfig
from .config import (
    FIELD_MAPPING, DEFAULT_VALUES, COLUMN_MAPPINGS,
    ENTITY_FIELDS, RELATION_MAPPINGS, QA_QUERY, CLIP_FIELDS,
    NODE_TYPES, EDGE_LABELS
)
from .parser import process_excel_file


class KFProcessor(BaseProcessor):
    """快反问题记录处理器"""

    @property
    def name(self) -> str:
        return 'kf'

    @property
    def display_name(self) -> str:
        return '快反问题记录'

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
        return process_excel_file(file_path, output_dir)

    def get_export_config(self):
        return ExportConfig(
            field_names={v: v for v in FIELD_MAPPING.values()},
            entity_fields=ENTITY_FIELDS,
            relation_mappings=RELATION_MAPPINGS,
            qa_query=QA_QUERY,
            clip_fields=CLIP_FIELDS,
            event_id_field='快反编号',
        )

    def get_graph_config(self):
        return GraphConfig(
            node_types=NODE_TYPES,
            edge_labels=EDGE_LABELS,
        )
