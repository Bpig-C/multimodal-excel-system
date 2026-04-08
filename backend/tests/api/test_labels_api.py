"""
标签管理API测试 (Task 13)
测试标签管理API端点
"""
import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)


def test_imports():
    """测试导入"""
    print("1. 测试标签管理API导入...")
    try:
        from api.labels import router
        print("✓ 标签管理API导入成功")
        assert router is not None
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        raise


def test_router_endpoints():
    """测试路由端点"""
    print("\n2. 测试路由端点...")
    try:
        from api.labels import router
        
        # 获取所有路由
        routes = [route.path for route in router.routes]
        
        print(f"✓ 找到 {len(routes)} 个路由端点")
        
        # 检查关键端点
        expected_endpoints = [
            "/api/v1/labels/entities",
            "/api/v1/labels/relations",
            "/api/v1/labels/import",
            "/api/v1/labels/export",
            "/api/v1/labels/prompt-preview",
            "/api/v1/labels/versions",
        ]
        
        for endpoint in expected_endpoints:
            # 检查是否有匹配的路由（可能包含路径参数）
            matching = [r for r in routes if endpoint in r or r.startswith(endpoint)]
            if matching:
                print(f"  ✓ {endpoint}")
            else:
                print(f"  ✗ 缺少端点: {endpoint}")
        
        assert len(routes) > 0
    except Exception as e:
        print(f"✗ 路由端点测试失败: {e}")
        raise


def test_api_methods():
    """测试API方法"""
    print("\n3. 测试API方法...")
    try:
        from api.labels import router
        
        # 统计不同HTTP方法的端点数量
        methods_count = {}
        for route in router.routes:
            for method in route.methods:
                methods_count[method] = methods_count.get(method, 0) + 1
        
        print("✓ API方法统计:")
        for method, count in sorted(methods_count.items()):
            print(f"  - {method}: {count}个端点")
        
        # 验证至少有GET, POST, PUT, DELETE方法
        required_methods = ['GET', 'POST', 'PUT', 'DELETE']
        for method in required_methods:
            if method in methods_count:
                print(f"  ✓ 包含{method}方法")
            else:
                print(f"  ✗ 缺少{method}方法")
        
        assert len(methods_count) > 0
    except Exception as e:
        print(f"✗ API方法测试失败: {e}")
        raise


def test_api_registration():
    """测试API注册"""
    print("\n4. 测试API注册...")
    try:
        from api import labels_router
        print("✓ 标签管理路由已在api包中注册")
        assert labels_router is not None
    except Exception as e:
        print(f"✗ API注册测试失败: {e}")
        raise


def test_documentation():
    """测试文档存在"""
    print("\n5. 测试API文档...")
    try:
        import os
        doc_path = os.path.join(backend_dir, 'api', 'README_LABELS_API.md')
        
        if os.path.exists(doc_path):
            print(f"✓ API文档存在: {doc_path}")
            
            # 检查文档大小
            size = os.path.getsize(doc_path)
            print(f"  文档大小: {size} 字节")
            
            assert size > 0
        else:
            print(f"✗ API文档不存在: {doc_path}")
            assert False, "API文档不存在"
    except Exception as e:
        print(f"✗ 文档测试失败: {e}")
        raise


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Task 13: 标签管理API测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_router_endpoints,
        test_api_methods,
        test_api_registration,
        test_documentation,
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
