"""
数据集分配API集成测试（新增）

覆盖接口：
  POST   /api/v1/datasets/{dataset_id}/assign           手动分配（full/range 两种模式）
  POST   /api/v1/datasets/{dataset_id}/assign/auto      自动平均分配
  GET    /api/v1/datasets/{dataset_id}/assignments      获取数据集分配列表
  DELETE /api/v1/datasets/{dataset_id}/assign/{user_id} 取消分配
  GET    /api/v1/datasets/my                            获取我的数据集（标注员）
  权限边界：非管理员调用分配接口返回 403
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, get_db
from models.db_models import (
    User, Corpus, Dataset, DatasetCorpus, AnnotationTask,
    TextEntity, Relation, ReviewTask, VersionHistory, DatasetAssignment
)
from conftest import (
    make_test_db, get_db_override, login, auth,
    create_user, create_corpus, create_dataset, create_task, truncate_all
)

# ── 模块级 DB 初始化 ──────────────────────────────────────────────────────────
engine, SL = make_test_db("test_dataset_assignment.db")
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    app.dependency_overrides[get_db] = get_db_override(SL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def cleanup():
    yield
    truncate_all(SL)


# ── 公共 fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def admin_tok():
    create_user(SL, "admin", "admin123", "admin")
    return login(client, "admin", "admin123")


@pytest.fixture(scope="function")
def annotator_tok():
    create_user(SL, "annotator", "pass123", "annotator")
    return login(client, "annotator", "pass123")


@pytest.fixture(scope="function")
def ds_ctx(admin_tok):
    """创建数据集 + 3条任务"""
    db = SL()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        admin_id = admin.id
    finally:
        db.close()

    ds_id = create_dataset(SL, "ds-assign-001", "分配测试数据集", admin_id)
    for i in range(3):
        corpus_id = create_corpus(SL, f"CORP_ASSIGN_{i:03d}", f"语料内容{i}", source_row=i + 1)
        create_task(SL, f"task-assign-{i:03d}", ds_id, corpus_id)

    return {"dataset_str_id": "ds-assign-001", "dataset_db_id": ds_id}


@pytest.fixture(scope="function")
def annotator_id(admin_tok):
    """创建标注员并返回 DB id"""
    return create_user(SL, "annotator", "pass123", "annotator")


# ── 手动分配 ──────────────────────────────────────────────────────────────────

def test_assign_full_mode(admin_tok, ds_ctx, annotator_id):
    """管理员全量分配数据集给标注员"""
    resp = client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign",
        json={"user_id": annotator_id, "role": "annotator", "mode": "full"},
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["user_id"] == annotator_id


def test_assign_range_mode(admin_tok, ds_ctx, annotator_id):
    """管理员按范围分配（任务 1-2）"""
    resp = client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign",
        json={
            "user_id": annotator_id,
            "role": "annotator",
            "mode": "range",
            "start_index": 1,
            "end_index": 2
        },
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    assert resp.json()["success"] is True


def test_assign_range_missing_index(admin_tok, ds_ctx, annotator_id):
    """range 模式缺少 start_index/end_index 返回 400"""
    resp = client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign",
        json={"user_id": annotator_id, "role": "annotator", "mode": "range"},
        headers=auth(admin_tok)
    )
    assert resp.status_code == 400


def test_assign_requires_admin(annotator_tok, ds_ctx, annotator_id):
    """非管理员分配返回 403"""
    resp = client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign",
        json={"user_id": annotator_id, "role": "annotator", "mode": "full"},
        headers=auth(annotator_tok)
    )
    assert resp.status_code == 403


def test_assign_dataset_not_found(admin_tok, annotator_id):
    """数据集不存在返回 404"""
    resp = client.post(
        "/api/v1/datasets/ds-nonexistent/assign",
        json={"user_id": annotator_id, "role": "annotator", "mode": "full"},
        headers=auth(admin_tok)
    )
    assert resp.status_code == 404


# ── 自动分配 ──────────────────────────────────────────────────────────────────

def test_auto_assign(admin_tok, ds_ctx, annotator_id):
    """自动平均分配给多个标注员"""
    annotator2_id = create_user(SL, "annotator2", "pass123", "annotator")

    resp = client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign/auto",
        json={"user_ids": [annotator_id, annotator2_id], "role": "annotator"},
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data["assignments"]) == 2


def test_auto_assign_requires_admin(annotator_tok, ds_ctx, annotator_id):
    """非管理员调用自动分配返回 403"""
    resp = client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign/auto",
        json={"user_ids": [annotator_id], "role": "annotator"},
        headers=auth(annotator_tok)
    )
    assert resp.status_code == 403


# ── 分配列表查询 ──────────────────────────────────────────────────────────────

def test_get_assignments(admin_tok, ds_ctx, annotator_id):
    """管理员获取数据集分配列表"""
    # 先创建一个分配
    client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign",
        json={"user_id": annotator_id, "role": "annotator", "mode": "full"},
        headers=auth(admin_tok)
    )

    resp = client.get(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assignments",
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data["assignments"]) >= 1


def test_get_assignments_dataset_not_found(admin_tok):
    """数据集不存在时获取分配列表返回 404"""
    resp = client.get(
        "/api/v1/datasets/ds-nonexistent/assignments",
        headers=auth(admin_tok)
    )
    assert resp.status_code == 404


# ── 我的数据集 ────────────────────────────────────────────────────────────────

def test_get_my_datasets_as_annotator(admin_tok, ds_ctx, annotator_id):
    """标注员可以看到被分配的数据集"""
    # 分配给标注员
    client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign",
        json={"user_id": annotator_id, "role": "annotator", "mode": "full"},
        headers=auth(admin_tok)
    )

    annotator_token = login(client, "annotator", "pass123")
    resp = client.get("/api/v1/datasets/my", headers=auth(annotator_token))
    assert resp.status_code == 200
    data = resp.json()["data"]
    dataset_ids = [item["dataset_id"] for item in data["items"]]
    assert ds_ctx["dataset_str_id"] in dataset_ids


def test_get_my_datasets_as_admin_empty(admin_tok):
    """管理员调用 /my 返回空列表（管理员不使用此接口）"""
    resp = client.get("/api/v1/datasets/my", headers=auth(admin_tok))
    assert resp.status_code == 200
    assert resp.json()["data"]["total"] == 0


# ── 取消分配 ──────────────────────────────────────────────────────────────────

def test_cancel_assignment(admin_tok, ds_ctx, annotator_id):
    """管理员取消分配成功"""
    # 先分配
    client.post(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign",
        json={"user_id": annotator_id, "role": "annotator", "mode": "full"},
        headers=auth(admin_tok)
    )

    resp = client.delete(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign/{annotator_id}",
        params={"role": "annotator"},
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    assert resp.json()["success"] is True

    # 验证分配已取消
    db = SL()
    try:
        assignment = db.query(DatasetAssignment).filter(
            DatasetAssignment.user_id == annotator_id,
            DatasetAssignment.is_active == True
        ).first()
        assert assignment is None
    finally:
        db.close()


def test_cancel_assignment_requires_admin(annotator_tok, ds_ctx, annotator_id):
    """非管理员取消分配返回 403"""
    resp = client.delete(
        f"/api/v1/datasets/{ds_ctx['dataset_str_id']}/assign/{annotator_id}",
        params={"role": "annotator"},
        headers=auth(annotator_tok)
    )
    assert resp.status_code == 403


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
