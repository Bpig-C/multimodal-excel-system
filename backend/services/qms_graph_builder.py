"""QMS不合格品知识图谱构建器"""
import hashlib
import json
from typing import Dict, Optional
from sqlalchemy.orm import Session

from models.db_models import (
    Customer, Defect, QMSWorkshop, QMSProductionLine,
    QMSStation, QMSInspectionNode, QMSDefectOrder
)


def _compute_qms_content_hash(entities: Dict) -> str:
    """计算 QMS 条目的整行内容哈希，作为唯一去重依据。
    包含制令单号本身，确保同一制令单号+不同业务内容产生不同哈希。
    """
    event = entities.get("event", {})
    product = entities.get("product", {})
    production = entities.get("production", {})
    inspection = entities.get("inspection", {})
    parts = [
        str(event.get("id") or ""),              # 制令单号
        str(event.get("occurrence_time") or ""),
        str(event.get("status") or ""),
        str(entities.get("customer") or ""),
        str(product.get("model") or ""),
        str(product.get("barcode") or ""),
        str(product.get("position") or ""),
        str(entities.get("defect") or ""),
        str(production.get("workshop") or ""),
        str(production.get("line") or ""),
        str(production.get("station") or ""),
        str(inspection.get("node") or ""),
    ]
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class QMSGraphBuilder:
    """构建 QMS 不合格品知识图谱"""

    def build_graph(self, db: Session, entities: Dict, skip_if_exists: bool = False) -> bool:
        """
        构建 QMS 图谱节点和关系

        去重策略：仅以整行内容哈希去重。
        制令单号不作为主键，同一制令单号的不同缺陷记录可独立存储；
        完全相同内容的重复行（哈希碰撞）才被跳过。

        Returns:
            True=新插入，False=已存在被跳过
        """
        order_id = entities['event'].get('id')

        content_hash = _compute_qms_content_hash(entities)

        if skip_if_exists:
            existing = db.query(QMSDefectOrder).filter_by(content_hash=content_hash).first()
            if existing:
                return False

        customer_id = self._upsert_one(db, Customer, 'name', entities.get('customer'))

        prod = entities.get('product', {})
        defect_id = self._upsert_one(db, Defect, 'name', entities.get('defect'))

        production = entities.get('production', {})
        workshop_id = self._upsert_one(db, QMSWorkshop, 'name', production.get('workshop'))
        line_id = self._upsert_line(db, production.get('line'), workshop_id)
        station_id = self._upsert_one(db, QMSStation, 'name', production.get('station'))

        inspection = entities.get('inspection', {})
        inspection_node_id = self._upsert_one(db, QMSInspectionNode, 'name', inspection.get('node'))

        event = entities['event']
        images = event.get('images', [])
        photo_path = images[0] if images else None

        db.add(QMSDefectOrder(
            order_id=order_id,
            content_hash=content_hash,
            entry_time=event.get('occurrence_time'),
            model=prod.get('model'),
            barcode=prod.get('barcode'),
            position=prod.get('position'),
            photo_path=photo_path,
            status=event.get('status'),
            data_source=event.get('data_source'),
            customer_id=customer_id,
            workshop_id=workshop_id,
            line_id=line_id,
            station_id=station_id,
            defect_id=defect_id,
            inspection_node_id=inspection_node_id
        ))

        db.commit()
        return True

    def _upsert_one(self, db: Session, model_class, col: str, value: str) -> Optional[int]:
        """插入或忽略单列唯一值，返回 id"""
        if not value:
            return None
        existing = db.query(model_class).filter(getattr(model_class, col) == value).first()
        if existing:
            return existing.id
        db.add(model_class(**{col: value}))
        db.flush()
        result = db.query(model_class).filter(getattr(model_class, col) == value).first()
        return result.id if result else None

    def _upsert_line(self, db: Session, name: str, workshop_id: Optional[int]) -> Optional[int]:
        """插入产线（name + workshop_id 联合唯一），返回 id"""
        if not name:
            return None
        existing = db.query(QMSProductionLine).filter(
            QMSProductionLine.name == name,
            QMSProductionLine.workshop_id == workshop_id
        ).first()
        if existing:
            return existing.id
        db.add(QMSProductionLine(name=name, workshop_id=workshop_id))
        db.flush()
        result = db.query(QMSProductionLine).filter(
            QMSProductionLine.name == name,
            QMSProductionLine.workshop_id == workshop_id
        ).first()
        return result.id if result else None
