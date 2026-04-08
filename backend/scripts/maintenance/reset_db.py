"""
数据库和文件完全重置脚本
删除所有数据、图片和上传文件，然后重新初始化
⚠️ 警告：此操作会删除所有数据和文件，请谨慎使用！

使用方法：
    cd backend
    python reset_db.py
"""
import sys
import os
import shutil
from pathlib import Path

# 添加backend目录到Python路径
BACKEND_ROOT = Path(__file__).resolve().parents[2]  # backend/
os.chdir(BACKEND_ROOT)
sys.path.insert(0, str(BACKEND_ROOT))

from database import engine, Base
from sqlalchemy import text
from config import settings
import init_db


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


def confirm_reset():
    """确认是否重置数据库和文件"""
    print("=" * 60)
    print("⚠️  警告：数据库和文件完全重置")
    print("=" * 60)
    print(f"当前数据库: {get_database_display_path()}")
    print("\n此操作将：")
    print("  1. 删除所有数据库表和数据")
    print("  2. 删除所有图片文件")
    print("  3. 删除所有上传文件（含 file_hashes.json）")
    print("  4. 删除所有导出文件")
    print("  5. 删除 data/processed/ 中间 JSON 文件")
    print("  6. 删除项目内遗留的多余 .db 文件（保留当前 DATABASE_URL 主库）")
    print("  7. 重新创建表结构")
    print("  8. 插入初始数据")
    print("\n⚠️  所有现有数据和文件将永久丢失！\n")
    
    response = input("确认要继续吗？(输入 'YES' 继续): ")
    return response == "YES"


def drop_all_tables():
    """删除所有表"""
    print("\n正在删除所有表...")
    
    # 获取所有表名
    with engine.connect() as conn:
        # SQLite特定的查询
        result = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ))
        tables = [row[0] for row in result]
    
    if tables:
        print(f"找到 {len(tables)} 个表:")
        for table in tables:
            print(f"  - {table}")
        
        # 删除所有表
        Base.metadata.drop_all(bind=engine)
        print("✓ 所有表已删除")
    else:
        print("✓ 没有找到需要删除的表")


def clean_directory(directory: Path, dir_name: str):
    """清理目录中的所有文件"""
    if directory.exists():
        file_count = sum(1 for _ in directory.rglob('*') if _.is_file())
        if file_count > 0:
            print(f"\n正在清理 {dir_name}...")
            print(f"找到 {file_count} 个文件")
            
            # 删除目录中的所有内容
            for item in directory.iterdir():
                if item.is_file():
                    item.unlink()
                    print(f"  - 删除文件: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    print(f"  - 删除目录: {item.name}")
            
            print(f"✓ {dir_name} 已清理")
        else:
            print(f"\n✓ {dir_name} 为空，无需清理")
    else:
        print(f"\n✓ {dir_name} 不存在，无需清理")


def clean_all_files():
    """清理所有文件"""
    print("\n" + "=" * 60)
    print("开始清理文件...")
    print("=" * 60)

    clean_directory(settings.IMAGE_DIR,    "图片目录 (data/images)")
    clean_directory(settings.UPLOAD_DIR,   "上传目录 (data/uploads，含 file_hashes.json)")
    clean_directory(settings.EXPORT_DIR,   "导出目录 (data/exports)")
    clean_directory(settings.PROCESSED_DIR,"中间处理目录 (data/processed)")

    print("\n✓ 所有文件已清理")


def clean_legacy_database_files():
    """删除项目内遗留数据库文件，避免多库歧义。"""
    active_db_path = resolve_sqlite_path(settings.DATABASE_URL)
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
            if active_db_path is not None and file_path == active_db_path:
                continue
            f.unlink()
            print(f"✔ 删除遗留数据库文件: {file_path}")
            removed += 1

    if removed == 0:
        print("✔ 未发现需要删除的遗留数据库文件")


def main():
    """主函数"""
    # 确认操作
    if not confirm_reset():
        print("\n操作已取消")
        return
    
    print("\n" + "=" * 60)
    print("开始重置数据库和文件...")
    print("=" * 60)
    
    try:
        # 1. 删除所有表
        drop_all_tables()

        # 2. 清理所有文件（含 data/processed/ 中间文件）
        clean_all_files()

        # 3. 清理项目内遗留数据库文件（init_db 会重建当前主库）
        clean_legacy_database_files()

        # 4. 重新初始化数据库
        print("\n" + "=" * 60)
        print("正在重新初始化数据库...")
        print("=" * 60)
        init_db.main()
        
        print("\n" + "=" * 60)
        print("✓ 数据库和文件重置完成！")
        print("=" * 60)
        print("\n系统已恢复到初始状态：")
        print("  - 数据库表已重建")
        print("  - 初始数据已插入")
        print("  - 所有文件已清理")
        print("\n可以重新开始使用系统。")
        
    except Exception as e:
        print(f"\n✗ 重置失败: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
