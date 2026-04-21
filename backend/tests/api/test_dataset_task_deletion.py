"""
数据集任务删除功能测试
测试删除任务的权限控制、数据完整性和边界情况
"""
import sys
from pathlib import Path
import pytest

# 添加backend目录到Python路径
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
from models.db_models import User, Corpus, Dataset, AnnotationTask, DatasetCorpus, TextEntity, Relation

# 创建测试数据库
TEST_DATABASE_URL = "sqlite:///./tests/test_artifacts/databases/test_dataset_task_deletion.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """覆盖数据库依赖"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """模块级别的数据库设置"""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def cleanup_data():
    """每个测试后清理数据"""
    yield
    db = TestingSessionLocal()
    try:
        db.query(TextEntity).delete()
        db.query(Relation).delete()
        db.query(AnnotationTask).delete()
        db.query(DatasetCorpus).delete()
        db.query(Dataset).delete()
        db.query(Corpus).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture(scope="function")
def admin_token():
    """创建管理员并获取token"""
    db = TestingSessionLocal()
    try:
        from services.user_service import UserService
        user_service = UserService(db)

        admin = user_service.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def annotator_token():
    """创建标注员并获取token"""
    db = TestingSessionLocal()
    try:
        from services.user_service import UserService
        user_service = UserService(db)

        annotator = user_service.create_user(
            username="annotator",
            password="pass123",
            role="annotator"
        )
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "annotator", "password": "pass123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def test_dataset_with_task(admin_token):
    """创建测试数据集和任务"""
    db = TestingSessionLocal()
    try:
        # 创建语料
        corpus = Corpus(
            text_id="test_001",
            text="这是测试语料内容",
            text_type="测试类型",
            source_file="test.xlsx",
            source_row=1,
            source_field="测试字段",
            has_images=False
        )
        db.add(corpus)
        db.commit()
        db.refresh(corpus)

        # 创建数据集
        dataset = Dataset(
            dataset_id="ds-test-001",
            name="测试数据集",
            description="用于测试删除功能",
            created_by=1
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        # 创建数据集-语料关联
        assoc = DatasetCorpus(
            dataset_id=dataset.id,
            corpus_id=corpus.id
        )
        db.add(assoc)

        # 创建标注任务
        task = AnnotationTask(
            task_id="task-test-001",
            dataset_id=dataset.id,
            corpus_id=corpus.id,
            status='pending'
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        # 添加一些标注数据
        entity = TextEntity(
            entity_id=1,
            task_id=task.id,
            version=1,
            token="测试实体",
            label="Product",
            start_offset=0,
            end_offset=4
        )
        db.add(entity)
        db.commit()

        return {
            "dataset_id": dataset.dataset_id,
            "task_id": task.task_id,
            "corpus_id": corpus.id,
            "task_db_id": task.id
        }
    finally:
        db.close()


def test_delete_task_as_admin_success(admin_token, test_dataset_with_task):
    """测试管理员成功删除任务"""
    dataset_id = test_dataset_with_task["dataset_id"]
    task_id = test_dataset_with_task["task_id"]

    response = client.delete(
        f"/api/v1/datasets/{dataset_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "任务删除成功"

    # 验证任务已删除
    db = TestingSessionLocal()
    try:
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        assert task is None

        # 验证关联的标注数据也被删除（级联删除）
        entities = db.query(TextEntity).filter(
            TextEntity.task_id == test_dataset_with_task["task_db_id"]
        ).all()
        assert len(entities) == 0
    finally:
        db.close()


def test_delete_task_as_annotator_forbidden(annotator_token, test_dataset_with_task):
    """测试标注员删除任务被拒绝（权限不足）"""
    dataset_id = test_dataset_with_task["dataset_id"]
    task_id = test_dataset_with_task["task_id"]

    response = client.delete(
        f"/api/v1/datasets/{dataset_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {annotator_token}"}
    )

    assert response.status_code == 403
    data = response.json()
    assert "仅管理员可删除任务" in data["detail"]

    # 验证任务未被删除
    db = TestingSessionLocal()
    try:
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        assert task is not None
    finally:
        db.close()


def test_delete_nonexistent_task(admin_token, test_dataset_with_task):
    """测试删除不存在的任务"""
    dataset_id = test_dataset_with_task["dataset_id"]

    response = client.delete(
        f"/api/v1/datasets/{dataset_id}/tasks/task-nonexistent",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404
    data = response.json()
    assert "任务不存在或不属于该数据集" in data["detail"]


def test_delete_task_from_wrong_dataset(admin_token, test_dataset_with_task):
    """测试从错误的数据集删除任务"""
    task_id = test_dataset_with_task["task_id"]

    response = client.delete(
        f"/api/v1/datasets/ds-wrong-dataset/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code in [404, 500]  # 数据集不存在或任务不属于该数据集


def test_delete_task_without_auth():
    """测试未认证用户删除任务"""
    response = client.delete(
        "/api/v1/datasets/ds-test-001/tasks/task-test-001"
    )

    assert response.status_code == 401


def test_cascade_deletion_of_relations(admin_token):
    """测试删除任务时关系数据的级联删除"""
    db = TestingSessionLocal()
    try:
        # 创建完整的测试数据
        corpus = Corpus(
            text_id="test_002",
            text="测试关系删除",
            text_type="测试",
            source_file="test.xlsx",
            source_row=1,
            source_field="测试",
            has_images=False
        )
        db.add(corpus)
        db.commit()
        db.refresh(corpus)

        dataset = Dataset(
            dataset_id="ds-test-002",
            name="关系测试数据集",
            created_by=1
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        assoc = DatasetCorpus(dataset_id=dataset.id, corpus_id=corpus.id)
        db.add(assoc)

        task = AnnotationTask(
            task_id="task-test-002",
            dataset_id=dataset.id,
            corpus_id=corpus.id,
            status='pending'
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        # 添加实体和关系
        entity1 = TextEntity(
            entity_id=1, task_id=task.id, version=1,
            token="实体1", label="Product",
            start_offset=0, end_offset=3
        )
        entity2 = TextEntity(
            entity_id=2, task_id=task.id, version=1,
            token="实体2", label="DefectPhenomenon",
            start_offset=4, end_offset=7
        )
        db.add_all([entity1, entity2])
        db.commit()

        relation = Relation(
            relation_id=1,
            task_id=task.id,
            version=1,
            from_entity_id=1,
            to_entity_id=2,
            relation_type="has_defect"
        )
        db.add(relation)
        db.commit()

        task_db_id = task.id
    finally:
        db.close()

    # 删除任务
    response = client.delete(
        f"/api/v1/datasets/ds-test-002/tasks/task-test-002",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200

    # 验证关系也被删除
    db = TestingSessionLocal()
    try:
        relations = db.query(Relation).filter(Relation.task_id == task_db_id).all()
        assert len(relations) == 0

        entities = db.query(TextEntity).filter(TextEntity.task_id == task_db_id).all()
        assert len(entities) == 0
    finally:
        db.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
