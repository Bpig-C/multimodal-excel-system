"""
偏移量验证与修正服务测试脚本
"""
import sys
from pathlib import Path

# 添加backend目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from services.offset_correction import OffsetCorrectionService


def test_offset_correction():
    """测试偏移量验证与修正服务"""
    print("=" * 60)
    print("测试偏移量验证与修正服务")
    print("=" * 60)
    
    service = OffsetCorrectionService()
    
    # 测试1: 精确匹配
    print("\n测试1: 精确匹配验证")
    print("-" * 60)
    
    text1 = "这是一个测试文本，包含实体标注。"
    entity1 = "测试文本"
    start1, end1 = 5, 9
    
    is_valid = service.validate_offset(text1, entity1, start1, end1)
    print(f"文本: {text1}")
    print(f"实体: {entity1}")
    print(f"偏移量: ({start1}, {end1})")
    print(f"验证结果: {'✓ 正确' if is_valid else '❌ 错误'}")
    print(f"提取文本: {text1[start1:end1]}")
    
    # 测试2: 偏移量错误，需要修正
    print("\n测试2: 偏移量修正（精确匹配）")
    print("-" * 60)
    
    text2 = "产品质量问题分析报告"
    entity2 = "质量问题"
    wrong_start, wrong_end = 0, 4  # 错误的偏移量
    
    corrected_start, corrected_end, log = service.correct_offset(
        text2, entity2, wrong_start, wrong_end
    )
    
    print(f"文本: {text2}")
    print(f"实体: {entity2}")
    print(f"原始偏移量: ({wrong_start}, {wrong_end}) -> '{text2[wrong_start:wrong_end]}'")
    if corrected_start is not None:
        print(f"✓ 修正后偏移量: ({corrected_start}, {corrected_end}) -> '{text2[corrected_start:corrected_end]}'")
        print(f"  修正类型: {log.correction_type}")
    else:
        print(f"❌ 修正失败: {log.message}")
    
    # 测试3: 包含空格的文本
    print("\n测试3: 包含空格的文本修正")
    print("-" * 60)
    
    text3 = "这是  一个  有多余空格  的文本"
    entity3 = "有多余空格"
    hint_start = 10
    
    corrected_start, corrected_end, log = service.correct_offset(
        text3, entity3, hint_start, hint_start + len(entity3)
    )
    
    print(f"文本: {text3}")
    print(f"实体: {entity3}")
    print(f"提示偏移量: {hint_start}")
    if corrected_start is not None:
        print(f"✓ 找到匹配: ({corrected_start}, {corrected_end}) -> '{text3[corrected_start:corrected_end]}'")
        print(f"  修正类型: {log.correction_type}")
    else:
        print(f"❌ 未找到匹配: {log.message}")
    
    # 测试4: 模糊匹配
    print("\n测试4: 模糊匹配（忽略标点）")
    print("-" * 60)
    
    text4 = "问题描述：产品外观有划痕，需要返工处理。"
    entity4 = "产品外观有划痕"
    hint_start = 5
    
    corrected_start, corrected_end, log = service.correct_offset(
        text4, entity4, hint_start, hint_start + len(entity4)
    )
    
    print(f"文本: {text4}")
    print(f"实体: {entity4}")
    print(f"提示偏移量: {hint_start}")
    if corrected_start is not None:
        print(f"✓ 找到匹配: ({corrected_start}, {corrected_end}) -> '{text4[corrected_start:corrected_end]}'")
        print(f"  修正类型: {log.correction_type}")
    else:
        print(f"❌ 未找到匹配: {log.message}")
    
    # 测试5: 无法匹配的情况
    print("\n测试5: 无法匹配的实体")
    print("-" * 60)
    
    text5 = "这是一段测试文本"
    entity5 = "不存在的实体"
    hint_start = 0
    
    corrected_start, corrected_end, log = service.correct_offset(
        text5, entity5, hint_start, hint_start + len(entity5)
    )
    
    print(f"文本: {text5}")
    print(f"实体: {entity5}")
    if corrected_start is None:
        print(f"✓ 正确识别无法匹配: {log.message}")
        print(f"  修正类型: {log.correction_type}")
    else:
        print(f"❌ 不应该找到匹配")
    
    # 测试6: 统计信息
    print("\n测试6: 修正统计信息")
    print("-" * 60)
    
    stats = service.get_correction_stats()
    print(f"总计: {stats['total']} 次修正")
    print(f"  - 精确匹配: {stats['exact_match']}")
    print(f"  - 模糊匹配: {stats['fuzzy_match']}")
    print(f"  - 修正失败: {stats['failed']}")
    
    # 测试7: 查看修正日志
    print("\n测试7: 修正日志详情")
    print("-" * 60)
    
    logs = service.get_correction_logs()
    for i, log in enumerate(logs, 1):
        print(f"\n日志 {i}:")
        print(f"  实体: {log.entity_text}")
        print(f"  原始: ({log.original_start}, {log.original_end})")
        print(f"  修正: ({log.corrected_start}, {log.corrected_end})")
        print(f"  类型: {log.correction_type}")
        print(f"  消息: {log.message}")
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_offset_correction()
