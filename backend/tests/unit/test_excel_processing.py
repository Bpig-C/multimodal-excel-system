"""
Excel处理服务测试脚本
测试Excel文件解析、图片提取、语料生成功能
"""
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加backend目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from database import Base
from services.excel_processing import ExcelProcessingService
from config import settings


def test_excel_processing():
    """测试Excel处理服务"""
    print("=" * 60)
    print("测试Excel处理服务")
    print("=" * 60)
    
    # 创建测试数据库
    test_db_path = "./tests/test_artifacts/databases/test_excel_processing.db"
    Path(test_db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # 如果存在旧的测试数据库，删除它
    if Path(test_db_path).exists():
        Path(test_db_path).unlink()
    
    engine = create_engine(f"sqlite:///{test_db_path}")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    
    # 创建会话
    db = SessionLocal()
    
    try:
        # 创建服务实例
        service = ExcelProcessingService(db)
        
        # 测试1: 验证Excel文件
        print("\n测试1: 验证Excel文件")
        print("-" * 60)
        
        # 从backend目录回到项目根目录
        test_file = Path("../参考项目代码/导入文件示例/品质失效案例-2022年-客户端质量问题.xlsx")
        
        if not test_file.exists():
            print(f"❌ 测试文件不存在: {test_file}")
            print("请确保参考项目代码目录存在")
            return
        
        validation_result = service.validate_excel_file(str(test_file))
        
        if validation_result["valid"]:
            print(f"✓ Excel文件验证通过")
            print(f"  - 行数: {validation_result['row_count']}")
            print(f"  - 列数: {validation_result['column_count']}")
            print(f"  - 列名: {', '.join(validation_result['columns'][:5])}...")
        else:
            print(f"❌ Excel文件验证失败: {validation_result['error']}")
            return
        
        # 测试2: 提取图片
        print("\n测试2: 提取WPS内嵌图片")
        print("-" * 60)
        
        image_mapping = service.extract_wps_excel_images(str(test_file), "品质失效案例-2022年-客户端质量问题.xlsx")
        
        print(f"✓ 提取图片数量: {len(image_mapping)}")
        if image_mapping:
            print(f"  示例图片:")
            for i, (name, path) in enumerate(list(image_mapping.items())[:3]):
                print(f"    - {name} -> {path}")
                if i >= 2:
                    break
        
        # 测试3: 文本分句
        print("\n测试3: 文本分句功能")
        print("-" * 60)
        
        test_texts = [
            "这是第一句。这是第二句。",
            "1. 第一项\n2. 第二项\n3. 第三项",
            "单行文本没有分隔符",
            "这是   有多余    空格的   文本。",  # 测试空格清理
            "  首尾有空格  。  另一句也有  。"  # 测试首尾空格
        ]
        
        for text in test_texts:
            sentences = service._split_text_to_sentences(text)
            print(f"✓ 原文: {text[:30]}...")
            print(f"  分句结果: {len(sentences)} 句")
            for i, sent in enumerate(sentences[:2]):
                print(f"    {i+1}. {sent[:40]}...")
        
        # 测试4: DISPIMG转换
        print("\n测试4: DISPIMG公式转换")
        print("-" * 60)
        
        test_dispimg = '=DISPIMG("ID_228A8CA5B0AB49848DD6699BFAAF4F35",1)'
        converted = service._convert_dispimg_to_markdown(test_dispimg)
        print(f"✓ 原始: {test_dispimg}")
        print(f"  转换: {converted}")
        
        # 提取图片引用
        image_refs = service._extract_image_paths(converted)
        print(f"  提取图片引用: {image_refs}")
        
        # 测试5: 完整处理流程（使用小样本）
        print("\n测试5: 完整处理流程")
        print("-" * 60)
        print("注意: 完整处理会创建语料记录，可能需要较长时间")
        print("如需测试完整流程，请取消下面的注释")
        
        # 取消注释以测试完整流程
        # result = service.process_excel_file(str(test_file), "品质失效案例-2022年-客户端质量问题.xlsx")
        # print(f"✓ 处理完成")
        # print(f"  - 语料数量: {result['corpus_count']}")
        # print(f"  - 句子数量: {result['sentence_count']}")
        # print(f"  - 图片数量: {result['image_count']}")
        # print(f"  - 状态: {result['status']}")
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_excel_processing()
