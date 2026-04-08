"""
复核API测试脚本
测试复核相关的REST API端点
"""
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import pytest

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from database import Base, get_db
from main import app
from models.db_models import (
    User, Corpus, Dataset, AnnotationTask, TextEntity, Relation, ReviewTask
)

# 创建测试数据库 - 保存到test_artifacts目录
TEST_DATABASE_URL = "sqlite:///./tests/test_artifacts/databases/test_review_api.db"
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """覆盖数据库依赖"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """测试前后的设置和清理"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    """创建测试客户端 fixture"""
    return TestClient(app)


@pytest.fixture(scope="module")
def annotator():
    """创建标注人员 fixture"""
    db = TestingSessionLocal()
    try:
        user = User(
            username="annotator1",
            password_hash="hash123",
            role="annotator"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


@pytest.fixture(scope="module")
def reviewer():
    """创建复核人员 fixture"""
    db = TestingSessionLocal()
    try:
        user = User(
            username="reviewer1",
            password_hash="hash456",
            role="reviewer"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


@pytest.fixture(scope="module")
def corpus():
    """创建语料 fixture"""
    db = TestingSessionLocal()
    try:
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
    finally:
        db.close()


@pytest.fixture(scope="module")
def dataset(annotator):
    """创建数据集 fixture"""
    db = TestingSessionLocal()
    try:
        ds = Dataset(
            dataset_id="DS_001",
            name="测试数据集",
            description="用于测试复核API",
            created_by=annotator.id
        )
        db.add(ds)
        db.commit()
        db.refresh(ds)
        return ds
    finally:
        db.close()


@pytest.fixture(scope="module")
def task(dataset, corpus, annotator):
    """创建标注任务 fixture"""
    db = TestingSessionLocal()
    try:
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
        
        task_db_id = t.id
        
        # 添加实体
        entity1 = TextEntity(
            entity_id=0,
            task_id=task_db_id,
            version=1,
            token="2022年02月21日",
            label="日期时间",
            start_offset=0,
            end_offset=12
        )
        entity2 = TextEntity(
            entity_id=1,
            task_id=task_db_id,
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
            task_id=task_db_id,
            version=1,
            from_entity_id=0,
            to_entity_id=1,
            relation_type="relates_to"
        )
        db.add(relation)
        db.commit()
    finally:
        db.close()
    
    # 返回 task_id 字符串
    return "TASK_001"


@pytest.fixture(scope="function")
def review_id(client, task):
    """创建复核任务并返回ID fixture"""
    # 重置任务状态为 completed
    db = TestingSessionLocal()
    try:
        task_obj = db.query(AnnotationTask).filter(
            AnnotationTask.task_id == task
        ).first()
        if task_obj:
            task_obj.status = 'completed'
            db.commit()
        
        # 删除已存在的待处理复核任务
        if task_obj:
            db.query(ReviewTask).filter(
                ReviewTask.task_id == task_obj.id,
                ReviewTask.status == 'pending'
            ).delete()
            db.commit()
    finally:
        db.close()
    
    # 创建新的复核任务
    response = client.post(f"/api/v1/review/submit/{task}")
    if response.status_code in [200, 201]:
        data = response.json()
        review_id_value = data.get("review_id") or data.get("data", {}).get("review_id")
        return review_id_value
    return None


def test_submit_review(client, task):
    """测试提交复核"""
    print("\n=== 测试1: 提交复核 ===")
    
    response = client.post(f"/api/v1/review/submit/{task}")
    
    assert response.status_code == 200, f"状态码错误: {response.status_code}"
    
    data = response.json()
    print(f"✓ 成功提交复核")
    print(f"  - 复核ID: {data['review_id']}")
    print(f"  - 任务ID: {data['task_id']}")
    print(f"  - 状态: {data['status']}")


def test_get_review_tasks(client):
    """测试获取复核任务列表"""
    print("\n=== 测试2: 获取复核任务列表 ===")
    
    response = client.get("/api/v1/review/tasks?status=pending")
    
    assert response.status_code == 200, f"状态码错误: {response.status_code}"
    
    data = response.json()
    print(f"✓ 成功获取复核任务列表")
    print(f"  - 任务数量: {len(data)}")
    
    if data:
        print(f"  - 第一个任务: {data[0]['review_id']}")


def test_get_review_detail(client, review_id):
    """测试获取复核任务详情"""
    print("\n=== 测试3: 获取复核任务详情 ===")
    
    response = client.get(f"/api/v1/review/{review_id}")
    
    assert response.status_code == 200, f"状态码错误: {response.status_code}"
    
    data = response.json()
    print(f"✓ 成功获取复核任务详情")
    print(f"  - 复核ID: {data['review_id']}")
    print(f"  - 任务ID: {data['task']['task_id']}")
    print(f"  - 文本实体数: {len(data['task']['text_entities'])}")
    print(f"  - 关系数: {len(data['task']['relations'])}")


def test_approve_review(client, review_id, reviewer):
    """测试批准复核"""
    print("\n=== 测试4: 批准复核 ===")
    
    response = client.post(
        f"/api/v1/review/{review_id}/approve?reviewer_id={reviewer.id}",
        json={"review_comment": "标注质量良好，批准通过"}
    )
    
    assert response.status_code == 200, f"状态码错误: {response.status_code}, 响应: {response.text}"
    
    data = response.json()
    print(f"✓ 成功批准复核")
    print(f"  - 复核状态: {data['status']}")
    print(f"  - 复核意见: {data['review_comment']}")


def test_reject_review(client, task, reviewer):
    """测试驳回复核"""
    print("\n=== 测试5: 驳回复核 ===")
    
    # 重置任务状态
    db = TestingSessionLocal()
    try:
        task_obj = db.query(AnnotationTask).filter(
            AnnotationTask.task_id == task
        ).first()
        if task_obj:
            task_obj.status = 'completed'
            db.commit()
        
        # 删除已存在的待处理复核任务
        db.query(ReviewTask).filter(
            ReviewTask.task_id == task_obj.id,
            ReviewTask.status == 'pending'
        ).delete()
        db.commit()
    finally:
        db.close()
    
    # 先提交新的复核
    response = client.post(f"/api/v1/review/submit/{task}")
    assert response.status_code == 200, f"提交复核失败: {response.status_code}, {response.text}"
    review_id = response.json()['review_id']
    print(f"✓ 创建新复核任务: {review_id}")
    
    # 驳回复核
    response = client.post(
        f"/api/v1/review/{review_id}/reject?reviewer_id={reviewer.id}",
        json={"review_comment": "实体标注不完整，需要补充标注"}
    )
    
    assert response.status_code == 200, f"状态码错误: {response.status_code}, {response.text}"
    
    data = response.json()
    print(f"✓ 成功驳回复核")
    print(f"  - 复核状态: {data['status']}")
    print(f"  - 驳回原因: {data['review_comment']}")


def test_dataset_statistics(client, dataset):
    """测试数据集质量统计"""
    print("\n=== 测试6: 数据集质量统计 ===")
    
    response = client.get(f"/api/v1/review/dataset/{dataset.id}/statistics")
    
    assert response.status_code == 200, f"状态码错误: {response.status_code}"
    
    data = response.json()
    print(f"✓ 成功获取质量统计")
    print(f"  - 总任务数: {data['total_tasks']}")
    print(f"  - 已批准: {data['approved_tasks']}")
    print(f"  - 已驳回: {data['rejected_tasks']}")
    print(f"  - 批准率: {data['approval_rate']:.2%}")
    print(f"  - 平均实体数: {data['average_entities_per_task']:.2f}")


def test_dataset_review_summary(client, dataset):
    """测试数据集复核摘要"""
    print("\n=== 测试7: 数据集复核摘要 ===")
    
    response = client.get(f"/api/v1/review/dataset/{dataset.id}/summary")
    
    assert response.status_code == 200, f"状态码错误: {response.status_code}"
    
    data = response.json()
    print(f"✓ 成功获取复核摘要")
    print(f"  - 总复核数: {data['total_reviews']}")
    print(f"  - 待处理: {data['pending_reviews']}")
    print(f"  - 已批准: {data['approved_reviews']}")
    print(f"  - 已驳回: {data['rejected_reviews']}")


def test_error_cases(client):
    """测试错误情况"""
    print("\n=== 测试8: 错误情况处理 ===")
    
    # 测试不存在的任务
    response = client.post("/api/v1/review/submit/NONEXISTENT")
    assert response.status_code == 404
    print("✓ 正确处理不存在的任务")
    
    # 测试不存在的复核
    response = client.get("/api/v1/review/NONEXISTENT")
    assert response.status_code == 404
    print("✓ 正确处理不存在的复核")
    
    # 测试驳回时缺少原因
    response = client.post(
        "/api/v1/review/REV_TEST/reject?reviewer_id=1",
        json={"review_comment": ""}
    )
    assert response.status_code == 400
    print("✓ 正确处理驳回时缺少原因")


def main():
    """主测试函数"""
    print("=" * 60)
    print("复核API测试")
    print("=" * 60)
    
    # 设置测试数据库
    db = setup_test_db()
    
    # 创建测试数据
    annotator, reviewer, task, dataset = create_test_data(db)
    
    # 创建测试客户端
    client = TestClient(app)
    
    # 运行测试
    results = []
    
    try:
        # 测试1: 提交复核
        review_id = test_submit_review(client, task)
        results.append(("提交复核", True))
        
        # 测试2: 获取复核任务列表
        test_get_review_tasks(client)
        results.append(("获取复核任务列表", True))
        
        # 测试3: 获取复核任务详情
        test_get_review_detail(client, review_id)
        results.append(("获取复核任务详情", True))
        
        # 测试4: 批准复核
        test_approve_review(client, review_id, reviewer)
        results.append(("批准复核", True))
        
        # 测试5: 驳回复核
        test_reject_review(client, task, reviewer)
        results.append(("驳回复核", True))
        
        # 测试6: 数据集质量统计
        test_dataset_statistics(client, dataset)
        results.append(("数据集质量统计", True))
        
        # 测试7: 数据集复核摘要
        test_dataset_review_summary(client, dataset)
        results.append(("数据集复核摘要", True))
        
        # 测试8: 错误情况处理
        test_error_cases(client)
        results.append(("错误情况处理", True))
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        results.append(("当前测试", False))
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        results.append(("当前测试", False))
    
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
