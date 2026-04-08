"""
版本管理API测试 (Task 18)
测试版本管理API端点
"""
import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)


def test_imports():
    """测试导入"""
    print("1. 测试版本管理API导入...")
    try:
        from api.versions import router
        print("✓ 版本管理API导入成功")
    except Exception as e:
        print(f"✗ 导入失败: {e}")

        raise


def test_router_endpoints():
    """测试路由端点"""
    print("\n2. 测试路由端点...")
    try:
        from api.versions import router
        
        # 获取所有路由
        routes = [route.path for route in router.routes]
        
        print(f"✓ 找到 {len(routes)} 个路由端点")
        
        # 检查关键端点
        expected_endpoints = [
            "/api/v1/versions/{task_id}",
            "/api/v1/versions/{task_id}/rollback",
            "/api/v1/versions/compare",
        ]
        
        for endpoint in expected_endpoints:
            matching = [r for r in routes if endpoint in r or r.startswith(endpoint.split('{')[0])]
            if matching:
                print(f"  ✓ {endpoint}")
            else:
                print(f"  ✗ 缺少端点: {endpoint}")
    except Exception as e:
        print(f"✗ 路由端点测试失败: {e}")

        raise


def test_api_methods():
    """测试API方法"""
    print("\n3. 测试API方法...")
    try:
        from api.versions import router
        
        # 统计不同HTTP方法的端点数量
        methods_count = {}
        for route in router.routes:
            for method in route.methods:
                methods_count[method] = methods_count.get(method, 0) + 1
        
        print("✓ API方法统计:")
        for method, count in sorted(methods_count.items()):
            print(f"  - {method}: {count}个端点")
        
        # 验证至少有GET和POST方法
        required_methods = ['GET', 'POST']
        for method in required_methods:
            if method in methods_count:
                print(f"  ✓ 包含{method}方法")
            else:
                print(f"  ✗ 缺少{method}方法")

                raise
    except Exception as e:
        print(f"✗ API方法测试失败: {e}")

        raise


def test_api_registration():
    """测试API注册"""
    print("\n4. 测试API注册...")
    try:
        from api import versions_router
        print("✓ 版本管理路由已在api包中注册")
    except Exception as e:
        print(f"✗ API注册测试失败: {e}")

        raise


def test_service_integration():
    """测试服务集成"""
    print("\n5. 测试服务集成...")
    try:
        from api.versions import router
        from services.version_management_service import VersionManagementService
        
        print("  ✓ VersionManagementService集成")
        print("✓ 服务集成正常")
    except Exception as e:
        print(f"✗ 服务集成测试失败: {e}")

        raise


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Task 18: 版本管理API测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_router_endpoints,
        test_api_methods,
        test_api_registration,
        test_service_integration,
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
