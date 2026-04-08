"""
数据集管理服务测试脚本
"""
import sys
from pathlib import Path

# 添加backend目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, init_db
from services.dataset_service import DatasetService
from models.db_models import Corpus, User


def test_dataset_service():
    """测试数据集管理服务"""
    print("=" * 60)
    print("测试数据集管理服务")
    print("=" * 60)
    
    # 初始化数据库
    init_db()
    db = SessionLocal()
    
    try:
        # 创建测试用户
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            print("❌ 请先运行 init_db.py 初始化数据库")
            return
        
        # 创建测试语料
        print("\n测试1: 创建测试语料")
        print("-" * 60)
        
        test_corpus = []
        for i in range(3):
            corpus = Corpus(
                text_id=f"test-corpus-{i+1}",
                text=f"这是测试语料{i+1}的内容。",
                text_type="测试",
                source_file="test.xlsx",
                source_row=i+1,
                source_field="测试字段"
            )
            db.add(corpus)
            test_corpus.append(corpus)
        
        db.commit()
        for corpus in test_corpus:
            db.refresh(corpus)
        
        print(f"✓ 创建了 {len(test_corpus)} 个测试语料")
        
        # 测试创建数据集
        print("\n测试2: 创建数据集")
        print("-" * 60)
        
        service = DatasetService(db)
        corpus_ids = [c.id for c in test_corpus]
        
        dataset = service.create_dataset(
            name="测试数据集",
            description="这是一个测试数据集",
            corpus_ids=corpus_ids,
            created_by=user.id
        )
        
        print(f"✓ 创建数据集成功")
        print(f"  数据集ID: {dataset.dataset_id}")
        print(f"  数据集名称: {dataset.name}")
        print(f"  语料数量: {len(corpus_ids)}")
        
        # 测试获取数据集
        print("\n测试3: 获取数据集详情")
        print("-" * 60)
        
        retrieved_dataset = service.get_dataset(dataset.dataset_id)
        print(f"✓ 获取数据集成功")
        print(f"  数据集ID: {retrieved_dataset.dataset_id}")
        print(f"  数据集名称: {retrieved_dataset.name}")
        print(f"  描述: {retrieved_dataset.description}")
        
        # 测试数据集统计
        print("\n测试4: 获取数据集统计")
        print("-" * 60)
        
        stats = service.get_dataset_statistics(dataset.dataset_id)
        print(f"✓ 统计信息:")
        print(f"  总任务数: {stats['total_tasks']}")
        print(f"  待处理任务: {stats['pending_tasks']}")
        print(f"  已完成任务: {stats['completed_tasks']}")
        print(f"  完成率: {stats['completion_rate']:.1f}%")
        print(f"  实体数: {stats['total_entities']}")
        print(f"  关系数: {stats['total_relations']}")
        
        # 测试数据集列表
        print("\n测试5: 获取数据集列表")
        print("-" * 60)
        
        datasets = service.list_datasets(limit=10)
        print(f"✓ 获取到 {len(datasets)} 个数据集")
        for ds in datasets:
            print(f"  - {ds.dataset_id}: {ds.name}")
        
        # 测试导出数据集
        print("\n测试6: 导出数据集")
        print("-" * 60)
        
        jsonl_data = service.export_dataset(dataset.dataset_id)
        lines = jsonl_data.split('\n')
        print(f"✓ 导出成功，共 {len(lines)} 条记录")
        if lines:
            import json
            first_record = json.loads(lines[0])
            print(f"  第一条记录:")
            print(f"    text_id: {first_record['text_id']}")
            print(f"    text: {first_record['text']}")
            print(f"    entities: {len(first_record['entities'])} 个")
            print(f"    relations: {len(first_record['relations'])} 个")
        
        # 测试删除数据集
        print("\n测试7: 删除数据集")
        print("-" * 60)
        
        success = service.delete_dataset(dataset.dataset_id)
        print(f"✓ 删除{'成功' if success else '失败'}")
        
        # 验证删除
        deleted_dataset = service.get_dataset(dataset.dataset_id)
        if deleted_dataset is None:
            print(f"✓ 确认数据集已删除")
        else:
            print(f"❌ 数据集仍然存在")
        
        # 清理测试数据
        print("\n清理测试数据...")
        for corpus in test_corpus:
            db.delete(corpus)
        db.commit()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_dataset_service()
