"""
图片标注Agent测试（简化版）
"""
import sys
from pathlib import Path

# 添加backend目录到Python路径
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from agents.image_annotation import ImageAnnotationAgent, ImageAnnotationOutput


def print_section(title: str):
    """打印测试章节标题"""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print('=' * 60)


def print_test(test_name: str):
    """打印测试名称"""
    print(f"\n=== {test_name} ===")


def test_single_image_annotation():
    """测试1: 单张图片标注"""
    print_test("测试1: 单张图片标注")
    
    agent = ImageAnnotationAgent()
    
    # 测试默认标签
    result = agent.annotate_image(
        image_path="/test/defect_image.jpg",
        context_text="产品排线连锡缺陷"
    )
    
    print(f"✓ 图片路径: {result.image_path}")
    print(f"✓ 标注标签: {result.label}")
    print(f"✓ 置信度: {result.confidence}")
    print(f"✓ 描述: {result.description}")
    
    # 验证输出格式
    assert isinstance(result, ImageAnnotationOutput)
    assert result.image_path == "/test/defect_image.jpg"
    assert result.label in ["缺陷图片", "缺陷区域"]
    assert 0 <= result.confidence <= 1
    
    print(f"\n✓ 输出格式验证通过")


def test_custom_labels():
    """测试2: 自定义标签列表"""
    print_test("测试2: 自定义标签列表")
    
    agent = ImageAnnotationAgent()
    
    # 使用自定义标签
    custom_labels = ["焊接缺陷", "外观缺陷", "尺寸缺陷"]
    result = agent.annotate_image(
        image_path="/test/solder_defect.jpg",
        context_text="焊接质量问题",
        available_labels=custom_labels
    )
    
    print(f"✓ 可用标签: {custom_labels}")
    print(f"✓ 选择标签: {result.label}")
    
    # 验证使用了自定义标签
    assert result.label in custom_labels
    print(f"\n✓ 自定义标签验证通过")


def test_batch_annotation():
    """测试3: 批量图片标注"""
    print_test("测试3: 批量图片标注")
    
    agent = ImageAnnotationAgent()
    
    # 批量标注
    image_paths = [
        "/test/img1.jpg",
        "/test/img2.jpg",
        "/test/img3.jpg"
    ]
    
    results = agent.annotate_images_batch(
        image_paths=image_paths,
        context_text="批量缺陷检测",
        available_labels=["缺陷图片"]
    )
    
    print(f"✓ 标注图片数: {len(results)}")
    
    # 验证结果
    assert len(results) == len(image_paths)
    
    for i, result in enumerate(results):
        print(f"  - 图片{i+1}: {result.image_path} -> {result.label}")
        assert result.image_path == image_paths[i]
        assert isinstance(result, ImageAnnotationOutput)
    
    print(f"\n✓ 批量标注验证通过")


def test_output_format():
    """测试4: 输出格式验证"""
    print_test("测试4: 输出格式验证")
    
    agent = ImageAnnotationAgent()
    
    result = agent.annotate_image(
        image_path="/test/test.jpg"
    )
    
    # 验证必需字段
    assert hasattr(result, 'image_path')
    assert hasattr(result, 'label')
    assert hasattr(result, 'confidence')
    assert hasattr(result, 'description')
    
    print(f"✓ 必需字段验证通过:")
    print(f"  - image_path: {result.image_path}")
    print(f"  - label: {result.label}")
    print(f"  - confidence: {result.confidence}")
    print(f"  - description: {result.description}")
    
    # 验证字段类型
    assert isinstance(result.image_path, str)
    assert isinstance(result.label, str)
    assert isinstance(result.confidence, (int, float)) or result.confidence is None
    assert isinstance(result.description, str) or result.description is None
    
    print(f"\n✓ 字段类型验证通过")


def test_default_labels():
    """测试5: 默认标签列表"""
    print_test("测试5: 默认标签列表")
    
    agent = ImageAnnotationAgent()
    
    print(f"✓ 默认标签列表: {agent.default_labels}")
    
    # 验证默认标签
    assert len(agent.default_labels) > 0
    assert "缺陷图片" in agent.default_labels
    
    # 测试使用默认标签
    result = agent.annotate_image("/test/img.jpg")
    assert result.label in agent.default_labels
    
    print(f"✓ 默认标签: {result.label}")
    print(f"\n✓ 默认标签验证通过")


def main():
    """运行所有测试"""
    print_section("图片标注Agent测试（简化版）")
    
    test_results = []
    
    try:
        # 测试1: 单张图片标注
        test_single_image_annotation()
        test_results.append(("单张图片标注", True))
        
        # 测试2: 自定义标签
        test_custom_labels()
        test_results.append(("自定义标签列表", True))
        
        # 测试3: 批量标注
        test_batch_annotation()
        test_results.append(("批量图片标注", True))
        
        # 测试4: 输出格式
        test_output_format()
        test_results.append(("输出格式验证", True))
        
        # 测试5: 默认标签
        test_default_labels()
        test_results.append(("默认标签列表", True))
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        test_results.append((f"测试失败", False))
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        test_results.append((f"测试异常", False))
    
    # 打印测试结果汇总
    print_section("测试结果汇总")
    
    for test_name, passed in test_results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, passed in test_results if passed)
    total_count = len(test_results)
    
    print(f"\n总计: {passed_count}/{total_count} 个测试通过")
    
    # 打印说明
    print_section("说明")
    print("""
这是图片标注Agent的简化版实现：

1. **简化功能**:
   - 不调用真实的多模态LLM（Qwen-VL）
   - 使用规则或默认标签进行分类
   - 为后续扩展预留接口

2. **核心功能**:
   - 单张图片标注
   - 批量图片标注
   - 自定义标签支持
   - 标准化输出格式

3. **扩展方向**:
   - 集成Qwen-VL多模态模型
   - 实现缺陷检测和定位
   - 支持基于上下文的智能分类
   - 添加置信度评估

4. **使用场景**:
   - 在批量标注服务中调用
   - 为图片生成初始标签
   - 辅助人工标注
    """)


if __name__ == "__main__":
    main()
