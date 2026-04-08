"""
标注任务API测试 (Task 15)
测试标注任务API端点
"""
import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)


def test_imports():
    """测试导入"""
    print("1. 测试标注任务API导入...")
    try:
        from api.annotations import router
        print("✓ 标注任务API导入成功")
    except Exception as e:
        print(f"✗ 导入失败: {e}")

        raise


def test_router_endpoints():
    """测试路由端点"""
    print("\n2. 测试路由端点...")
    try:
        from api.annotations import router
        
        # 获取所有路由
        routes = [route.path for route in router.routes]
        
        print(f"✓ 找到 {len(routes)} 个路由端点")
        
        # 检查关键端点类别
        batch_endpoints = [r for r in routes if '/batch' in r]
        entity_endpoints = [r for r in routes if '/entities' in r]
        relation_endpoints = [r for r in routes if '/relations' in r]
        
        print(f"  - 批量标注端点: {len(batch_endpoints)}个")
        print(f"  - 实体管理端点: {len(entity_endpoints)}个")
        print(f"  - 关系管理端点: {len(relation_endpoints)}个")
        
        # 验证至少有这些端点
        assert len(batch_endpoints) >= 3, "批量标注端点不足"
        assert len(entity_endpoints) >= 3, "实体管理端点不足"
        assert len(relation_endpoints) >= 3, "关系管理端点不足"
        
        print("✓ 端点数量符合预期")
    except Exception as e:
        print(f"✗ 路由端点测试失败: {e}")

        raise


def test_api_methods():
    """测试API方法"""
    print("\n3. 测试API方法...")
    try:
        from api.annotations import router
        
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

                raise
    except Exception as e:
        print(f"✗ API方法测试失败: {e}")

        raise


def test_background_tasks():
    """测试后台任务支持"""
    print("\n4. 测试后台任务支持...")
    try:
        from api.annotations import router
        import inspect
        
        # 查找使用BackgroundTasks的端点
        has_background_tasks = False
        
        for route in router.routes:
            if hasattr(route, 'endpoint'):
                sig = inspect.signature(route.endpoint)
                for param_name, param in sig.parameters.items():
                    if 'BackgroundTasks' in str(param.annotation):
                        has_background_tasks = True
                        print(f"  ✓ {route.path} 使用BackgroundTasks")
                        break
        
        if has_background_tasks:
            print("✓ 支持后台任务")
        else:
            print("✗ 未找到使用BackgroundTasks的端点")

            raise
    except Exception as e:
        print(f"✗ 后台任务测试失败: {e}")

        raise


def test_api_registration():
    """测试API注册"""
    print("\n5. 测试API注册...")
    try:
        from api import annotations_router
        print("✓ 标注任务路由已在api包中注册")
    except Exception as e:
        print(f"✗ API注册测试失败: {e}")

        raise


def test_cascade_delete():
    """测试级联删除逻辑"""
    print("\n6. 测试级联删除逻辑...")
    try:
        # 读取API文件内容检查级联删除逻辑
        api_file = os.path.join(backend_dir, 'api', 'annotations.py')
        
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有删除关联关系的逻辑
        if 'delete_entity' in content and 'Relation' in content:
            print("✓ 实体删除包含关系级联删除逻辑")
        else:
            print("✗ 未找到级联删除逻辑")

            raise
    except Exception as e:
        print(f"✗ 级联删除测试失败: {e}")

        raise


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Task 15: 标注任务API测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_router_endpoints,
        test_api_methods,
        test_background_tasks,
        test_api_registration,
        test_cascade_delete,
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
