"""
强制清理数据库
删除所有数据集、语料、图片等数据，保留用户和标签配置
"""
import sys
import os
import shutil
from pathlib import Path
from sqlalchemy import text

# 添加backend目录到Python路径
BACKEND_ROOT = Path(__file__).resolve().parents[2]  # backend/
os.chdir(BACKEND_ROOT)
sys.path.insert(0, str(BACKEND_ROOT))

from database import SessionLocal
from config import settings


def resolve_sqlite_path(db_url: str) -> Path | None:
    """Resolve the SQLite file path for the current DATABASE_URL."""
    if not db_url.startswith("sqlite:///"):
        return None

    raw_path = Path(db_url.replace("sqlite:///", "", 1))
    if raw_path.is_absolute():
        return raw_path.resolve()
    return (BACKEND_ROOT / raw_path).resolve()


def get_database_display_path() -> str:
    """获取当前数据库的可读路径（优先显示SQLite绝对路径）"""
    sqlite_path = resolve_sqlite_path(settings.DATABASE_URL)
    if sqlite_path is not None:
        return str(sqlite_path)
    return settings.DATABASE_URL


def force_clean_all_data(db):
    """强制清理所有业务数据"""
    print("\n开始清理数据...")

    cleanup_plan = [
        ("batch_jobs", "批量任务"),
        ("version_history", "版本历史记录"),
        ("review_tasks", "复核任务"),
        ("relations", "关系"),
        ("image_entities", "图片实体"),
        ("text_entities", "文本实体"),
        ("annotation_tasks", "标注任务"),
        ("quick_response_events", "KF快反事件"),
        ("qms_defect_orders", "QMS不合格品记录"),
        ("dataset_corpus", "数据集-语料关联"),
        ("dataset_assignments", "数据集分配"),
        ("datasets", "数据集"),
        ("images", "图片记录"),
        ("corpus", "语料"),
        ("products", "产品型号"),
        ("root_causes", "异常原因"),
        ("four_m_elements", "4M要素"),
        ("qms_production_lines", "QMS产线"),
        ("qms_workshops", "QMS车间"),
        ("qms_stations", "QMS岗位"),
        ("qms_inspection_nodes", "QMS质检节点"),
        ("customers", "客户"),
        ("defects", "缺陷类型"),
    ]

    for table_name, label in cleanup_plan:
        exists = db.execute(
            text("SELECT 1 FROM sqlite_master WHERE type='table' AND name=:name"),
            {"name": table_name}
        ).first()

        if not exists:
            continue

        count = db.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar() or 0
        if count > 0:
            db.execute(text(f'DELETE FROM "{table_name}"'))
            print(f"✓ 删除了 {count} 个{label}")

    db.commit()
    print("\n✓ 数据清理完成！")
    print("\n保留的数据:")
    print("  - 用户账户")
    print("  - 实体类型配置")
    print("  - 关系类型配置")
    print("  - 标签体系版本")


def clean_extra_databases():
    """清理项目内遗留的歧义数据库文件，保留当前活动主库。"""
    main_db_path = resolve_sqlite_path(settings.DATABASE_URL)
    candidate_dirs = [
        settings.DATABASE_DIR.resolve(),
        (BACKEND_ROOT / "data" / "database").resolve(),
        (BACKEND_ROOT / "data").resolve(),
    ]

    seen_dirs = set()
    removed = 0
    for db_dir in candidate_dirs:
        if db_dir in seen_dirs or not db_dir.exists():
            continue
        seen_dirs.add(db_dir)

        for f in db_dir.glob("*.db"):
            file_path = f.resolve()
            if main_db_path is not None and file_path == main_db_path:
                continue
            f.unlink()
            print(f"✔ 删除歧义数据库文件: {file_path}")
            removed += 1

    if removed == 0:
        print("✔ 未发现需要清理的歧义数据库文件")


def clean_file_storage():
    """清空业务文件（图片、上传、导出、中间处理文件）。"""
    dirs = [
        (settings.IMAGE_DIR,    "图片目录 (data/images)"),
        (settings.UPLOAD_DIR,   "上传目录 (data/uploads，含 file_hashes.json)"),
        (settings.EXPORT_DIR,   "导出目录 (data/exports)"),
        (settings.PROCESSED_DIR,"中间处理目录 (data/processed)"),
    ]
    for path, label in dirs:
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✔ 已清空{label}: {path}")


def main():
    """主函数"""
    print("=" * 60)
    print("⚠️  警告：此操作将删除所有业务数据！")
    print("=" * 60)
    print(f"当前数据库: {get_database_display_path()}")
    print("\n将要删除:")
    print("  - 所有数据集")
    print("  - 所有语料")
    print("  - 所有图片")
    print("  - 所有标注任务")
    print("  - 所有复核任务")
    print("  - 所有版本历史")
    print("  - 所有 KF/QMS 业务记录和维表")
    print("  - data/processed/ 中间 JSON 文件")
    print("  - 项目内遗留的多余 .db 文件（保留当前 DATABASE_URL 主库）")
    print("\n将会保留:")
    print("  - 用户账户")
    print("  - 标签配置（实体类型、关系类型）")
    
    confirm = input("\n确定要继续吗？(输入 'yes' 确认): ")
    
    if confirm.lower() != 'yes':
        print("\n操作已取消")
        return
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        force_clean_all_data(db)
        clean_file_storage()
        clean_extra_databases()
        
        print("\n" + "=" * 60)
        print("清理完成！现在可以重新上传数据。")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 清理失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
