"""
Add missing columns to the batch_jobs table.

This script is idempotent and always follows DATABASE_URL from .env.
It no longer falls back to any repo-local annotation.db file.
"""
import os
import sqlite3
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
os.chdir(BACKEND_ROOT)
sys.path.insert(0, str(BACKEND_ROOT))

from config import settings


REQUIRED_COLUMNS = {
    "progress": "REAL DEFAULT 0.0",
    "error_message": "TEXT",
    "created_by": "INTEGER REFERENCES users(id)",
}


def get_sqlite_path_from_url(database_url: str) -> Path:
    """Resolve the SQLite file path from DATABASE_URL."""
    if not database_url:
        raise ValueError("DATABASE_URL 未配置，脚本不会再回退到项目内置 annotation.db")

    if not database_url.startswith("sqlite:///"):
        raise ValueError(f"DATABASE_URL 必须是 SQLite URL，当前为: {database_url}")

    raw_path = database_url.replace("sqlite:///", "", 1)
    path = Path(raw_path)
    if not path.is_absolute():
        path = (BACKEND_ROOT / path).resolve()
    return path


def get_table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    """Return the column names of a table."""
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """Check whether a table exists."""
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return cursor.fetchone() is not None


def migrate_batch_jobs_fields() -> int:
    """Apply the migration and return the number of added columns."""
    db_path = get_sqlite_path_from_url(settings.DATABASE_URL)
    print(f"当前数据库: {db_path}")

    if not db_path.exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")

    added_count = 0

    with sqlite3.connect(db_path) as conn:
        if not table_exists(conn, "batch_jobs"):
            raise RuntimeError("表 batch_jobs 不存在，请先执行 python init_db.py")

        existing_columns = get_table_columns(conn, "batch_jobs")
        print(f"现有字段: {sorted(existing_columns)}")

        for column_name, column_def in REQUIRED_COLUMNS.items():
            if column_name in existing_columns:
                print(f"已存在字段: {column_name}")
                continue

            alter_sql = f"ALTER TABLE batch_jobs ADD COLUMN {column_name} {column_def}"
            conn.execute(alter_sql)
            added_count += 1
            print(f"新增字段: {column_name} ({column_def})")

        if "progress" in REQUIRED_COLUMNS:
            conn.execute("UPDATE batch_jobs SET progress = 0.0 WHERE progress IS NULL")

        conn.commit()
        print(f"迁移后字段: {sorted(get_table_columns(conn, 'batch_jobs'))}")

    return added_count


def main() -> None:
    print("=" * 60)
    print("batch_jobs 字段迁移开始")
    print("=" * 60)

    try:
        added = migrate_batch_jobs_fields()
        print("=" * 60)
        if added == 0:
            print("无需迁移，字段已完整")
        else:
            print(f"迁移完成，新增字段数: {added}")
        print("=" * 60)
    except Exception as exc:
        print(f"迁移失败: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
