"""
实体抽取Agent测试脚本
"""
import sys
from pathlib import Path
import json

# 添加backend目录到路径
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from agents.entity_extraction import get_entity_agent


def test_entity_extraction():
    """测试实体抽取Agent"""
    print("=" * 60)
    print("测试实体抽取Agent")
    print("=" * 60)
    
    # 获取Agent实例
    agent = get_entity_agent()
    
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
        print(f"\n测试{i}: {test_case['text_id']}")
        print("-" * 60)
        print(f"文本: {test_case['text']}")
        
        try:
            # 调用实体抽取
            result = agent.extract_entities(
                text_id=test_case['text_id'],
                text=test_case['text']
            )
            
            print(f"\n✓ 提取成功，共{len(result.entities)}个实体:")
            
            # 显示提取的实体
            for entity in result.entities:
                extracted_text = test_case['text'][entity.start_offset:entity.end_offset]
                match_status = "✓" if extracted_text == entity.token else "❌"
                print(f"  {match_status} [{entity.label}] {entity.token} ({entity.start_offset}, {entity.end_offset})")
                if extracted_text != entity.token:
                    print(f"     实际提取: '{extracted_text}'")
            
            # 显示JSON格式
            print(f"\nJSON输出:")
            print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
            
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # 显示偏移量修正统计
    print("\n" + "=" * 60)
    print("偏移量修正统计")
    print("=" * 60)
    stats = agent.get_correction_stats()
    print(f"总计: {stats['total']} 次修正")
    print(f"  - 精确匹配: {stats['exact_match']}")
    print(f"  - 模糊匹配: {stats['fuzzy_match']}")
    print(f"  - 修正失败: {stats['failed']}")
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)
    print("\n注意: 此测试需要有效的DASHSCOPE_API_KEY环境变量")
    print("如果测试失败，请检查.env文件中的API配置")


if __name__ == "__main__":
    test_entity_extraction()
