"""
关系抽取Agent测试脚本
"""
import sys
from pathlib import Path
import json

# 添加backend目录到路径
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from agents.entity_extraction import get_entity_agent
from agents.relation_extraction import get_relation_agent


def test_relation_extraction():
    """测试关系抽取Agent"""
    print("=" * 60)
    print("测试关系抽取Agent")
    print("=" * 60)
    
    # 获取Agent实例
    entity_agent = get_entity_agent()
    relation_agent = get_relation_agent()
    
    # 测试用例
    test_cases = [
        {
            "text_id": "test_001",
            "text": "产品外观有划痕，经检查发现是焊接工序中操作不当导致。"
        },
        {
            "text_id": "test_002",
            "text": "XX型号主板在测试工序中发现功能失效，原因是电子元件质量不合格。"
        },
        {
            "text_id": "test_003",
            "text": "2022年3月，XX客户反馈显示屏出现裂纹，需要返工处理。"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试{i}: {test_case['text_id']}")
        print("=" * 60)
        print(f"文本: {test_case['text']}")
        
        try:
            # 步骤1: 提取实体
            print(f"\n步骤1: 提取实体")
            print("-" * 60)
            entity_result = entity_agent.extract_entities(
                text_id=test_case['text_id'],
                text=test_case['text']
            )
            
            print(f"✓ 提取成功，共{len(entity_result.entities)}个实体:")
            for entity in entity_result.entities:
                print(f"  [{entity.id}] {entity.token} ({entity.label})")
            
            # 步骤2: 提取关系
            print(f"\n步骤2: 提取关系")
            print("-" * 60)
            relation_result = relation_agent.extract_relations(
                text_id=test_case['text_id'],
                text=test_case['text'],
                entities=entity_result.entities
            )
            
            print(f"✓ 提取成功，共{len(relation_result.relations)}个关系:")
            for relation in relation_result.relations:
                # 查找实体信息
                from_entity = next((e for e in entity_result.entities if e.id == relation.from_id), None)
                to_entity = next((e for e in entity_result.entities if e.id == relation.to_id), None)
                
                if from_entity and to_entity:
                    print(f"  [{relation.id}] {from_entity.token} --[{relation.type}]--> {to_entity.token}")
                else:
                    print(f"  [{relation.id}] {relation.from_id} --[{relation.type}]--> {relation.to_id} (实体未找到)")
            
            # 显示完整JSON
            print(f"\n完整JSON输出:")
            print("-" * 60)
            output = {
                "text_id": test_case['text_id'],
                "text": test_case['text'],
                "entities": [e.model_dump() for e in entity_result.entities],
                "relations": [r.model_dump() for r in relation_result.relations]
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)
    print("\n注意: 此测试需要有效的DASHSCOPE_API_KEY环境变量")
    print("如果测试失败，请检查.env文件中的API配置")


if __name__ == "__main__":
    test_relation_extraction()
