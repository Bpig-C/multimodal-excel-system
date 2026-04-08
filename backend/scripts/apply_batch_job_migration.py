"""
应用批量任务表字段迁移
添加 progress, error_message, created_by 字段
"""
import sqlite3
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Settings

def apply_migration():
    """应用迁移"""
    settings = Settings()
    # 从 DATABASE_URL 提取数据库文件路径
    db_path = settings.DATABASE_URL.replace('sqlite:///', '')
    
    print(f"数据库路径: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"错误: 数据库文件不存在: {db_path}")
        return False
    
    # 读取迁移SQL
    migration_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'migrations',
        'add_batch_job_fields.sql'
    )
    
    if not os.path.exists(migration_file):
        print(f"错误: 迁移文件不存在: {migration_file}")
        return False
    
    with open(migration_file, 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(batch_jobs)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"当前 batch_jobs 表字段: {columns}")
        
        fields_to_add = ['progress', 'error_message', 'created_by']
        missing_fields = [f for f in fields_to_add if f not in columns]
        
        if not missing_fields:
            print("✅ 所有字段已存在，无需迁移")
            return True
        
        print(f"需要添加的字段: {missing_fields}")
        
        # 执行迁移
        # 分割SQL语句并逐个执行
        statements = [s.strip() for s in migration_sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                print(f"执行: {statement[:100]}...")
                try:
                    cursor.execute(statement)
                except sqlite3.OperationalError as e:
                    if 'duplicate column name' in str(e).lower():
                        print(f"  ⚠️  字段已存在，跳过")
                    else:
                        raise
        
        conn.commit()
        
        # 验证迁移
        cursor.execute("PRAGMA table_info(batch_jobs)")
        columns_after = [row[1] for row in cursor.fetchall()]
        
        print(f"\n迁移后 batch_jobs 表字段: {columns_after}")
        
        # 检查所有字段是否都存在
        all_present = all(f in columns_after for f in fields_to_add)
        
        if all_present:
            print("\n✅ 迁移成功！所有字段已添加")
            return True
        else:
            print("\n❌ 迁移失败！部分字段未添加")
            return False
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("批量任务表字段迁移")
    print("=" * 60)
    
    success = apply_migration()
    
    if success:
        print("\n✅ 迁移完成")
        sys.exit(0)
    else:
        print("\n❌ 迁移失败")
        sys.exit(1)
