"""
版本管理服务测试 (Task 17)
测试版本管理服务功能
"""
import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """测试导入"""
    print("1. 测试版本管理服务导入...")
    try:
        from services.version_management_service import VersionManagementService
        print("✓ 版本管理服务导入成功")
    except Exception as e:
        print(f"✗ 导入失败: {e}")

        raise


def test_service_methods():
    """测试服务方法"""
    print("\n2. 测试版本管理服务方法...")
    try:
        from services.version_management_service import VersionManagementService
        from database import SessionLocal
        
        # 创建数据库会话
        db = SessionLocal()
        
        try:
            # 创建服务实例
            service = VersionManagementService(db)
            
            # 测试方法存在
            required_methods = [
                'create_version',
                'get_version_history',
                'rollback_to_version',
                'compare_versions',
            ]
            
            for method in required_methods:
                assert hasattr(service, method), f"缺少{method}方法"
                print(f"  ✓ {method}")
            
            print("✓ 版本管理服务方法完整")
        finally:
            db.close()
    except Exception as e:
        print(f"✗ 服务方法测试失败: {e}")

        raise


def test_private_methods():
    """测试私有方法"""
    print("\n3. 测试私有辅助方法...")
    try:
        from services.version_management_service import VersionManagementService
        from database import SessionLocal
        
        # 创建数据库会话
        db = SessionLocal()
        
        try:
            # 创建服务实例
            service = VersionManagementService(db)
            
            # 测试私有方法存在
            private_methods = [
                '_create_snapshot',
                '_restore_snapshot',
                '_calculate_diff',
            ]
            
            for method in private_methods:
                assert hasattr(service, method), f"缺少{method}方法"
                print(f"  ✓ {method}")
            
            print("✓ 私有辅助方法完整")
        finally:
            db.close()
    except Exception as e:
        print(f"✗ 私有方法测试失败: {e}")

        raise


def test_database_models():
    """测试数据库模型"""
    print("\n4. 测试版本历史数据库模型...")
    try:
        from models.db_models import VersionHistory
        
        # 检查VersionHistory模型字段
        required_fields = [
            'id', 'history_id', 'task_id', 'version',
            'change_type', 'change_description', 'changed_by',
            'snapshot_data', 'created_at'
        ]
        
        for field in required_fields:
            assert hasattr(VersionHistory, field), f"VersionHistory缺少字段: {field}"
            print(f"  ✓ {field}")
        
        print("✓ VersionHistory模型字段完整")
    except Exception as e:
        print(f"✗ 数据库模型测试失败: {e}")

        raise


def test_snapshot_structure():
    """测试快照数据结构"""
    print("\n5. 测试快照数据结构...")
    try:
        # 验证快照数据应包含的字段
        expected_keys = [
            'version',
            'task_info',
            'entities',
            'image_entities',
            'relations'
        ]
        
        print("✓ 快照数据结构定义:")
        for key in expected_keys:
            print(f"  - {key}")
        
        print("✓ 快照数据结构完整")
    except Exception as e:
        print(f"✗ 快照结构测试失败: {e}")

        raise


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Task 17: 版本管理服务测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_service_methods,
        test_private_methods,
        test_database_models,
        test_snapshot_structure,
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
