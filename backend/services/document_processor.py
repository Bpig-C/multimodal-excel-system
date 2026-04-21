"""
Excel文件处理服务
支持WPS Excel和Microsoft Excel格式的图片提取
"""
import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Optional
import logging

from database import SessionLocal
from models.db_models import Corpus
from processors import get_processor
from utils.file_utils import sanitize_filename
from config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Excel文件处理器"""

    def __init__(self, processor_name: str = 'kf'):
        """
        初始化文档处理器

        Args:
            processor_name: 处理器名称 ('kf' / 'qms' / 'failure_case')
        """
        self.upload_dir = settings.UPLOAD_DIR / processor_name
        self.processed_dir = settings.PROCESSED_DIR
        self.hash_file = self.upload_dir / "file_hashes.json"
        self.processor = get_processor(processor_name)
        self.processor_name = processor_name

        logger.info(f"[DocumentProcessor] upload_dir: {self.upload_dir}")
        logger.info(f"[DocumentProcessor] processed_dir: {self.processed_dir}")
        logger.info(f"[DocumentProcessor] processor: {self.processor.name}")

        # 目录已在 config.py 启动时创建，此处仅做保险
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # 加载已处理文件的哈希记录
        self.file_hashes = self._load_hashes()

    def _load_hashes(self) -> Dict[str, Dict]:
        """加载文件哈希记录，兼容旧版共用 file_hashes.json 的数据"""
        logger.info(f"[_load_hashes] 尝试加载: {self.hash_file}")
        logger.info(f"[_load_hashes] 文件存在: {self.hash_file.exists()}")
        if self.hash_file.exists():
            try:
                with open(self.hash_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"[_load_hashes] 成功加载 {len(data)} 条记录")
                    return data
            except Exception as e:
                logger.error(f"加载哈希记录失败: {e}")
                return {}

        # 兼容旧版：尝试从根目录 file_hashes.json 迁移本处理器的记录
        legacy_hash_file = settings.UPLOAD_DIR / "file_hashes.json"
        if legacy_hash_file.exists():
            try:
                with open(legacy_hash_file, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
                migrated = {k: v for k, v in all_data.items()
                            if v.get('processor') == self.processor_name}
                if migrated:
                    logger.info(f"[_load_hashes] 从旧版哈希文件迁移 {len(migrated)} 条记录")
                    # 写入新位置，下次直接读
                    with open(self.hash_file, 'w', encoding='utf-8') as f:
                        json.dump(migrated, f, ensure_ascii=False, indent=2)
                    return migrated
            except Exception as e:
                logger.error(f"迁移旧版哈希记录失败: {e}")

        logger.info(f"[_load_hashes] 文件不存在，返回空字典")
        return {}

    def _save_hashes(self):
        """保存文件哈希记录"""
        try:
            with open(self.hash_file, 'w', encoding='utf-8') as f:
                json.dump(self.file_hashes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存哈希记录失败: {e}")

    def calculate_file_hash(self, file_path: Path) -> str:
        """计算文件的SHA256哈希值"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def check_duplicate(self, file_hash: str, filename: str) -> Optional[Dict]:
        """检查文件是否已处理过"""
        if file_hash in self.file_hashes:
            record = self.file_hashes[file_hash]
            logger.info(f"发现重复文件: {filename}, 原文件: {record['original_filename']}")
            return record
        return None

    def extract_data_source(self, filename: str) -> str:
        """从文件名提取数据源"""
        base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
        sanitized_name = sanitize_filename(base_name)
        return sanitized_name

    def process_excel(self, file_path: Path, original_filename: str) -> Dict:
        """处理Excel文件"""
        try:
            # 1. 计算文件哈希
            file_hash = self.calculate_file_hash(file_path)
            logger.info(f"文件哈希: {file_hash}")

            # 2. 检查是否重复
            duplicate_record = self.check_duplicate(file_hash, original_filename)
            if duplicate_record:
                return {
                    'success': True,
                    'is_duplicate': True,
                    'message': f'文件已处理过，跳过重复处理',
                    'original_file': duplicate_record['original_filename'],
                    'processed_time': duplicate_record['processed_time'],
                    'output_dir': duplicate_record['output_dir'],
                    'data_source': duplicate_record['data_source']
                }

            # 3. 规范化文件名
            sanitized_name = sanitize_filename(original_filename)
            base_name = sanitized_name.rsplit('.', 1)[0]

            # 4. 提取数据源
            data_source = self.extract_data_source(original_filename)
            logger.info(f"数据源: {data_source}")

            # 5. 设置输出目录: data/processed/{processor_name}/{data_source}/
            output_dir = self.processed_dir / self.processor_name / data_source

            # 6. 通过处理器解析Excel文件
            logger.info(f"开始处理Excel文件: {original_filename}")
            result = self.processor.parse_excel(str(file_path), str(output_dir))

            # 7. 记录处理信息
            import datetime
            process_record = {
                'file_hash': file_hash,
                'original_filename': original_filename,
                'sanitized_filename': sanitized_name,
                'data_source': data_source,
                'output_dir': str(output_dir),
                'table_count': result['table_count'],
                'image_directory': result['image_directory'],
                'processed_time': datetime.datetime.now().isoformat(),
                'status': result['status'],
                'processor': self.processor.name
            }

            # 8. 保存哈希记录
            self.file_hashes[file_hash] = process_record
            self._save_hashes()

            logger.info(f"Excel处理完成: {result['table_count']} 个表格")

            return {
                'success': True,
                'is_duplicate': False,
                'message': '文件处理成功',
                'data_source': data_source,
                'output_dir': str(output_dir),
                'table_count': result['table_count'],
                'image_count': len(list(Path(result['image_directory']).glob('*.*'))) if Path(result['image_directory']).exists() else 0,
                'json_files': [f"page_{i}.json" for i in range(result['table_count'])]
            }

        except Exception as e:
            logger.error(f"处理Excel文件失败: {str(e)}", exc_info=True)
            return {
                'success': False,
                'is_duplicate': False,
                'message': f'处理失败: {str(e)}'
            }

    def reload_hashes(self):
        """重新加载哈希记录"""
        self.file_hashes = self._load_hashes()
        logger.info(f"重新加载哈希记录，当前数量: {len(self.file_hashes)}")

    def _get_failure_case_record_count(self, record: Dict) -> int:
        """从语料库中统计品质案例的实际记录数。"""
        source_file = (record.get('original_filename') or '').strip()
        if not source_file:
            return 0

        db = SessionLocal()
        try:
            return db.query(Corpus.source_row).filter(
                Corpus.source_file == source_file,
                Corpus.source_row.isnot(None)
            ).distinct().count()
        except Exception as e:
            logger.error(f"[get_processed_files] 统计 failure_case 记录数失败: {source_file}, 错误: {e}")
            return 0
        finally:
            db.close()

    def _get_db_record_count(self, data_source: str) -> int:
        """从数据库统计 kf/qms 处理器的实际写入记录数。"""
        from models.db_models import QuickResponseEvent, QMSDefectOrder
        db = SessionLocal()
        try:
            if self.processor_name == 'kf':
                return db.query(QuickResponseEvent).filter(
                    QuickResponseEvent.data_source == data_source
                ).count()
            if self.processor_name == 'qms':
                return db.query(QMSDefectOrder).filter(
                    QMSDefectOrder.data_source == data_source
                ).count()
            return 0
        except Exception as e:
            logger.error(f"[get_processed_files] 统计DB记录数失败: {data_source}, 错误: {e}")
            return 0
        finally:
            db.close()

    def get_processed_files(self) -> list:
        """获取已处理文件列表"""
        result = []
        logger.info(f"[get_processed_files] 哈希记录数量: {len(self.file_hashes)}")

        for file_hash, record in self.file_hashes.items():
            if record.get('processor') != self.processor_name:
                continue
            output_dir = Path(record['output_dir'])
            record_count = 0

            if self.processor_name == 'failure_case':
                record_count = self._get_failure_case_record_count(record)
            elif self.processor_name in ('kf', 'qms'):
                record_count = self._get_db_record_count(record['data_source'])
            elif output_dir.exists():
                json_files = list(sorted(output_dir.glob('page_*.json')))
                for json_file in json_files:
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            record_count += len(data.get('table_data', []))
                    except Exception as e:
                        logger.error(f"[get_processed_files] 读取JSON文件失败: {json_file}, 错误: {e}")
            else:
                logger.warning(f"[get_processed_files] 输出目录不存在: {output_dir}")

            result.append({
                'filename': record['original_filename'],
                'data_source': record['data_source'],
                'table_count': record_count,
                'processed_time': record['processed_time'],
                'output_dir': record['output_dir']
            })

        logger.info(f"[get_processed_files] 返回 {len(result)} 个文件记录")
        return result
