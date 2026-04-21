"""
清除数据库中的 QMS 类型数据

删除范围：
  - qms_defect_orders        QMS不合格品记录（主表）
  - qms_inspection_nodes     QMS质检节点（维表）
  - qms_stations             QMS岗位（维表）
  - qms_production_lines     QMS产线（维表）
  - qms_workshops            QMS车间（维表）

不删除：
  - customers / defects      与 KF 共用的维表，保留
  - KF 快反数据
  - 所有语料 / 数据集 / 标注任务
  - 用户 / 标签配置
  - data/processed/qms/      中间 JSON 文件（需手动清理或使用 --purge-files 选项）
"""
import sys
import os
import shutil
import argparse
from pathlib import Path
from sqlalchemy import text

BACKEND_ROOT = Path(__file__).resolve().parents[2]  # backend/
os.chdir(BACKEND_ROOT)
sys.path.insert(0, str(BACKEND_ROOT))

from database import SessionLocal
from config import settings


def resolve_sqlite_path(db_url: str) -> Path | None:
    if not db_url.startswith("sqlite:///"):
        return None
    raw_path = Path(db_url.replace("sqlite:///", "", 1))
    if raw_path.is_absolute():
        return raw_path.resolve()
    return (BACKEND_ROOT / raw_path).resolve()


def get_database_display_path() -> str:
    p = resolve_sqlite_path(settings.DATABASE_URL)
    return str(p) if p else settings.DATABASE_URL


# 按外键依赖顺序排列：先删引用表，再删维表
QMS_TABLES = [
    ("qms_defect_orders",    "QMS不合格品记录"),
    ("qms_inspection_nodes", "QMS质检节点"),
    ("qms_stations",         "QMS岗位"),
    ("qms_production_lines", "QMS产线"),
    ("qms_workshops",        "QMS车间"),
]


def delete_qms_data(db) -> dict[str, int]:
    """删除所有 QMS 相关表数据，返回各表删除数量。"""
    results = {}
    for table_name, label in QMS_TABLES:
        exists = db.execute(
            text("SELECT 1 FROM sqlite_master WHERE type='table' AND name=:n"),
            {"n": table_name},
        ).first()
        if not exists:
            print(f"  - 表 {table_name} 不存在，跳过")
            continue

        count = db.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar() or 0
        if count > 0:
            db.execute(text(f'DELETE FROM "{table_name}"'))
            print(f"  ✓ 删除了 {count:>6} 条 {label} ({table_name})")
        else:
            print(f"  - {label} ({table_name}) 无数据，跳过")
        results[table_name] = count

    db.commit()
    return results


def purge_qms_files():
    """清空 data/processed/qms/ 目录下的中间 JSON 文件。"""
    qms_dir: Path = settings.PROCESSED_DIR / "qms"
    if not qms_dir.exists():
        print(f"  - 目录不存在，跳过: {qms_dir}")
        return
    shutil.rmtree(qms_dir, ignore_errors=True)
    qms_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ 已清空中间文件目录: {qms_dir}")

    # 同时清理上传目录中的 qms 上传文件
    qms_upload_dir: Path = settings.UPLOAD_DIR / "qms"
    if qms_upload_dir.exists():
        shutil.rmtree(qms_upload_dir, ignore_errors=True)
        qms_upload_dir.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ 已清空上传目录: {qms_upload_dir}")


def main():
    parser = argparse.ArgumentParser(description="清除数据库中的 QMS 类型数据")
    parser.add_argument(
        "--purge-files",
        action="store_true",
        help="同时清空 data/processed/qms/ 和 data/uploads/qms/ 目录",
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="跳过确认提示，直接执行",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("⚠️  将删除数据库中所有 QMS 类型数据")
    print("=" * 60)
    print(f"当前数据库: {get_database_display_path()}")
    print("\n将要删除:")
    for _, label in QMS_TABLES:
        print(f"  - {label}")
    if args.purge_files:
        print("  - data/processed/qms/  中间 JSON 文件")
        print("  - data/uploads/qms/    上传文件")
    print("\n不会删除:")
    print("  - customers / defects（与 KF 共用的维表）")
    print("  - KF 快反数据")
    print("  - 语料 / 数据集 / 标注任务")
    print("  - 用户 / 标签配置")

    if not args.yes:
        confirm = input("\n确定要继续吗？(输入 'yes' 确认): ")
        if confirm.strip().lower() != "yes":
            print("\n操作已取消")
            return

    db = SessionLocal()
    try:
        print("\n开始清理数据库...")
        results = delete_qms_data(db)
        total = sum(results.values())

        if args.purge_files:
            print("\n开始清理文件...")
            purge_qms_files()

        print("\n" + "=" * 60)
        print(f"✓ QMS 数据清理完成，共删除 {total} 条记录")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 清理失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
