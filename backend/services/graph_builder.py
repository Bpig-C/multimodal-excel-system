"""KF knowledge graph builder."""
import hashlib
import json
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy.orm import Session

from models.db_models import (
    Customer,
    Product,
    Defect,
    RootCause,
    FourMElement,
    QuickResponseEvent,
)


def _compute_kf_content_hash(entities: Dict) -> str:
    """计算 KF 条目的内容哈希（排除 id/data_source/images 等非业务字段）。"""
    event = entities.get("event", {})
    product = entities.get("product", {})
    root_cause = entities.get("root_cause", {})
    parts = [
        str(event.get("occurrence_time") or ""),
        str(event.get("problem_analysis") or ""),
        str(event.get("short_term_measure") or ""),
        str(event.get("long_term_measure") or ""),
        str(event.get("classification") or ""),
        str(entities.get("customer") or ""),
        str(product.get("model") or ""),
        str(product.get("category") or ""),
        str(product.get("industry") or ""),
        str(entities.get("defect") or ""),
        str(root_cause.get("category") or ""),
        str(root_cause.get("process") or ""),
        str(entities.get("four_m") or ""),
    ]
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class GraphBuilder:
    """Builds KF graph entities into relational tables."""

    def build_graph(self, db: Session, entities: Dict, skip_if_exists: bool = False) -> bool:
        """
        Build graph nodes and relationships.

        去重策略：
        1. 若 event_id 非空，以主键查重（唯一键优先）
        2. 以内容哈希兜底，防止相同内容用不同 id 重复写入

        Returns:
            True if inserted, False if skipped as duplicate.
        """
        event_id = entities["event"]["id"]
        content_hash = _compute_kf_content_hash(entities)

        if skip_if_exists:
            # 唯一键优先
            if event_id:
                existing = db.query(QuickResponseEvent).filter_by(id=event_id).first()
                if existing:
                    return False
            # 内容哈希兜底
            existing_by_hash = db.query(QuickResponseEvent).filter_by(
                content_hash=content_hash
            ).first()
            if existing_by_hash:
                return False

        customer_id = self._insert_customer(db, entities["customer"])
        product_id = self._insert_product(db, entities["product"])
        defect_id = self._insert_defect(db, entities["defect"])
        root_cause_id = self._insert_root_cause(db, entities["root_cause"])
        four_m_id = self._insert_four_m(db, entities["four_m"])

        self._insert_event(
            db,
            entities["event"],
            content_hash,
            customer_id,
            product_id,
            defect_id,
            root_cause_id,
            four_m_id,
        )

        db.commit()
        return True

    def _insert_customer(self, db: Session, name: str) -> Optional[int]:
        if not name:
            return None
        existing = db.query(Customer).filter_by(name=name).first()
        if existing:
            return existing.id
        db.add(Customer(name=name))
        db.flush()
        result = db.query(Customer).filter_by(name=name).first()
        return result.id if result else None

    def _insert_product(self, db: Session, product: Dict) -> Optional[int]:
        if not product.get("model"):
            return None
        existing = db.query(Product).filter_by(model=product["model"]).first()
        if existing:
            return existing.id
        db.add(
            Product(
                model=product["model"],
                product_category=product.get("category"),
                industry_category=product.get("industry"),
            )
        )
        db.flush()
        result = db.query(Product).filter_by(model=product["model"]).first()
        return result.id if result else None

    def _insert_defect(self, db: Session, name: str) -> Optional[int]:
        if not name:
            return None
        existing = db.query(Defect).filter_by(name=name).first()
        if existing:
            return existing.id
        db.add(Defect(name=name))
        db.flush()
        result = db.query(Defect).filter_by(name=name).first()
        return result.id if result else None

    def _insert_root_cause(self, db: Session, root_cause: Dict) -> Optional[int]:
        if not root_cause.get("category"):
            return None

        existing = db.query(RootCause).filter_by(
            category=root_cause["category"],
            process_category=root_cause.get("process"),
        ).first()
        if existing:
            return existing.id

        db.add(
            RootCause(
                category=root_cause["category"],
                process_category=root_cause.get("process"),
            )
        )
        db.flush()
        result = db.query(RootCause).filter_by(
            category=root_cause["category"],
            process_category=root_cause.get("process"),
        ).first()
        return result.id if result else None

    def _insert_four_m(self, db: Session, element: str) -> Optional[int]:
        if not element:
            return None
        existing = db.query(FourMElement).filter_by(element=element).first()
        if existing:
            return existing.id
        db.add(FourMElement(element=element))
        db.flush()
        result = db.query(FourMElement).filter_by(element=element).first()
        return result.id if result else None

    def _parse_occurrence_time(self, value: object) -> Optional[datetime]:
        """Normalize Excel/JSON date values to datetime for SQLAlchemy DateTime columns."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None

            iso_candidate = text[:-1] + "+00:00" if text.endswith("Z") else text
            try:
                return datetime.fromisoformat(iso_candidate)
            except ValueError:
                pass

            for fmt in (
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d",
                "%Y-%m-%d",
            ):
                try:
                    return datetime.strptime(text, fmt)
                except ValueError:
                    continue

        return None

    def _insert_event(
        self,
        db: Session,
        event: Dict,
        content_hash: str,
        customer_id: int,
        product_id: int,
        defect_id: int,
        root_cause_id: int,
        four_m_id: int,
    ) -> None:
        db.merge(
            QuickResponseEvent(
                id=event["id"],
                content_hash=content_hash,
                occurrence_time=self._parse_occurrence_time(event.get("occurrence_time")),
                problem_analysis=event.get("problem_analysis"),
                short_term_measure=event.get("short_term_measure"),
                long_term_measure=event.get("long_term_measure"),
                images=json.dumps(event.get("images", []), ensure_ascii=False),
                data_source=event.get("data_source"),
                classification=event.get("classification"),
                customer_id=customer_id,
                product_id=product_id,
                defect_id=defect_id,
                root_cause_id=root_cause_id,
                four_m_id=four_m_id,
            )
        )
