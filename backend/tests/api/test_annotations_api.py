"""
标注任务API集成测试（重写）

覆盖接口：
  GET    /api/v1/annotations                          任务列表（按角色过滤）
  GET    /api/v1/annotations/{task_id}                任务详情
  PUT    /api/v1/annotations/{task_id}                更新任务状态
  POST   /api/v1/annotations/{task_id}/entities       添加文本实体
  PUT    /api/v1/annotations/{task_id}/entities/{id}  更新文本实体
  DELETE /api/v1/annotations/{task_id}/entities/{id}  删除文本实体
  POST   /api/v1/annotations/{task_id}/relations      添加关系
  PUT    /api/v1/annotations/{task_id}/relations/{id} 更新关系
  DELETE /api/v1/annotations/{task_id}/relations/{id} 删除关系
  GET    /api/v1/annotations/batch/{job_id}           批量任务状态（不存在场景）
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
engine, SL = make_test_db("test_annotations_integration.db")
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


# ── 公共测试数据 fixture ───────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def admin_tok():
    create_user(SL, "admin", "admin123", "admin")
    return login(client, "admin", "admin123")


@pytest.fixture(scope="function")
def viewer_tok():
    create_user(SL, "viewer", "viewer123", "viewer")
    return login(client, "viewer", "viewer123")


@pytest.fixture(scope="function")
def task_ctx(admin_tok):
    """创建测试数据并返回关键 ID"""
    db = SL()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        admin_id = admin.id
    finally:
        db.close()

    corpus_id = create_corpus(SL, "CORP_ANN_001", "2022年捷普反馈排线连锡10pcs")
    ds_id = create_dataset(SL, "ds-ann-001", "标注集成测试数据集", admin_id)
    task_id = create_task(SL, "task-ann-001", ds_id, corpus_id)
    return {"task_str_id": "task-ann-001", "task_db_id": task_id}


# ── 任务列表 ──────────────────────────────────────────────────────────────────

def test_get_annotations_as_admin(admin_tok, task_ctx):
    """管理员可以获取所有任务列表"""
    resp = client.get("/api/v1/annotations", headers=auth(admin_tok))
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "items" in data["data"]
    assert data["data"]["total"] >= 1


def test_get_annotations_viewer_forbidden(viewer_tok):
    """浏览员访问任务列表返回 403"""
    resp = client.get("/api/v1/annotations", headers=auth(viewer_tok))
    assert resp.status_code == 403


def test_get_annotations_no_auth():
    """未认证访问返回 401"""
    resp = client.get("/api/v1/annotations")
    assert resp.status_code == 401


# ── 任务详情 ──────────────────────────────────────────────────────────────────

def test_get_annotation_task_detail(admin_tok, task_ctx):
    """获取任务详情，包含语料和实体列表"""
    resp = client.get(
        f"/api/v1/annotations/{task_ctx['task_str_id']}",
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["task_id"] == "task-ann-001"
    assert data["corpus"] is not None
    assert "entities" in data
    assert "relations" in data


def test_get_annotation_task_not_found(admin_tok):
    """查询不存在任务返回 404"""
    resp = client.get("/api/v1/annotations/task-nonexistent", headers=auth(admin_tok))
    assert resp.status_code == 404


# ── 更新任务状态 ──────────────────────────────────────────────────────────────

def test_update_annotation_task_status(admin_tok, task_ctx):
    """管理员可以更新任务状态"""
    resp = client.put(
        f"/api/v1/annotations/{task_ctx['task_str_id']}",
        json={"status": "completed"},
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "completed"


def test_update_task_viewer_forbidden(viewer_tok, task_ctx):
    """浏览员更新任务返回 403"""
    resp = client.put(
        f"/api/v1/annotations/{task_ctx['task_str_id']}",
        json={"status": "completed"},
        headers=auth(viewer_tok)
    )
    assert resp.status_code == 403


# ── 实体 CRUD ─────────────────────────────────────────────────────────────────

def test_add_text_entity(task_ctx):
    """添加文本实体成功"""
    resp = client.post(
        f"/api/v1/annotations/{task_ctx['task_str_id']}/entities",
        json={"token": "捷普", "label": "Customer", "start_offset": 5, "end_offset": 7}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["token"] == "捷普"
    assert data["label"] == "Customer"


def test_add_entity_missing_params(task_ctx):
    """缺少必需参数时返回 400"""
    resp = client.post(
        f"/api/v1/annotations/{task_ctx['task_str_id']}/entities",
        json={"token": "捷普"}  # 缺少 label, start_offset, end_offset
    )
    assert resp.status_code == 400


def test_update_text_entity(task_ctx):
    """更新文本实体 label"""
    # 先添加
    add_resp = client.post(
        f"/api/v1/annotations/{task_ctx['task_str_id']}/entities",
        json={"token": "CB760", "label": "Product", "start_offset": 8, "end_offset": 13}
    )
    assert add_resp.status_code == 200
    entity_db_id = add_resp.json()["data"]["id"]

    # 再更新
    upd_resp = client.put(
        f"/api/v1/annotations/{task_ctx['task_str_id']}/entities/{entity_db_id}",
        json={"label": "Defect"}
    )
    assert upd_resp.status_code == 200
    assert upd_resp.json()["data"]["label"] == "Defect"


def test_delete_text_entity(task_ctx):
    """删除文本实体后查询不到"""
    add_resp = client.post(
        f"/api/v1/annotations/{task_ctx['task_str_id']}/entities",
        json={"token": "连锡", "label": "DefectPhenomenon", "start_offset": 14, "end_offset": 16}
    )
    entity_db_id = add_resp.json()["data"]["id"]

    del_resp = client.delete(
        f"/api/v1/annotations/{task_ctx['task_str_id']}/entities/{entity_db_id}"
    )
    assert del_resp.status_code == 200

    # 验证已删除
    db = SL()
    try:
        assert db.query(TextEntity).filter(TextEntity.id == entity_db_id).first() is None
    finally:
        db.close()


def test_delete_entity_not_found(task_ctx):
    """删除不存在实体返回 404"""
    resp = client.delete(
        f"/api/v1/annotations/{task_ctx['task_str_id']}/entities/99999"
    )
    assert resp.status_code == 404


# ── 关系 CRUD ─────────────────────────────────────────────────────────────────

def test_add_relation(task_ctx):
    """添加关系：两个实体之间建立关联"""
    tid = task_ctx["task_str_id"]
    e1 = client.post(
        f"/api/v1/annotations/{tid}/entities",
        json={"token": "捷普", "label": "Customer", "start_offset": 5, "end_offset": 7}
    ).json()["data"]["entity_id"]
    e2 = client.post(
        f"/api/v1/annotations/{tid}/entities",
        json={"token": "排线连锡", "label": "DefectPhenomenon", "start_offset": 14, "end_offset": 18}
    ).json()["data"]["entity_id"]

    resp = client.post(
        f"/api/v1/annotations/{tid}/relations",
        json={"from_entity_id": e1, "to_entity_id": e2, "relation_type": "has_defect"}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["from_entity_id"] == e1
    assert data["to_entity_id"] == e2
    assert data["relation_type"] == "has_defect"


def test_add_relation_missing_entities(task_ctx):
    """实体不存在时添加关系返回 400"""
    resp = client.post(
        f"/api/v1/annotations/{task_ctx['task_str_id']}/relations",
        json={"from_entity_id": "nonexistent-1", "to_entity_id": "nonexistent-2"}
    )
    assert resp.status_code == 400


def test_delete_relation(task_ctx):
    """删除关系成功"""
    tid = task_ctx["task_str_id"]
    e1 = client.post(
        f"/api/v1/annotations/{tid}/entities",
        json={"token": "产品A", "label": "Product", "start_offset": 0, "end_offset": 3}
    ).json()["data"]["entity_id"]
    e2 = client.post(
        f"/api/v1/annotations/{tid}/entities",
        json={"token": "缺陷B", "label": "DefectPhenomenon", "start_offset": 4, "end_offset": 7}
    ).json()["data"]["entity_id"]
    rel_id = client.post(
        f"/api/v1/annotations/{tid}/relations",
        json={"from_entity_id": e1, "to_entity_id": e2, "relation_type": "has_defect"}
    ).json()["data"]["id"]

    del_resp = client.delete(f"/api/v1/annotations/{tid}/relations/{rel_id}")
    assert del_resp.status_code == 200

    db = SL()
    try:
        assert db.query(Relation).filter(Relation.id == rel_id).first() is None
    finally:
        db.close()


# ── 批量任务 ──────────────────────────────────────────────────────────────────

def test_get_batch_job_not_found(admin_tok):
    """查询不存在的批量任务返回 404"""
    resp = client.get("/api/v1/annotations/batch/job-nonexistent")
    assert resp.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
