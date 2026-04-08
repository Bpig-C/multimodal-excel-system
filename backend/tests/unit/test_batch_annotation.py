"""
批量标注服务测试 (Task 14)
测试批量标注服务功能
"""
import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """测试导入"""
    print("1. 测试批量标注服务导入...")
    try:
        from services.batch_annotation_service import BatchAnnotationService
        print("✓ 批量标注服务导入成功")
    except Exception as e:
        print(f"✗ 导入失败: {e}")

        raise


def test_service_methods():
    """测试服务方法"""
    print("\n2. 测试批量标注服务方法...")
    try:
        from services.batch_annotation_service import BatchAnnotationService
        from database import SessionLocal
        
        # 创建数据库会话
        db = SessionLocal()
        
        try:
            # 创建服务实例
            service = BatchAnnotationService(db)
            
            # 测试方法存在
            required_methods = [
                'create_batch_job',
                'get_batch_job',
                'update_batch_job_status',
                'execute_batch_annotation',
                'cancel_batch_job',
                'get_batch_job_statistics',
            ]
            
            for method in required_methods:
                assert hasattr(service, method), f"缺少{method}方法"
                print(f"  ✓ {method}")
            
            print("✓ 批量标注服务方法完整")
        finally:
            db.close()
    except Exception as e:
        print(f"✗ 服务方法测试失败: {e}")

        raise


def test_database_models():
    """测试数据库模型"""
    print("\n3. 测试批量任务数据库模型...")
    try:
        from models.db_models import BatchJob
        
        # 检查BatchJob模型字段
        required_fields = [
            'id', 'job_id', 'dataset_id', 'status',
            'total_tasks', 'completed_tasks', 'failed_tasks',
            'started_at', 'completed_at', 'created_at'
        ]
        
        for field in required_fields:
            assert hasattr(BatchJob, field), f"BatchJob缺少字段: {field}"
            print(f"  ✓ {field}")
        
        print("✓ BatchJob模型字段完整")
    except Exception as e:
        print(f"✗ 数据库模型测试失败: {e}")

        raise


def test_agent_integration():
    """测试Agent集成"""
    print("\n4. 测试Agent集成...")
    try:
        from services.batch_annotation_service import BatchAnnotationService
        from agents.entity_extraction import EntityExtractionAgent
        from agents.relation_extraction import RelationExtractionAgent
        
        print("  ✓ EntityExtractionAgent")
        print("  ✓ RelationExtractionAgent")
        print("✓ Agent集成正常")
    except Exception as e:
        print(f"✗ Agent集成测试失败: {e}")

        raise


def test_async_support():
    """测试异步支持"""
    print("\n5. 测试异步支持...")
    try:
        from services.batch_annotation_service import BatchAnnotationService
        import inspect
        
        # 检查execute_batch_annotation是否是异步方法
        method = getattr(BatchAnnotationService, 'execute_batch_annotation')
        is_async = inspect.iscoroutinefunction(method)
        
        if is_async:
            print("✓ execute_batch_annotation是异步方法")
        else:
            print("✗ execute_batch_annotation不是异步方法")

            raise
    except Exception as e:
        print(f"✗ 异步支持测试失败: {e}")

        raise


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Task 14: 批量标注服务测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_service_methods,
        test_database_models,
        test_agent_integration,
        test_async_support,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ 测试执行失败: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ 所有测试通过!")
    else:
        print(f"✗ {results.count(False)} 个测试失败")
    print("=" * 60)
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
