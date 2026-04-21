"""
版本管理API集成测试（重写）

覆盖接口：
  GET    /api/v1/versions/{task_id}              版本历史列表
  GET    /api/v1/versions/{task_id}/{version}    版本详情
  POST   /api/v1/versions/{task_id}/snapshot     手动创建版本快照
  POST   /api/v1/versions/{task_id}/rollback     回滚到指定版本
  GET    /api/v1/versions/compare                版本对比
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
    TextEntity, Relation, VersionHistory, ReviewTask, DatasetAssignment
)
from conftest import (
    make_test_db, get_db_override, login, auth,
    create_user, create_corpus, create_dataset, create_task, truncate_all
)

# ── 模块级 DB 初始化 ──────────────────────────────────────────────────────────
engine, SL = make_test_db("test_versions_integration.db")
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
def task_ctx():
    """创建一个任务用于版本测试"""
    admin_id = create_user(SL, "admin", "admin123", "admin")
    corpus_id = create_corpus(SL, "CORP_VER_001", "版本测试语料")
    ds_id = create_dataset(SL, "ds-ver-001", "版本测试数据集", admin_id)
    task_db_id = create_task(SL, "task-ver-001", ds_id, corpus_id)
    return {"task_str_id": "task-ver-001", "task_db_id": task_db_id}


# ── 版本历史 ──────────────────────────────────────────────────────────────────

def test_get_version_history_empty(task_ctx):
    """新建任务版本历史为空"""
    resp = client.get(f"/api/v1/versions/{task_ctx['task_str_id']}")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["task_id"] == "task-ver-001"
    assert data["total"] == 0
    assert data["versions"] == []


def test_get_version_history_task_not_found():
    """不存在的任务返回 404"""
    resp = client.get("/api/v1/versions/task-nonexistent")
    assert resp.status_code == 404


# ── 创建快照 ──────────────────────────────────────────────────────────────────

def test_create_version_snapshot(task_ctx):
    """手动创建版本快照成功"""
    resp = client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/snapshot",
        json={"change_description": "测试快照"}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "history_id" in data
    assert data["task_id"] == "task-ver-001"
    assert data["version"] >= 1


def test_create_snapshot_and_list(task_ctx):
    """创建快照后历史列表中可以查到"""
    client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/snapshot",
        json={"change_description": "第一次快照"}
    )
    client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/snapshot",
        json={"change_description": "第二次快照"}
    )

    resp = client.get(f"/api/v1/versions/{task_ctx['task_str_id']}")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] >= 2


def test_create_snapshot_task_not_found():
    """对不存在的任务创建快照返回 404"""
    resp = client.post(
        "/api/v1/versions/task-nonexistent/snapshot",
        json={"change_description": "不应成功"}
    )
    assert resp.status_code == 404


# ── 版本详情 ──────────────────────────────────────────────────────────────────

def test_get_version_detail(task_ctx):
    """获取版本详情包含快照数据"""
    snap_resp = client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/snapshot",
        json={"change_description": "详情测试快照"}
    )
    version_num = snap_resp.json()["data"]["version"]

    resp = client.get(f"/api/v1/versions/{task_ctx['task_str_id']}/{version_num}")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["version"] == version_num
    assert "snapshot" in data


def test_get_version_detail_not_found(task_ctx):
    """不存在的版本号返回 404"""
    resp = client.get(f"/api/v1/versions/{task_ctx['task_str_id']}/9999")
    assert resp.status_code == 404


# ── 版本比较 ──────────────────────────────────────────────────────────────────

def test_compare_versions(task_ctx):
    """两个版本之间的对比"""
    v1 = client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/snapshot",
        json={"change_description": "对比-v1"}
    ).json()["data"]["version"]

    v2 = client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/snapshot",
        json={"change_description": "对比-v2"}
    ).json()["data"]["version"]

    resp = client.get(
        "/api/v1/versions/compare",
        params={"task_id": task_ctx["task_str_id"], "version1": v1, "version2": v2}
    )
    assert resp.status_code == 200
    assert resp.json()["success"] is True


# ── 版本回滚 ──────────────────────────────────────────────────────────────────

def test_rollback_version(task_ctx):
    """回滚到历史版本"""
    v1 = client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/snapshot",
        json={"change_description": "回滚目标"}
    ).json()["data"]["version"]

    # 再创建一个快照
    client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/snapshot",
        json={"change_description": "当前版本"}
    )

    resp = client.post(
        f"/api/v1/versions/{task_ctx['task_str_id']}/rollback",
        json={"target_version": v1}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["target_version"] == v1


def test_rollback_nonexistent_task():
    """对不存在任务回滚返回 404"""
    resp = client.post(
        "/api/v1/versions/task-nonexistent/rollback",
        json={"target_version": 1}
    )
    assert resp.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
