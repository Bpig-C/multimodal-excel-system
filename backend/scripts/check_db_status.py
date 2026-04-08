"""检查数据库状态"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # 检查所有表
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
    tables = [row[0] for row in result.fetchall()]
    
    print("数据库中的表:")
    for table in tables:
        print(f"  - {table}")
    
    # 检查 annotation_tasks 表是否存在
    if 'annotation_tasks' in tables:
        print("\n✓ annotation_tasks 表存在")
        
        # 检查现有索引
        result = conn.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND tbl_name='annotation_tasks'
            ORDER BY name
        """))
        indexes = [row[0] for row in result.fetchall() if row[0]]
        
        print(f"\n现有索引 ({len(indexes)}):")
        for idx in indexes:
            print(f"  - {idx}")
    else:
        print("\n❌ annotation_tasks 表不存在")
        print("需要先初始化数据库")
