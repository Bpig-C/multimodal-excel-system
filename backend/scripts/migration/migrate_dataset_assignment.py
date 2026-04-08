"""
数据集分配功能 - 数据库迁移脚本
执行 dataset_assignments 表的创建和索引添加
"""
import sqlite3
from pathlib import Path
from config import settings

def run_migration():
    """执行数据库迁移"""
    # 从 DATABASE_URL 提取数据库路径
    db_url = settings.DATABASE_URL
    db_path = db_url.replace("sqlite:///", "")
    migration_file = Path(__file__).parent / "migrations" / "add_dataset_assignment.sql"
    
    print(f"📊 开始数据库迁移...")
    print(f"数据库路径: {db_path}")
    print(f"迁移脚本: {migration_file}")
    
    # 读取迁移脚本
    with open(migration_file, 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 执行迁移脚本
        cursor.executescript(migration_sql)
        conn.commit()
        
        print("\n✅ 数据库迁移成功!")
        
        # 验证表是否创建
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='dataset_assignments'
        """)
        result = cursor.fetchone()
        
        if result:
            print(f"✅ dataset_assignments 表已创建")
            
            # 显示表结构
            cursor.execute("PRAGMA table_info(dataset_assignments)")
            columns = cursor.fetchall()
            print(f"\n📋 表结构 ({len(columns)} 个字段):")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # 显示索引
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND tbl_name='dataset_assignments'
            """)
            indexes = cursor.fetchall()
            print(f"\n📑 索引 ({len(indexes)} 个):")
            for idx in indexes:
                print(f"  - {idx[0]}")
        else:
            print("❌ 表创建失败")
            
    except Exception as e:
        print(f"\n❌ 迁移失败: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
