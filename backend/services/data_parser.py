import json
import logging
from typing import List, Dict
from pathlib import Path

from processors import get_processor

logger = logging.getLogger(__name__)


class DataParser:
    """解析表格数据，通过处理器配置驱动字段映射"""

    def __init__(self, processor_name: str = 'kf'):
        self.processor = get_processor(processor_name)

    def parse_json_file(self, file_path: str) -> List[Dict]:
        """解析JSON文件"""
        logger.debug(f"开始解析JSON文件: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.debug(f"JSON文件键: {list(data.keys())}")
        table_data = data.get('table_data', [])
        logger.debug(f"table_data长度: {len(table_data)}")

        if not table_data:
            logger.warning(f"JSON文件中没有table_data或为空: {file_path}")

        return table_data

    def extract_entities(self, record: Dict, data_source: str = None) -> Dict:
        """从单条记录提取实体，委托给处理器"""
        return self.processor.extract_entities(record, data_source)

    def detect_data_version(self, record: Dict) -> str:
        """
        检测数据版本

        Returns:
            'v2': 新版本（包含所有字段）
            'v1': 老版本（缺少所有字段）
            'v1.5': 部分缺失
        """
        required_fields = list(self.processor.default_values.keys())
        missing_count = sum(1 for f in required_fields if not record.get(f))

        if missing_count == 0:
            return 'v2'
        elif missing_count == len(required_fields):
            return 'v1'
        else:
            return 'v1.5'

    def batch_parse(self, file_paths: List[str]) -> List[Dict]:
        """批量解析多个JSON文件"""
        all_entities = []
        for file_path in file_paths:
            records = self.parse_json_file(file_path)
            for record in records:
                entities = self.extract_entities(record)
                all_entities.append(entities)
        return all_entities

    def parse_with_report(self, file_path: str) -> tuple[List[Dict], Dict]:
        """解析JSON文件并生成版本统计报告"""
        records = self.parse_json_file(file_path)

        stats = {
            'total': len(records),
            'v1': 0,
            'v2': 0,
            'v1.5': 0
        }

        for record in records:
            version = self.detect_data_version(record)
            stats[version] += 1

        logger.info(f"数据版本统计 - 总计: {stats['total']}, "
                    f"新版本(v2): {stats['v2']}, "
                    f"老版本(v1): {stats['v1']}, "
                    f"部分缺失(v1.5): {stats['v1.5']}")

        return records, stats
