"""
检查数据库中的分配记录
"""
import sqlite3
from pathlib import Path

from config import settings


def resolve_sqlite_path() -> Path:
    """Resolve the current SQLite database path from DATABASE_URL."""
    db_url = settings.DATABASE_URL
    if not db_url.startswith("sqlite:///"):
        raise ValueError(f"当前 DATABASE_URL 不是 SQLite: {db_url}")

    raw_path = Path(db_url.replace("sqlite:///", "", 1))
    if raw_path.is_absolute():
        return raw_path.resolve()
    return (Path(__file__).resolve().parent / raw_path).resolve()


DB_PATH = resolve_sqlite_path()

def check_database():
    """检查数据库中的分配记录"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("=" * 80)
    print("1. 检查所有用户")
    print("=" * 80)
    cursor.execute("""
        SELECT id, username, role, created_at
        FROM users
        ORDER BY id
    """)
    users = cursor.fetchall()
    print(f"\n找到 {len(users)} 个用户：")
    for user in users:
        print(f"  ID: {user[0]}, 用户名: {user[1]}, 角色: {user[2]}, 创建时间: {user[3]}")
    
    print("\n" + "=" * 80)
    print("2. 检查所有数据集")
    print("=" * 80)
    cursor.execute("""
        SELECT id, dataset_id, name, created_by, created_at
        FROM datasets
        ORDER BY id
    """)
    datasets = cursor.fetchall()
    print(f"\n找到 {len(datasets)} 个数据集：")
    for ds in datasets:
        print(f"  ID: {ds[0]}, dataset_id: {ds[1]}, 名称: {ds[2]}, 创建者: {ds[3]}")
    
    print("\n" + "=" * 80)
    print("3. 检查所有活跃的分配记录")
    print("=" * 80)
    cursor.execute("""
        SELECT 
            da.id,
            d.dataset_id,
            d.name as dataset_name,
            u.username,
            da.role,
            da.task_start_index,
            da.task_end_index,
            da.is_active,
            da.assigned_at
        FROM dataset_assignments da
        JOIN datasets d ON da.dataset_id = d.id
        JOIN users u ON da.user_id = u.id
        WHERE da.is_active = 1
        ORDER BY da.assigned_at DESC
    """)
    assignments = cursor.fetchall()
    
    if assignments:
        print(f"\n找到 {len(assignments)} 个活跃分配：")
        for assign in assignments:
            print(f"\n  分配ID: {assign[0]}")
            print(f"  数据集: {assign[1]} ({assign[2]})")
            print(f"  用户: {assign[3]}")
            print(f"  角色: {assign[4]}")
            print(f"  任务范围: {assign[5]}-{assign[6]}")
            print(f"  分配时间: {assign[8]}")
    else:
        print("\n❌ 没有找到任何活跃的分配记录！")
        print("\n这就是为什么标注员看不到数据集的原因。")
        print("请确保：")
        print("1. 在管理员界面完成了分配")
        print("2. 点击了'确认提交'按钮")
        print("3. 看到了'分配提交成功'的提示")
    
    print("\n" + "=" * 80)
    print("4. 检查所有分配记录（包括不活跃的）")
    print("=" * 80)
    cursor.execute("""
        SELECT 
            da.id,
            d.dataset_id,
            u.username,
            da.role,
            da.is_active,
            da.assigned_at
        FROM dataset_assignments da
        JOIN datasets d ON da.dataset_id = d.id
        JOIN users u ON da.user_id = u.id
        ORDER BY da.assigned_at DESC
    """)
    all_assignments = cursor.fetchall()
    
    if all_assignments:
        print(f"\n找到 {len(all_assignments)} 个分配记录（包括不活跃的）：")
        for assign in all_assignments:
            status = "✓ 活跃" if assign[4] else "✗ 不活跃"
            print(f"  {status} - 用户: {assign[2]}, 角色: {assign[3]}, 数据集: {assign[1]}")
    else:
        print("\n❌ 数据库中完全没有分配记录！")
    
    conn.close()

if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"❌ 数据库文件不存在: {DB_PATH}")
    else:
        print(f"✓ 数据库文件: {DB_PATH}\n")
        check_database()
