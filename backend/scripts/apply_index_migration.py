"""
应用数据库索引迁移脚本

使用方法：
    python backend/scripts/apply_index_migration.py
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import engine
from sqlalchemy import text

def apply_migration():
    """应用索引迁移"""
    migration_file = Path(__file__).parent.parent / "migrations" / "add_task_query_indexes.sql"
    
    print("="*80)
    print("应用数据库索引迁移")
    print("="*80)
    print(f"\n迁移文件: {migration_file}")
    
    if not migration_file.exists():
        print(f"\n❌ 错误: 迁移文件不存在")
        return False
    
    # 读取 SQL 文件
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 分割 SQL 语句（按分号分割，但跳过注释）
    statements = []
    current_statement = []
    
    for line in sql_content.split('\n'):
        # 跳过纯注释行
        stripped = line.strip()
        if stripped.startswith('--') or not stripped:
            continue
        
        current_statement.append(line)
        
        # 如果行以分号结尾，这是一个完整的语句
        if stripped.endswith(';'):
            statements.append('\n'.join(current_statement))
            current_statement = []
    
    # 添加最后一个语句（如果有）
    if current_statement:
        statements.append('\n'.join(current_statement))
    
    print(f"\n找到 {len(statements)} 条 SQL 语句")
    
    # 执行迁移
    try:
        with engine.connect() as conn:
            print("\n开始执行迁移...")
            
            for i, statement in enumerate(statements, 1):
                # 跳过空语句
                if not statement.strip():
                    continue
                
                # 只显示 CREATE INDEX 语句
                if 'CREATE INDEX' in statement.upper():
                    # 提取索引名称
                    if 'idx_annotation_tasks_dataset_status' in statement:
                        print(f"  [{i}] 创建复合索引: idx_annotation_tasks_dataset_status")
                    elif 'idx_annotation_tasks_created_at' in statement:
                        print(f"  [{i}] 创建时间索引: idx_annotation_tasks_created_at")
                    else:
                        print(f"  [{i}] 创建索引...")
                
                try:
                    conn.execute(text(statement))
                    conn.commit()
                except Exception as e:
                    # 如果索引已存在，继续执行
                    if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
                        print(f"      (索引已存在，跳过)")
                    else:
                        raise
            
            print("\n✓ 迁移执行成功")
            
            # 验证索引
            print("\n验证索引创建:")
            result = conn.execute(text("""
                SELECT name 
                FROM sqlite_master 
                WHERE type='index' 
                  AND tbl_name='annotation_tasks'
                  AND name LIKE 'idx_annotation_tasks_%'
                ORDER BY name
            """))
            
            indexes = result.fetchall()
            for idx in indexes:
                print(f"  ✓ {idx[0]}")
            
            return True
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    success = apply_migration()
    
    if success:
        print("\n" + "="*80)
        print("迁移完成")
        print("="*80)
        print("\n下一步:")
        print("1. 运行性能测试: python backend/scripts/test_index_performance.py")
        print("2. 验证应用功能正常")
        print("3. 监控查询性能")
        print()
    else:
        print("\n迁移失败，请检查错误信息")
        sys.exit(1)


if __name__ == "__main__":
    main()
