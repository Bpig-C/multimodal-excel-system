"""
复核服务测试脚本
测试复核流程的核心功能
"""
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base
from models.db_models import (
    User, Corpus, Dataset, AnnotationTask, TextEntity, Relation, ReviewTask
)
from services.review_service import ReviewService


@pytest.fixture(scope="module")
def db():
    """创建测试数据库 fixture"""
    engine = create_engine('sqlite:///./tests/test_artifacts/databases/test_review_service.db', echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def service(db):
    """创建 ReviewService fixture"""
    return ReviewService(db)


@pytest.fixture(scope="module")
def annotator(db):
    """创建标注人员 fixture"""
    user = User(
        username="annotator1",
        password_hash="hash123",
        role="annotator"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="module")
def reviewer(db):
    """创建复核人员 fixture"""
    user = User(
        username="reviewer1",
        password_hash="hash456",
        role="reviewer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="module")
def corpus(db):
    """创建语料 fixture"""
    c = Corpus(
        text_id="CORP_001",
        text="2022年02月21日，捷普产线反馈CB760-60038产品排线连锡10pcs。",
        text_type="问题描述",
        source_file="test.xlsx",
        source_row=1,
        source_field="问题描述"
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@pytest.fixture(scope="module")
def dataset(db, annotator):
    """创建数据集 fixture"""
    ds = Dataset(
        dataset_id="DS_001",
        name="测试数据集",
        description="用于测试复核功能",
        created_by=annotator.id
    )
    db.add(ds)
    db.commit()
    db.refresh(ds)
    return ds


@pytest.fixture(scope="module")
def task(db, dataset, corpus, annotator):
    """创建标注任务 fixture"""
    t = AnnotationTask(
        task_id="TASK_001",
        dataset_id=dataset.id,
        corpus_id=corpus.id,
        status='completed',
        annotation_type='manual',
        assigned_to=annotator.id
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    
    # 添加实体
    entity1 = TextEntity(
        entity_id=0,
        task_id=t.id,
        version=1,
        token="2022年02月21日",
        label="日期时间",
        start_offset=0,
        end_offset=12
    )
    entity2 = TextEntity(
        entity_id=1,
        task_id=t.id,
        version=1,
        token="捷普",
        label="客户名称",
        start_offset=13,
        end_offset=15
    )
    db.add_all([entity1, entity2])
    db.commit()
    
    # 添加关系
    relation = Relation(
        relation_id=0,
        task_id=t.id,
        version=1,
        from_entity_id=0,
        to_entity_id=1,
        relation_type="relates_to"
    )
    db.add(relation)
    db.commit()
    
    return t


@pytest.fixture(scope="function")  # 改为 function scope
def review(service, task, reviewer, db):
    """创建复核任务 fixture"""
    # 确保任务状态为 completed
    task_obj = db.query(AnnotationTask).filter(AnnotationTask.id == task.id).first()
    if task_obj:
        task_obj.status = 'completed'
        db.commit()
    
    # 删除已存在的待处理复核任务
    db.query(ReviewTask).filter(
        ReviewTask.task_id == task.id,
        ReviewTask.status == 'pending'
    ).delete()
    db.commit()
    
    return service.submit_for_review(task_id=task.id, reviewer_id=reviewer.id)


def test_submit_for_review(db, service, task):
    """测试提交复核"""
    print("\n=== 测试1: 提交复核 ===")
    
    try:
        review = service.submit_for_review(task.id)
        print(f"✓ 成功创建复核任务: {review.review_id}")
        print(f"  - 状态: {review.status}")
        print(f"  - 关联任务: {task.task_id}")
        
        # 验证任务状态更新
        db.refresh(task)
        assert task.status == 'under_review', "任务状态应更新为under_review"
        print(f"✓ 任务状态已更新为: {task.status}")
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise


def test_get_review_tasks(db, service):
    """测试查询复核任务"""
    print("\n=== 测试2: 查询复核任务 ===")
    
    try:
        # 查询所有待处理的复核任务
        reviews, total = service.get_review_tasks(status='pending')
        print(f"✓ 查询到 {total} 个待处理复核任务")
        
        for review in reviews:
            print(f"  - {review.review_id}: 状态={review.status}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

        raise


def test_get_review_detail(db, service, review):
    """测试获取复核任务详情"""
    print("\n=== 测试3: 获取复核任务详情 ===")
    
    try:
        detail = service.get_review_task_detail(review.review_id)
        
        if detail:
            print(f"✓ 成功获取复核任务详情")
            print(f"  - 复核ID: {detail['review_id']}")
            print(f"  - 任务ID: {detail['task']['task_id']}")
            print(f"  - 文本实体数: {len(detail['task']['text_entities'])}")
            print(f"  - 关系数: {len(detail['task']['relations'])}")
            
            # 显示实体详情
            for entity in detail['task']['text_entities']:
                print(f"    实体: {entity['token']} ({entity['label']})")
        else:
            print("✗ 未找到复核任务详情")

            raise
    except Exception as e:
        print(f"✗ 测试失败: {e}")

        raise


def test_approve_task(db, service, review, reviewer):
    """测试批准任务"""
    print("\n=== 测试4: 批准任务 ===")
    
    try:
        updated_review = service.approve_task(
            review.review_id,
            reviewer.id,
            "标注质量良好，批准通过"
        )
        
        print(f"✓ 成功批准任务")
        print(f"  - 复核状态: {updated_review.status}")
        print(f"  - 复核意见: {updated_review.review_comment}")
        print(f"  - 复核时间: {updated_review.reviewed_at}")
        
        # 验证任务状态
        task = db.query(AnnotationTask).filter(
            AnnotationTask.id == review.task_id
        ).first()
        assert task.status == 'approved', "任务状态应更新为approved"
        print(f"✓ 任务状态已更新为: {task.status}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

        raise


def test_reject_task(db, service, task, reviewer):
    """测试驳回任务"""
    print("\n=== 测试5: 驳回任务 ===")
    
    try:
        # 重新提交复核
        task.status = 'completed'
        db.commit()
        
        review = service.submit_for_review(task.id)
        print(f"✓ 重新创建复核任务: {review.review_id}")
        
        # 驳回任务
        updated_review = service.reject_task(
            review.review_id,
            reviewer.id,
            "实体标注不完整，需要补充标注"
        )
        
        print(f"✓ 成功驳回任务")
        print(f"  - 复核状态: {updated_review.status}")
        print(f"  - 驳回原因: {updated_review.review_comment}")
        
        # 验证任务状态
        db.refresh(task)
        assert task.status == 'rejected', "任务状态应更新为rejected"
        print(f"✓ 任务状态已更新为: {task.status}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

        raise


def test_record_modifications(db, service, review):
    """测试记录复核修改"""
    print("\n=== 测试6: 记录复核修改 ===")
    
    try:
        modifications = {
            "added_entities": [
                {"id": 2, "token": "产线", "label": "地点部门"}
            ],
            "removed_entities": [],
            "modified_entities": [
                {"id": 1, "old_label": "客户名称", "new_label": "供应商"}
            ],
            "added_relations": [
                {"from_id": 0, "to_id": 2, "type": "relates_to"}
            ],
            "removed_relations": []
        }
        
        service.record_review_modifications(review.review_id, modifications)
        print(f"✓ 成功记录复核修改")
        
        # 验证修改记录
        db.refresh(review)
        import json
        stored_data = json.loads(review.review_comment)
        print(f"  - 新增实体: {len(stored_data['modifications']['added_entities'])}")
        print(f"  - 修改实体: {len(stored_data['modifications']['modified_entities'])}")
        print(f"  - 新增关系: {len(stored_data['modifications']['added_relations'])}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

        raise


def test_quality_statistics(db, service, dataset):
    """测试质量统计"""
    print("\n=== 测试7: 质量统计 ===")
    
    try:
        stats = service.calculate_quality_statistics(dataset.id)
        
        print(f"✓ 成功计算质量统计")
        print(f"  - 总任务数: {stats['total_tasks']}")
        print(f"  - 已完成: {stats['completed_tasks']}")
        print(f"  - 待复核: {stats['under_review_tasks']}")
        print(f"  - 已批准: {stats['approved_tasks']}")
        print(f"  - 已驳回: {stats['rejected_tasks']}")
        print(f"  - 完成率: {stats['completion_rate']:.2%}")
        print(f"  - 批准率: {stats['approval_rate']:.2%}")
        print(f"  - 驳回率: {stats['rejection_rate']:.2%}")
        print(f"  - 平均实体数: {stats['average_entities_per_task']:.2f}")
        print(f"  - 平均关系数: {stats['average_relations_per_task']:.2f}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

        raise


def test_review_summary(db, service, dataset):
    """测试复核摘要"""
    print("\n=== 测试8: 复核摘要 ===")
    
    try:
        summary = service.get_dataset_review_summary(dataset.id)
        
        print(f"✓ 成功获取复核摘要")
        print(f"  - 总复核数: {summary['total_reviews']}")
        print(f"  - 待处理: {summary['pending_reviews']}")
        print(f"  - 已批准: {summary['approved_reviews']}")
        print(f"  - 已驳回: {summary['rejected_reviews']}")
        print(f"  - 平均复核时间: {summary['average_review_time_hours']:.2f} 小时")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

        raise


def main():
    """主测试函数"""
    print("=" * 60)
    print("复核服务测试")
    print("=" * 60)
    
    # 设置测试数据库
    db = setup_test_db()
    service = ReviewService(db)
    
    # 创建测试数据
    annotator, reviewer, task = create_test_data(db)
    dataset = db.query(Dataset).first()
    
    # 运行测试
    results = []
    
    # 测试1: 提交复核
    review = test_submit_for_review(db, service, task)
    results.append(("提交复核", review is not None))
    
    if review:
        # 测试2: 查询复核任务
        results.append(("查询复核任务", test_get_review_tasks(db, service)))
        
        # 测试3: 获取复核详情
        results.append(("获取复核详情", test_get_review_detail(db, service, review)))
        
        # 测试6: 记录复核修改
        results.append(("记录复核修改", test_record_modifications(db, service, review)))
        
        # 测试4: 批准任务
        results.append(("批准任务", test_approve_task(db, service, review, reviewer)))
    
    # 测试5: 驳回任务
    results.append(("驳回任务", test_reject_task(db, service, task, reviewer)))
    
    # 测试7: 质量统计
    results.append(("质量统计", test_quality_statistics(db, service, dataset)))
    
    # 测试8: 复核摘要
    results.append(("复核摘要", test_review_summary(db, service, dataset)))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {test_name}")
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    # 清理
    db.close()
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
