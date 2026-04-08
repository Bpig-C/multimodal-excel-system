"""
图片标注API测试脚本
快速验证图片标注API的基本功能
"""
import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

def test_imports():
    """测试导入"""
    print("1. 测试导入...")
    try:
        from api.images import router
        print("✓ 图片标注API导入成功")
        assert router is not None
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        raise


def test_router_endpoints():
    """测试路由端点"""
    print("\n2. 测试路由端点...")
    try:
        from api.images import router
        
        # 获取所有路由
        routes = [route.path for route in router.routes]
        
        expected_routes = [
            "/api/v1/images/{image_id}/entities",
        ]
        
        print(f"✓ 找到 {len(routes)} 个路由端点")
        
        # 检查关键端点
        for route in routes:
            print(f"  - {route}")
        
        assert len(routes) > 0
    except Exception as e:
        print(f"✗ 路由端点测试失败: {e}")
        raise


def test_database_models():
    """测试数据库模型"""
    print("\n3. 测试数据库模型...")
    try:
        from models.db_models import Image, ImageEntity
        
        # 检查Image模型字段
        image_fields = ['id', 'image_id', 'corpus_id', 'file_path', 
                       'width', 'height', 'created_at']
        for field in image_fields:
            if not hasattr(Image, field):
                print(f"✗ Image模型缺少字段: {field}")
                assert False, f"Image模型缺少字段: {field}"
        
        print("✓ Image模型字段完整")
        
        # 检查ImageEntity模型字段
        entity_fields = ['id', 'entity_id', 'task_id', 'image_id', 'label',
                        'bbox_x', 'bbox_y', 'bbox_width', 'bbox_height',
                        'confidence', 'version', 'created_at']
        for field in entity_fields:
            if not hasattr(ImageEntity, field):
                print(f"✗ ImageEntity模型缺少字段: {field}")
                assert False, f"ImageEntity模型缺少字段: {field}"
        
        print("✓ ImageEntity模型字段完整")
        
    except Exception as e:
        print(f"✗ 数据库模型测试失败: {e}")
        raise


def test_api_registration():
    """测试API注册"""
    print("\n4. 测试API注册...")
    try:
        from api import images_router
        print("✓ 图片标注路由已在api包中注册")
        assert images_router is not None
    except Exception as e:
        print(f"✗ API注册测试失败: {e}")
        raise


def main():
    """运行所有测试"""
    print("=" * 60)
    print("图片标注API快速测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_router_endpoints,
        test_database_models,
        test_api_registration,
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
