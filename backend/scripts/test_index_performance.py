"""
测试数据库索引性能
用于验证 add_task_query_indexes.sql 迁移脚本的效果

使用方法：
1. 先运行迁移脚本创建索引
2. 运行此脚本测试性能
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import get_db, engine
from models.db_models import AnnotationTask
import random

def test_index_exists():
    """测试索引是否存在"""
    print("\n" + "="*80)
    print("测试 1: 验证索引是否存在")
    print("="*80)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type='index' AND tbl_name='annotation_tasks'
            ORDER BY name
        """))
        
        indexes = result.fetchall()
        
        expected_indexes = [
            'idx_annotation_tasks_dataset_status',
            'idx_annotation_tasks_created_at'
        ]
        
        found_indexes = [idx[0] for idx in indexes if idx[0]]
        
        print(f"\n找到的索引 ({len(found_indexes)}):")
        for idx in indexes:
            if idx[0]:  # 跳过 None（自动创建的索引）
                print(f"  ✓ {idx[0]}")
                if idx[1]:
                    print(f"    定义: {idx[1]}")
        
        # 验证必需的索引
        missing = []
        for expected in expected_indexes:
            if expected not in found_indexes:
                missing.append(expected)
        
        if missing:
            print(f"\n❌ 缺少索引: {', '.join(missing)}")
            print("请先运行迁移脚本: backend/migrations/add_task_query_indexes.sql")
            return False
        else:
            print(f"\n✓ 所有必需的索引都已创建")
            return True


def test_query_performance():
    """测试查询性能"""
    print("\n" + "="*80)
    print("测试 2: 查询性能测试")
    print("="*80)
    
    db = next(get_db())
    
    try:
        # 获取任务总数
        total_tasks = db.query(AnnotationTask).count()
        print(f"\n当前任务总数: {total_tasks}")
        
        if total_tasks == 0:
            print("⚠️  数据库中没有任务数据，无法进行性能测试")
            return
        
        # 获取一个存在的 dataset_id
        sample_task = db.query(AnnotationTask).first()
        if not sample_task:
            print("⚠️  无法获取示例任务")
            return
        
        dataset_id = sample_task.dataset_id
        
        # 测试 1: 按数据集和状态筛选
        print(f"\n测试查询 1: 按数据集和状态筛选")
        print(f"  WHERE dataset_id = {dataset_id} AND status = 'pending'")
        
        start_time = time.time()
        results = db.query(AnnotationTask).filter(
            AnnotationTask.dataset_id == dataset_id,
            AnnotationTask.status == 'pending'
        ).all()
        elapsed = (time.time() - start_time) * 1000
        
        print(f"  结果数量: {len(results)}")
        print(f"  查询时间: {elapsed:.2f} ms")
        
        # 测试 2: 按时间排序
        print(f"\n测试查询 2: 按创建时间排序（分页）")
        print(f"  ORDER BY created_at DESC LIMIT 20")
        
        start_time = time.time()
        results = db.query(AnnotationTask).order_by(
            AnnotationTask.created_at.desc()
        ).limit(20).all()
        elapsed = (time.time() - start_time) * 1000
        
        print(f"  结果数量: {len(results)}")
        print(f"  查询时间: {elapsed:.2f} ms")
        
        # 测试 3: 复杂查询（数据集 + 状态 + 排序）
        print(f"\n测试查询 3: 复合条件查询")
        print(f"  WHERE dataset_id = {dataset_id} AND status IN ('pending', 'in_progress')")
        print(f"  ORDER BY created_at DESC LIMIT 20")
        
        start_time = time.time()
        results = db.query(AnnotationTask).filter(
            AnnotationTask.dataset_id == dataset_id,
            AnnotationTask.status.in_(['pending', 'in_progress'])
        ).order_by(
            AnnotationTask.created_at.desc()
        ).limit(20).all()
        elapsed = (time.time() - start_time) * 1000
        
        print(f"  结果数量: {len(results)}")
        print(f"  查询时间: {elapsed:.2f} ms")
        
        # 性能评估
        print(f"\n性能评估:")
        if total_tasks < 1000:
            print(f"  数据集规模: 小型 ({total_tasks} 条)")
            print(f"  预期查询时间: < 10 ms")
        elif total_tasks < 10000:
            print(f"  数据集规模: 中型 ({total_tasks} 条)")
            print(f"  预期查询时间: < 50 ms")
        else:
            print(f"  数据集规模: 大型 ({total_tasks} 条)")
            print(f"  预期查询时间: < 100 ms")
        
        if elapsed < 10:
            print(f"  ✓ 查询性能优秀")
        elif elapsed < 50:
            print(f"  ✓ 查询性能良好")
        elif elapsed < 100:
            print(f"  ⚠️  查询性能一般")
        else:
            print(f"  ❌ 查询性能较差，可能需要进一步优化")
        
    finally:
        db.close()


def test_explain_query_plan():
    """测试查询计划，验证是否使用了索引"""
    print("\n" + "="*80)
    print("测试 3: 查询计划分析（验证索引使用）")
    print("="*80)
    
    with engine.connect() as conn:
        # 获取一个示例 dataset_id
        result = conn.execute(text("SELECT dataset_id FROM annotation_tasks LIMIT 1"))
        row = result.fetchone()
        
        if not row:
            print("⚠️  数据库中没有任务数据")
            return
        
        dataset_id = row[0]
        
        # 测试查询计划
        queries = [
            {
                'name': '按数据集和状态筛选',
                'sql': f"""
                    SELECT * FROM annotation_tasks 
                    WHERE dataset_id = {dataset_id} AND status = 'pending'
                """
            },
            {
                'name': '按时间排序',
                'sql': """
                    SELECT * FROM annotation_tasks 
                    ORDER BY created_at DESC 
                    LIMIT 20
                """
            },
            {
                'name': '复合查询',
                'sql': f"""
                    SELECT * FROM annotation_tasks 
                    WHERE dataset_id = {dataset_id} AND status IN ('pending', 'in_progress')
                    ORDER BY created_at DESC 
                    LIMIT 20
                """
            }
        ]
        
        for query in queries:
            print(f"\n查询: {query['name']}")
            print(f"SQL: {query['sql'].strip()}")
            print(f"\n查询计划:")
            
            result = conn.execute(text(f"EXPLAIN QUERY PLAN {query['sql']}"))
            plan = result.fetchall()
            
            uses_index = False
            for row in plan:
                print(f"  {row}")
                # 检查是否使用了我们创建的索引
                if 'idx_annotation_tasks_dataset_status' in str(row) or \
                   'idx_annotation_tasks_created_at' in str(row):
                    uses_index = True
            
            if uses_index:
                print(f"  ✓ 使用了优化索引")
            else:
                print(f"  ⚠️  未使用优化索引（可能使用了其他索引或全表扫描）")


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("数据库索引性能测试")
    print("="*80)
    
    # 测试 1: 验证索引存在
    if not test_index_exists():
        print("\n❌ 索引验证失败，请先运行迁移脚本")
        return
    
    # 测试 2: 查询性能测试
    test_query_performance()
    
    # 测试 3: 查询计划分析
    test_explain_query_plan()
    
    print("\n" + "="*80)
    print("测试完成")
    print("="*80)
    print("\n建议:")
    print("1. 如果查询性能不理想，可以运行 ANALYZE 命令更新统计信息")
    print("2. 定期监控查询性能，特别是在数据量增长后")
    print("3. 考虑添加更多索引以优化特定查询场景")
    print()


if __name__ == "__main__":
    main()
