"""
标签管理服务测试 (Task 12)
测试标签配置缓存、动态Prompt生成和标签管理服务
"""
import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """测试导入"""
    print("1. 测试标签管理模块导入...")
    try:
        from services.label_config_cache import LabelConfigCache
        from services.dynamic_prompt_builder import DynamicPromptBuilder
        from services.label_management_service import LabelManagementService
        print("✓ 标签管理模块导入成功")
    except Exception as e:
        print(f"✗ 导入失败: {e}")

        raise


def test_label_config_cache():
    """测试标签配置缓存"""
    print("\n2. 测试标签配置缓存...")
    try:
        from services.label_config_cache import LabelConfigCache
        
        # 测试类方法存在 (LabelConfigCache uses class methods, not instance methods)
        assert hasattr(LabelConfigCache, 'get_entity_types'), "缺少get_entity_types方法"
        assert hasattr(LabelConfigCache, 'get_relation_types'), "缺少get_relation_types方法"
        assert hasattr(LabelConfigCache, 'invalidate_cache'), "缺少invalidate_cache方法"
        
        print("✓ 标签配置缓存功能完整")
    except Exception as e:
        print(f"✗ 标签配置缓存测试失败: {e}")

        raise


def test_dynamic_prompt_builder():
    """测试动态Prompt构建器"""
    print("\n3. 测试动态Prompt构建器...")
    try:
        from services.dynamic_prompt_builder import DynamicPromptBuilder
        
        # DynamicPromptBuilder uses static methods, no instance needed
        # 测试静态方法存在
        assert hasattr(DynamicPromptBuilder, 'build_entity_extraction_prompt'), "缺少build_entity_extraction_prompt方法"
        assert hasattr(DynamicPromptBuilder, 'build_relation_extraction_prompt'), "缺少build_relation_extraction_prompt方法"
        assert hasattr(DynamicPromptBuilder, 'build_entity_types_section'), "缺少build_entity_types_section方法"
        assert hasattr(DynamicPromptBuilder, 'build_relation_types_section'), "缺少build_relation_types_section方法"
        
        print("✓ 动态Prompt构建器功能完整")
    except Exception as e:
        print(f"✗ 动态Prompt构建器测试失败: {e}")

        raise


def test_label_management_service():
    """测试标签管理服务"""
    print("\n4. 测试标签管理服务...")
    try:
        from services.label_management_service import LabelManagementService
        from database import SessionLocal
        
        # 创建数据库会话
        db = SessionLocal()
        
        try:
            # 创建服务实例
            service = LabelManagementService(db)
            
            # 测试实体类型方法
            entity_methods = [
                'create_entity_type',
                'get_entity_type',
                'list_entity_types',
                'update_entity_type',
                'delete_entity_type',
                'review_entity_type'  # Actual method name
            ]
            
            for method in entity_methods:
                assert hasattr(service, method), f"缺少{method}方法"
            
            print("✓ 实体类型管理方法完整")
            
            # 测试关系类型方法
            relation_methods = [
                'create_relation_type',
                'get_relation_type',
                'list_relation_types',
                'update_relation_type',
                'delete_relation_type',
                'review_relation_type'  # Actual method name
            ]
            
            for method in relation_methods:
                assert hasattr(service, method), f"缺少{method}方法"
            
            print("✓ 关系类型管理方法完整")
            
            # 测试导入导出方法
            assert hasattr(service, 'export_label_schema'), "缺少export_label_schema方法"
            assert hasattr(service, 'import_label_schema'), "缺少import_label_schema方法"
            
            print("✓ 导入导出方法完整")
            
            # 测试版本管理方法
            version_methods = [
                'create_version_snapshot',
                'list_versions',
                'get_version',
                'activate_version',
                'get_active_version'  # Actual method name
            ]
            
            for method in version_methods:
                assert hasattr(service, method), f"缺少{method}方法"
            
            print("✓ 版本管理方法完整")
        finally:
            db.close()
    except Exception as e:
        print(f"✗ 标签管理服务测试失败: {e}")

        raise


def test_database_models():
    """测试数据库模型"""
    print("\n5. 测试标签相关数据库模型...")
    try:
        from models.db_models import EntityType, RelationType, LabelSchemaVersion
        
        # 检查EntityType模型字段
        entity_fields = ['id', 'type_name', 'type_name_zh', 'color', 'description',
                        'definition', 'examples', 'disambiguation', 'is_active',
                        'is_reviewed', 'supports_bbox']
        
        for field in entity_fields:
            assert hasattr(EntityType, field), f"EntityType缺少字段: {field}"
        
        print("✓ EntityType模型字段完整")
        
        # 检查RelationType模型字段
        relation_fields = ['id', 'type_name', 'type_name_zh', 'color', 'description',
                          'definition', 'direction_rule', 'examples', 'disambiguation',
                          'is_active', 'is_reviewed']
        
        for field in relation_fields:
            assert hasattr(RelationType, field), f"RelationType缺少字段: {field}"
        
        print("✓ RelationType模型字段完整")
        
        # 检查LabelSchemaVersion模型字段
        version_fields = ['id', 'version_id', 'version_name', 'description',
                         'schema_data', 'is_active', 'created_by', 'created_at']
        
        for field in version_fields:
            assert hasattr(LabelSchemaVersion, field), f"LabelSchemaVersion缺少字段: {field}"
        
        print("✓ LabelSchemaVersion模型字段完整")
    except Exception as e:
        print(f"✗ 数据库模型测试失败: {e}")

        raise


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Task 12: 标签管理服务测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_label_config_cache,
        test_dynamic_prompt_builder,
        test_label_management_service,
        test_database_models,
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
