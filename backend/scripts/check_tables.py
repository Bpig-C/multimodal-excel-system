import sqlite3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Settings

settings = Settings()
db_path = settings.DATABASE_URL.replace('sqlite:///', '')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print("数据库中的表:")
for table in tables:
    print(f"  - {table}")
    
# 检查 batch_jobs 表
if 'batch_jobs' in tables:
    cursor.execute("PRAGMA table_info(batch_jobs)")
    columns = cursor.fetchall()
    print("\nbatch_jobs 表结构:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
else:
    print("\n❌ batch_jobs 表不存在！")

conn.close()
