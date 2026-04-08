"""鍥捐氨鏌ヨ寮曟搸"""
import json
import re
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from urllib.parse import quote
from sqlalchemy.orm import Session
from sqlalchemy import text, func

from config import settings
from models.db_models import (
    Corpus, QuickResponseEvent, QMSDefectOrder,
    Customer, Product, Defect, RootCause, FourMElement,
    QMSWorkshop, QMSProductionLine, QMSStation, QMSInspectionNode, Image
)
from utils.file_utils import sanitize_filename


class QueryEngine:
    """鍥捐氨鏌ヨ寮曟搸"""

    FAILURE_CASE_REQUIRED_FIELDS = [
        '问题分类',
        '客户/发生工程/供应商',
        '质量问题',
        '问题描述',
        '问题处理',
        '原因分析',
        '采取措施',
    ]

    def __init__(self, processor_name: str = 'kf'):
        self.processor_name = processor_name

    def _clean_image_path(self, image_path: Optional[str]) -> str:
        """Normalize image path to forward-slash relative format."""
        if not image_path:
            return ''
        return str(image_path).strip().replace('\\', '/').lstrip('/')

    def _to_storage_preview_url(self, image_path: Optional[str]) -> str:
        """Build preview URL for files managed by storage service (/images)."""
        cleaned = self._clean_image_path(image_path)
        if not cleaned:
            return ''
        if cleaned.startswith('images/'):
            cleaned = cleaned[len('images/'):]
        return f"/images/{quote(cleaned, safe='/')}"

    def _to_processed_preview_url(
        self,
        processor_name: str,
        data_source: Optional[str],
        image_path: Optional[str],
    ) -> str:
        """Build preview URL for processed KF/QMS image folders."""
        cleaned, ds = self._normalize_processed_relative_path(data_source, image_path)
        if not cleaned or not ds:
            return ''

        encoded_ds = quote(ds, safe='')
        encoded_path = quote(cleaned, safe='/')
        return f"/processed-images/{processor_name}/{encoded_ds}/{encoded_path}"

    def _normalize_processed_relative_path(
        self,
        data_source: Optional[str],
        image_path: Optional[str],
    ) -> Tuple[str, str]:
        """Normalize processed image relative path and datasource."""
        cleaned = self._clean_image_path(image_path)
        ds = (data_source or '').strip()
        if not cleaned or not ds:
            return cleaned, ds

        # Some records may store "{data_source}/imgs/xxx.png".
        prefix = f"{ds}/"
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
        return cleaned, ds

    def _candidate_processed_data_sources(self, data_source: Optional[str]) -> List[str]:
        """Build possible directory names for one logical data_source."""
        ds = (data_source or '').strip()
        if not ds:
            return []

        candidates: List[str] = []
        for item in (
            ds,
            sanitize_filename(ds),
            ds.replace('-', '_'),
            ds.replace('_', '-'),
        ):
            normalized = (item or '').strip()
            if normalized and normalized not in candidates:
                candidates.append(normalized)
        return candidates

    def _strip_data_source_prefix(self, image_path: str, data_source_candidates: List[str]) -> str:
        """Strip optional '<data_source>/' prefix in stored image path."""
        cleaned = self._clean_image_path(image_path)
        for ds in data_source_candidates:
            prefix = f"{ds}/"
            if cleaned.startswith(prefix):
                return cleaned[len(prefix):]
        return cleaned

    def _safe_local_resolve(self, base_dir: Path, relative_path: str) -> Optional[Path]:
        """Resolve path under base_dir and reject traversal paths."""
        if not relative_path:
            return None
        base = base_dir.resolve()
        candidate = (base / relative_path).resolve()
        try:
            candidate.relative_to(base)
        except ValueError:
            return None
        return candidate

    def _processed_image_exists(
        self,
        processor_name: str,
        data_source: Optional[str],
        image_path: Optional[str],
    ) -> bool:
        """Whether KF/QMS processed image file exists on local filesystem."""
        return self._resolve_processed_preview_url(processor_name, data_source, image_path) is not None

    def _resolve_processed_preview_url(
        self,
        processor_name: str,
        data_source: Optional[str],
        image_path: Optional[str],
    ) -> Optional[str]:
        """
        Resolve the first existing processed image URL.

        Handles data_source naming drift such as '-' vs '_'.
        """
        if settings.STORAGE_TYPE != 'local':
            # Processed images are local files; in non-local storage mode keep direct URL build.
            return self._to_processed_preview_url(processor_name, data_source, image_path)

        candidates = self._candidate_processed_data_sources(data_source)
        if not candidates:
            return None

        cleaned = self._strip_data_source_prefix(self._clean_image_path(image_path), candidates)
        if not cleaned:
            return None

        for candidate_ds in candidates:
            relative = f"{processor_name}/{candidate_ds}/{cleaned}"
            resolved = self._safe_local_resolve(settings.PROCESSED_DIR, relative)
            if resolved and resolved.is_file():
                encoded_ds = quote(candidate_ds, safe='')
                encoded_path = quote(cleaned, safe='/')
                return f"/processed-images/{processor_name}/{encoded_ds}/{encoded_path}"
        return None

    def _storage_image_exists(self, image_path: Optional[str]) -> bool:
        """Whether storage-managed image exists (local check, MinIO optimistic)."""
        cleaned = self._clean_image_path(image_path)
        if not cleaned:
            return False
        if settings.STORAGE_TYPE != 'local':
            # MinIO does not have cheap local existence check here; keep preview enabled.
            return True
        resolved = self._safe_local_resolve(settings.IMAGE_DIR, cleaned)
        return bool(resolved and resolved.is_file())

    def _parse_image_paths(self, raw_value) -> List[str]:
        """Parse image path list from json/list/string/markdown values."""
        if raw_value is None:
            return []

        if isinstance(raw_value, list):
            candidates = [str(v) for v in raw_value if str(v).strip()]
        else:
            text_value = str(raw_value).strip()
            if not text_value:
                return []

            candidates: List[str] = []

            # Markdown images: ![...](path)
            markdown_paths = re.findall(r'!\[.*?\]\((.*?)\)', text_value)
            if markdown_paths:
                candidates.extend(markdown_paths)
            else:
                # JSON array or JSON string
                try:
                    parsed = json.loads(text_value)
                    if isinstance(parsed, list):
                        candidates.extend([str(v) for v in parsed if str(v).strip()])
                    elif isinstance(parsed, str) and parsed.strip():
                        candidates.append(parsed.strip())
                except Exception:
                    # Common separators for multiple values
                    if any(sep in text_value for sep in [',', ';', '|']):
                        for part in re.split(r'[,;|]', text_value):
                            if part.strip():
                                candidates.append(part.strip())
                    else:
                        candidates.append(text_value)

        normalized: List[str] = []
        seen = set()
        for item in candidates:
            cleaned = self._clean_image_path(item)
            if not cleaned:
                continue
            if cleaned not in seen:
                seen.add(cleaned)
                normalized.append(cleaned)

        return normalized

    def _build_kf_preview_urls(self, image_paths: List[str], data_source: Optional[str]) -> List[str]:
        urls: List[str] = []
        for path in image_paths:
            if path.startswith(('http://', 'https://')):
                urls.append(path)
                continue

            # KF/QMS current data usually points to processed/{processor}/{data_source}/imgs/*
            processed_url = self._resolve_processed_preview_url('kf', data_source, path)
            if processed_url:
                urls.append(processed_url)
            elif self._storage_image_exists(path):
                urls.append(self._to_storage_preview_url(path))
        return urls

    def _build_qms_preview_urls(self, image_paths: List[str], data_source: Optional[str]) -> List[str]:
        urls: List[str] = []
        for path in image_paths:
            if path.startswith(('http://', 'https://')):
                urls.append(path)
                continue

            processed_url = self._resolve_processed_preview_url('qms', data_source, path)
            if processed_url:
                urls.append(processed_url)
            elif self._storage_image_exists(path):
                urls.append(self._to_storage_preview_url(path))
        return urls

    def _get_failure_case_image_paths(self, db: Session, source_file: str, source_row: int) -> List[str]:
        image_rows = db.query(Image.file_path).join(
            Corpus, Image.corpus_id == Corpus.id
        ).filter(
            Corpus.source_file == source_file,
            Corpus.source_row == source_row,
        ).all()
        image_paths = [self._clean_image_path(row[0]) for row in image_rows if row and row[0]]
        seen = set()
        unique_paths: List[str] = []
        for path in image_paths:
            if path and path not in seen:
                seen.add(path)
                unique_paths.append(path)
        return unique_paths

    def get_graph_data(self, db: Session, filters: Optional[Dict] = None, limit: int = 100) -> Dict:
        """鑾峰彇鍥捐氨鏁版嵁"""
        if self.processor_name == 'qms':
            return self._get_qms_graph_data(db, filters, limit)
        return self._get_kf_graph_data(db, filters, limit)

    def _get_kf_graph_data(self, db: Session, filters: Optional[Dict] = None, limit: int = 100) -> Dict:
        nodes = []
        edges = []
        node_ids = set()

        # 鏋勫缓鏌ヨ
        query = db.query(
            QuickResponseEvent, Customer, Product, Defect, RootCause, FourMElement
        ).outerjoin(
            Customer, QuickResponseEvent.customer_id == Customer.id
        ).outerjoin(
            Product, QuickResponseEvent.product_id == Product.id
        ).outerjoin(
            Defect, QuickResponseEvent.defect_id == Defect.id
        ).outerjoin(
            RootCause, QuickResponseEvent.root_cause_id == RootCause.id
        ).outerjoin(
            FourMElement, QuickResponseEvent.four_m_id == FourMElement.id
        )

        # 搴旂敤杩囨护
        if filters:
            if filters.get('customer'):
                query = query.filter(Customer.name == filters['customer'])
            if filters.get('product'):
                query = query.filter(Product.model == filters['product'])
            if filters.get('defect'):
                query = query.filter(Defect.name == filters['defect'])
            if filters.get('start_date'):
                query = query.filter(QuickResponseEvent.occurrence_time >= filters['start_date'])
            if filters.get('end_date'):
                query = query.filter(QuickResponseEvent.occurrence_time <= filters['end_date'])

        query = query.limit(limit)
        results = query.all()

        for event, customer, product, defect, root_cause, four_m in results:
            event_id = f"event_{event.id}"

            # 澶勭悊鍥剧墖璺緞
            event_data = {
                'id': event.id,
                'occurrence_time': str(event.occurrence_time) if event.occurrence_time else None,
                'problem_analysis': event.problem_analysis,
                'short_term_measure': event.short_term_measure,
                'long_term_measure': event.long_term_measure,
                'images': [],
                'data_source': event.data_source,
                'classification': event.classification,
            }
            if event.images:
                try:
                    images = json.loads(event.images) if isinstance(event.images, str) else event.images
                    data_source = event.data_source or ''
                    event_data['images'] = [f"{data_source}/{img}" if data_source else img for img in images]
                except:
                    event_data['images'] = []

            nodes.append({
                'id': event_id,
                'type': 'QuickResponseEvent',
                'text': event.id,
                'data': event_data
            })
            node_ids.add(event_id)

            # 瀹㈡埛鑺傜偣
            if customer:
                customer_id = f"customer_{customer.id}"
                if customer_id not in node_ids:
                    nodes.append({
                        'id': customer_id,
                        'type': 'Customer',
                        'text': customer.name,
                        'data': {'name': customer.name}
                    })
                    node_ids.add(customer_id)
                edges.append({
                    'from': event_id,
                    'to': customer_id,
                    'text': '褰掑睘瀹㈡埛',
                    'type': 'BELONGS_TO_CUSTOMER'
                })

            # 浜у搧鑺傜偣
            if product:
                product_id = f"product_{product.id}"
                if product_id not in node_ids:
                    nodes.append({
                        'id': product_id,
                        'type': 'ProductModel',
                        'text': product.model,
                        'data': {
                            'model': product.model,
                            'category': product.product_category,
                            'industry': product.industry_category
                        }
                    })
                    node_ids.add(product_id)
                edges.append({
                    'from': event_id,
                    'to': product_id,
                    'text': '娑夊強浜у搧',
                    'type': 'INVOLVES_PRODUCT'
                })

            # 缂洪櫡鑺傜偣
            if defect:
                defect_id = f"defect_{defect.id}"
                if defect_id not in node_ids:
                    nodes.append({
                        'id': defect_id,
                        'type': 'DefectType',
                        'text': defect.name,
                        'data': {'name': defect.name}
                    })
                    node_ids.add(defect_id)
                edges.append({
                    'from': event_id,
                    'to': defect_id,
                    'text': '缂洪櫡绫诲瀷',
                    'type': 'HAS_DEFECT'
                })

            # 寮傚父鍘熷洜鑺傜偣
            if root_cause and root_cause.category and root_cause.category != '鏈垎绫?':
                rc_id = f"root_cause_{root_cause.id}"
                if rc_id not in node_ids:
                    nodes.append({
                        'id': rc_id,
                        'type': 'RootCause',
                        'text': root_cause.category,
                        'data': {
                            'category': root_cause.category,
                            'process': root_cause.process_category
                        }
                    })
                    node_ids.add(rc_id)
                edges.append({
                    'from': event_id,
                    'to': rc_id,
                    'text': '寮傚父鍘熷洜',
                    'type': 'ATTRIBUTED_TO'
                })

            # 4M瑕佺礌鑺傜偣
            if four_m and four_m.element and four_m.element != '鏈垎绫?':
                fm_id = f"four_m_{four_m.id}"
                if fm_id not in node_ids:
                    nodes.append({
                        'id': fm_id,
                        'type': 'FourMElement',
                        'text': four_m.element,
                        'data': {'element': four_m.element}
                    })
                    node_ids.add(fm_id)
                edges.append({
                    'from': event_id,
                    'to': fm_id,
                    'text': '4M瑕佺礌',
                    'type': 'RELATED_TO_4M'
                })

        return {'nodes': nodes, 'lines': edges}

    def _get_qms_graph_data(self, db: Session, filters: Optional[Dict] = None, limit: int = 100) -> Dict:
        nodes = []
        edges = []
        node_ids = set()

        query = db.query(QMSDefectOrder).outerjoin(
            Customer, QMSDefectOrder.customer_id == Customer.id
        ).outerjoin(
            QMSWorkshop, QMSDefectOrder.workshop_id == QMSWorkshop.id
        ).outerjoin(
            QMSProductionLine, QMSDefectOrder.line_id == QMSProductionLine.id
        ).outerjoin(
            QMSStation, QMSDefectOrder.station_id == QMSStation.id
        ).outerjoin(
            Defect, QMSDefectOrder.defect_id == Defect.id
        ).outerjoin(
            QMSInspectionNode, QMSDefectOrder.inspection_node_id == QMSInspectionNode.id
        )

        if filters:
            if filters.get('customer'):
                query = query.filter(Customer.name == filters['customer'])
            if filters.get('defect'):
                query = query.filter(Defect.name == filters['defect'])
            if filters.get('workshop'):
                query = query.filter(QMSWorkshop.name == filters['workshop'])
            if filters.get('start_date'):
                query = query.filter(QMSDefectOrder.entry_time >= filters['start_date'])
            if filters.get('end_date'):
                query = query.filter(QMSDefectOrder.entry_time <= filters['end_date'])

        query = query.limit(limit)
        results = query.all()

        for order in results:
            order_id = f"order_{order.id}"

            order_data = {
                'id': order.id,
                'entry_time': order.entry_time,
                'model': order.model,
                'barcode': order.barcode,
                'position': order.position,
                'status': order.status,
                'data_source': order.data_source,
            }

            nodes.append({
                'id': order_id,
                'type': 'DefectOrder',
                'text': order.id,
                'data': order_data
            })
            node_ids.add(order_id)

        return {'nodes': nodes, 'lines': edges}

    def get_event_detail(self, db: Session, event_id: str) -> Optional[Dict]:
        """鑾峰彇浜嬩欢璇︽儏"""
        event = db.query(QuickResponseEvent).filter(QuickResponseEvent.id == event_id).first()
        if not event:
            return None

        result = {
            'id': event.id,
            'occurrence_time': str(event.occurrence_time) if event.occurrence_time else None,
            'problem_analysis': event.problem_analysis,
            'short_term_measure': event.short_term_measure,
            'long_term_measure': event.long_term_measure,
            'data_source': event.data_source,
            'classification': event.classification,
        }

        if event.images:
            try:
                images = json.loads(event.images) if isinstance(event.images, str) else event.images
                data_source = event.data_source or ''
                result['images'] = [f"{data_source}/{img}" if data_source else img for img in images]
            except:
                result['images'] = []

        return result

    def get_statistics(self, db: Session) -> Dict:
        """鑾峰彇缁熻鏁版嵁"""
        if self.processor_name == 'failure_case':
            return self._get_failure_case_statistics(db)
        if self.processor_name == 'qms':
            return self._get_qms_statistics(db)
        return self._get_kf_statistics(db)

    def _get_kf_statistics(self, db: Session) -> Dict:
        stats = {}

        # 鎬讳簨浠舵暟
        stats['total_events'] = db.query(QuickResponseEvent).count()

        # 缂洪櫡绫诲瀷鍒嗗竷
        defect_dist = db.query(
            Defect.name, func.count(QuickResponseEvent.id).label('count')
        ).join(
            QuickResponseEvent, QuickResponseEvent.defect_id == Defect.id
        ).group_by(
            Defect.name
        ).order_by(
            text('count DESC')
        ).limit(10).all()
        stats['defect_distribution'] = [{'name': d[0], 'count': d[1]} for d in defect_dist]

        # 4M瑕佺礌鍒嗗竷
        four_m_dist = db.query(
            FourMElement.element, func.count(QuickResponseEvent.id).label('count')
        ).join(
            QuickResponseEvent, QuickResponseEvent.four_m_id == FourMElement.id
        ).filter(
            FourMElement.element != '鏈垎绫?'
        ).group_by(
            FourMElement.element
        ).order_by(
            text('count DESC')
        ).all()
        stats['four_m_distribution'] = [{'element': d[0], 'count': d[1]} for d in four_m_dist]

        # 瀹㈡埛闂鎺掕
        customer_rank = db.query(
            Customer.name, func.count(QuickResponseEvent.id).label('count')
        ).join(
            QuickResponseEvent, QuickResponseEvent.customer_id == Customer.id
        ).group_by(
            Customer.name
        ).order_by(
            text('count DESC')
        ).limit(10).all()
        stats['customer_ranking'] = [{'name': c[0], 'count': c[1]} for c in customer_rank]

        return stats

    def _get_qms_statistics(self, db: Session) -> Dict:
        stats = {}

        stats['total_events'] = db.query(QMSDefectOrder).count()

        # 缂洪櫡鍒嗗竷
        defect_dist = db.query(
            Defect.name, func.count(QMSDefectOrder.id).label('count')
        ).join(
            QMSDefectOrder, QMSDefectOrder.defect_id == Defect.id
        ).group_by(
            Defect.name
        ).order_by(
            text('count DESC')
        ).limit(10).all()
        stats['defect_distribution'] = [{'name': d[0], 'count': d[1]} for d in defect_dist]

        # 杞﹂棿鍒嗗竷
        workshop_dist = db.query(
            QMSWorkshop.name, func.count(QMSDefectOrder.id).label('count')
        ).join(
            QMSDefectOrder, QMSDefectOrder.workshop_id == QMSWorkshop.id
        ).group_by(
            QMSWorkshop.name
        ).order_by(
            text('count DESC')
        ).all()
        stats['workshop_distribution'] = [{'name': w[0], 'count': w[1]} for w in workshop_dist]

        # 浜х嚎鍒嗗竷
        line_dist = db.query(
            QMSProductionLine.name, func.count(QMSDefectOrder.id).label('count')
        ).join(
            QMSDefectOrder, QMSDefectOrder.line_id == QMSProductionLine.id
        ).group_by(
            QMSProductionLine.name
        ).order_by(
            text('count DESC')
        ).limit(10).all()
        stats['line_distribution'] = [{'name': l[0], 'count': l[1]} for l in line_dist]

        # 璐ㄦ鑺傜偣鍒嗗竷
        inspection_dist = db.query(
            QMSInspectionNode.name, func.count(QMSDefectOrder.id).label('count')
        ).join(
            QMSDefectOrder, QMSDefectOrder.inspection_node_id == QMSInspectionNode.id
        ).group_by(
            QMSInspectionNode.name
        ).order_by(
            text('count DESC')
        ).all()
        stats['inspection_node_distribution'] = [{'name': i[0], 'count': i[1]} for i in inspection_dist]

        # 鐘舵€佸垎甯?
        status_dist = db.query(
            QMSDefectOrder.status, func.count(QMSDefectOrder.id).label('count')
        ).filter(
            QMSDefectOrder.status.isnot(None),
            QMSDefectOrder.status != ''
        ).group_by(
            QMSDefectOrder.status
        ).order_by(
            text('count DESC')
        ).all()
        stats['status_distribution'] = [{'status': s[0], 'count': s[1]} for s in status_dist]

        # 瀹㈡埛鎺掕
        customer_rank = db.query(
            Customer.name, func.count(QMSDefectOrder.id).label('count')
        ).join(
            QMSDefectOrder, QMSDefectOrder.customer_id == Customer.id
        ).group_by(
            Customer.name
        ).order_by(
            text('count DESC')
        ).limit(10).all()
        stats['customer_ranking'] = [{'name': c[0], 'count': c[1]} for c in customer_rank]

        return stats

    def get_data_list(self, db: Session, processor_name: str = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        """鑾峰彇鏁版嵁鍒楄〃"""
        target = processor_name or self.processor_name
        if target == 'failure_case':
            return self._get_failure_case_list(db, limit, offset)
        if target == 'qms':
            return self._get_qms_list(db, limit, offset)
        return self._get_kf_list(db, limit, offset)
    def get_data_total_count(self, db: Session, processor_name: str = None) -> int:
        """Get total row count for pagination."""
        target = processor_name or self.processor_name
        if target == 'failure_case':
            return db.query(
                Corpus.source_file,
                Corpus.source_row,
            ).filter(
                Corpus.source_file.isnot(None),
                Corpus.source_row.isnot(None),
            ).group_by(
                Corpus.source_file,
                Corpus.source_row,
            ).count()
        if target == 'qms':
            return db.query(QMSDefectOrder).count()
        return db.query(QuickResponseEvent).count()
    def _get_kf_list(self, db: Session, limit: int = 100, offset: int = 0) -> List[Dict]:
        results = db.query(QuickResponseEvent).limit(limit).offset(offset).all()
        response: List[Dict] = []
        for e in results:
            image_paths = self._parse_image_paths(e.images)
            image_preview_urls = self._build_kf_preview_urls(image_paths, e.data_source)
            response.append({
                'id': e.id,
                'occurrence_time': str(e.occurrence_time) if e.occurrence_time else None,
                'problem_analysis': e.problem_analysis,
                'short_term_measure': e.short_term_measure,
                'long_term_measure': e.long_term_measure,
                'classification': e.classification,
                'data_source': e.data_source,
                'image_paths': image_paths,
                'image_preview_urls': image_preview_urls,
                'image_count': len(image_paths),
                'image_available_count': len(image_preview_urls),
                'image_missing_count': max(0, len(image_paths) - len(image_preview_urls)),
            })
        return response

    def _get_qms_list(self, db: Session, limit: int = 100, offset: int = 0) -> List[Dict]:
        results = db.query(QMSDefectOrder).limit(limit).offset(offset).all()
        response: List[Dict] = []
        for e in results:
            image_paths = self._parse_image_paths(e.photo_path)
            image_preview_urls = self._build_qms_preview_urls(image_paths, e.data_source)
            response.append({
                'id': e.id,
                'entry_time': e.entry_time,
                'model': e.model,
                'barcode': e.barcode,
                'position': e.position,
                'status': e.status,
                'data_source': e.data_source,
                'image_paths': image_paths,
                'image_preview_urls': image_preview_urls,
                'image_count': len(image_paths),
                'image_available_count': len(image_preview_urls),
                'image_missing_count': max(0, len(image_paths) - len(image_preview_urls)),
            })
        return response

    def _get_failure_case_list(self, db: Session, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Group failure case records by source_file and source_row."""
        grouped_rows = db.query(
            Corpus.source_file,
            Corpus.source_row,
        ).filter(
            Corpus.source_file.isnot(None),
            Corpus.source_row.isnot(None),
        ).group_by(
            Corpus.source_file,
            Corpus.source_row,
        ).order_by(
            Corpus.source_file.desc(),
            Corpus.source_row.desc(),
        ).offset(offset).limit(limit).all()

        results: List[Dict] = []
        for source_file, source_row in grouped_rows:
            record = {
                'id': f'{source_file}:{source_row}',
                'source_file': source_file,
                'source_row': source_row,
            }
            for field in self.FAILURE_CASE_REQUIRED_FIELDS:
                record[field] = ''

            field_rows = db.query(
                Corpus.source_field,
                Corpus.text,
            ).filter(
                Corpus.source_file == source_file,
                Corpus.source_row == source_row,
                Corpus.source_field.in_(self.FAILURE_CASE_REQUIRED_FIELDS),
            ).all()

            for source_field, text_value in field_rows:
                if not source_field:
                    continue
                if not record[source_field]:
                    record[source_field] = text_value or ''

            image_paths = self._get_failure_case_image_paths(db, source_file, source_row)
            record['image_paths'] = image_paths
            image_preview_urls = [
                self._to_storage_preview_url(path) for path in image_paths
                if self._storage_image_exists(path)
            ]
            record['image_preview_urls'] = image_preview_urls
            record['image_count'] = len(image_paths)
            record['image_available_count'] = len(image_preview_urls)
            record['image_missing_count'] = max(0, len(image_paths) - len(image_preview_urls))

            results.append(record)

        return results

    def _get_failure_case_statistics(self, db: Session) -> Dict:
        """Failure case statistics aggregated from corpus."""
        stats: Dict = {}

        # 鎬讳簨浠舵暟锛氭寜 source_file + source_row 鍘婚噸
        stats['total_events'] = db.query(
            Corpus.source_file,
            Corpus.source_row,
        ).filter(
            Corpus.source_file.isnot(None),
            Corpus.source_row.isnot(None),
        ).group_by(
            Corpus.source_file,
            Corpus.source_row,
        ).count()

        defect_dist = db.query(
            Corpus.text,
            func.count(Corpus.id).label('count'),
        ).filter(
            Corpus.source_field == '质量问题',
            Corpus.text.isnot(None),
            Corpus.text != '',
        ).group_by(
            Corpus.text,
        ).order_by(
            text('count DESC'),
        ).limit(10).all()
        if not defect_dist:
            # Backward compatibility for older imports that only kept coarse category.
            defect_dist = db.query(
                Corpus.text,
                func.count(Corpus.id).label('count'),
            ).filter(
                Corpus.source_field == '问题分类',
                Corpus.text.isnot(None),
                Corpus.text != '',
            ).group_by(
                Corpus.text,
            ).order_by(
                text('count DESC'),
            ).limit(10).all()
        stats['defect_distribution'] = [{'name': d[0], 'count': d[1]} for d in defect_dist]

        customer_rank = db.query(
            Corpus.text,
            func.count(Corpus.id).label('count'),
        ).filter(
            Corpus.source_field == '客户/发生工程/供应商',
            Corpus.text.isnot(None),
            Corpus.text != '',
        ).group_by(
            Corpus.text,
        ).order_by(
            text('count DESC'),
        ).limit(10).all()
        stats['customer_ranking'] = [{'name': c[0], 'count': c[1]} for c in customer_rank]

        # 椤甸潰澶嶇敤瀛楁锛氬搧璐ㄦ渚嬫棤 4M 鍒嗗竷
        stats['four_m_distribution'] = []

        return stats








