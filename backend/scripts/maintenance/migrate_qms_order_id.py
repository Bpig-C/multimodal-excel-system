"""
迁移脚本：qms_defect_orders 表结构变更

变更内容：
  - id: String(100) 主键（制令单号） → Integer 自增主键
  - 新增 order_id: String(100) 普通列（存放制令单号，非唯一）
  - content_hash: 保持唯一约束不变，作为唯一去重依据

背景：同一制令单号可能对应多条不同缺陷记录，不能作为主键。
去重改为仅依赖整行内容哈希。

操作步骤：
  1. 重命名旧表为备份表
  2. 用新结构创建 qms_defect_orders
  3. 将旧数据迁移过来（旧 id → 新 order_id）
  4. 删除备份表
"""
import sys
import os
from pathlib import Path
from sqlalchemy import text

BACKEND_ROOT = Path(__file__).resolve().parents[2]
os.chdir(BACKEND_ROOT)
sys.path.insert(0, str(BACKEND_ROOT))

from database import SessionLocal, engine
from config import settings
from models.db_models import Base, QMSDefectOrder


def get_db_path() -> str:
    url = settings.DATABASE_URL
    if url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "", 1)
    return url


def table_exists(db, name: str) -> bool:
    return bool(db.execute(
        text("SELECT 1 FROM sqlite_master WHERE type='table' AND name=:n"),
        {"n": name}
    ).first())


def column_exists(db, table: str, col: str) -> bool:
    rows = db.execute(text(f'PRAGMA table_info("{table}")')).fetchall()
    return any(row[1] == col for row in rows)


def main():
    print("=" * 60)
    print("qms_defect_orders 表结构迁移")
    print("=" * 60)
    print(f"数据库: {get_db_path()}")

    db = SessionLocal()
    try:
        if not table_exists(db, "qms_defect_orders"):
            print("\n表不存在，直接用新结构建表...")
            Base.metadata.create_all(engine, tables=[QMSDefectOrder.__table__])
            print("✓ 建表完成")
            return

        # 判断是否已经迁移过（新结构有 order_id 列，旧结构没有）
        if column_exists(db, "qms_defect_orders", "order_id"):
            print("\n✓ 表已是新结构，无需迁移")
            return

        old_count = db.execute(text('SELECT COUNT(*) FROM qms_defect_orders')).scalar() or 0
        print(f"\n当前记录数: {old_count} 条")
        print("\n将执行：")
        print("  1. 备份旧表 → qms_defect_orders_bak")
        print("  2. 创建新结构表")
        print("  3. 迁移数据（旧 id → 新 order_id）")
        print("  4. 删除备份表")

        confirm = input("\n确定要继续吗？(输入 'yes' 确认): ")
        if confirm.strip().lower() != "yes":
            print("操作已取消")
            return

        # 1. 重命名旧表
        db.execute(text("ALTER TABLE qms_defect_orders RENAME TO qms_defect_orders_bak"))
        db.commit()
        print("\n✓ 旧表已备份为 qms_defect_orders_bak")

        # 2. 用新模型建表
        Base.metadata.create_all(engine, tables=[QMSDefectOrder.__table__])
        print("✓ 新表已创建")

        # 3. 迁移数据：旧 id → 新 order_id
        db.execute(text("""
            INSERT INTO qms_defect_orders
                (order_id, content_hash, entry_time, model, barcode, position,
                 photo_path, status, data_source,
                 customer_id, workshop_id, line_id, station_id, defect_id, inspection_node_id)
            SELECT
                id, content_hash, entry_time, model, barcode, position,
                photo_path, status, data_source,
                customer_id, workshop_id, line_id, station_id, defect_id, inspection_node_id
            FROM qms_defect_orders_bak
        """))
        db.commit()

        new_count = db.execute(text('SELECT COUNT(*) FROM qms_defect_orders')).scalar() or 0
        print(f"✓ 数据迁移完成: {new_count}/{old_count} 条")

        # 4. 删除备份表
        db.execute(text("DROP TABLE qms_defect_orders_bak"))
        db.commit()
        print("✓ 备份表已删除")

        print("\n" + "=" * 60)
        print("迁移完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 迁移失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
