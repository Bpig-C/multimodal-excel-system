"""
图片标注API集成测试（重写）

覆盖接口：
  POST   /api/v1/images/{image_id}/entities           添加图片实体（整图 & 区域）
  GET    /api/v1/images/{image_id}/entities           获取图片实体列表
  PUT    /api/v1/images/{image_id}/entities/{id}      更新图片实体
  DELETE /api/v1/images/{image_id}/entities/{id}      删除图片实体
  错误场景：图片不存在、边界框参数不完整、超出图片范围
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
    TextEntity, Relation, Image, ImageEntity, ReviewTask, VersionHistory, DatasetAssignment
)
from conftest import (
    make_test_db, get_db_override,
    create_user, create_corpus, create_dataset, create_task, create_image, truncate_all
)

# ── 模块级 DB 初始化 ──────────────────────────────────────────────────────────
engine, SL = make_test_db("test_images_integration.db")
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
def img_task_ctx():
    """创建图片 + 任务"""
    admin_id = create_user(SL, "admin", "admin123", "admin")
    img_id = create_image(SL, "IMG_001", "data/images/test.png", width=800, height=600)
    corpus_id = create_corpus(SL, "CORP_IMG_001", "图片标注测试语料")
    ds_id = create_dataset(SL, "ds-img-001", "图片测试数据集", admin_id)
    task_db_id = create_task(SL, "task-img-001", ds_id, corpus_id)
    return {
        "image_str_id": "IMG_001",
        "task_str_id": "task-img-001",
        "task_db_id": task_db_id
    }


# ── 添加图片实体 ──────────────────────────────────────────────────────────────

def test_add_image_entity_whole(img_task_ctx):
    """添加整图标注（不带边界框）"""
    resp = client.post(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities",
        json={"task_id": img_task_ctx["task_str_id"], "label": "Product"}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["label"] == "Product"
    assert data["annotation_type"] == "whole_image"
    assert data["bbox"] is None


def test_add_image_entity_bbox(img_task_ctx):
    """添加区域标注（带边界框）"""
    resp = client.post(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities",
        json={
            "task_id": img_task_ctx["task_str_id"],
            "label": "Defect",
            "bbox_x": 10, "bbox_y": 20,
            "bbox_width": 100, "bbox_height": 80
        }
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["annotation_type"] == "region"
    assert data["bbox"]["x"] == 10
    assert data["bbox"]["width"] == 100


def test_add_entity_image_not_found(img_task_ctx):
    """图片不存在时返回 404"""
    resp = client.post(
        "/api/v1/images/IMG_NONEXISTENT/entities",
        json={"task_id": img_task_ctx["task_str_id"], "label": "Product"}
    )
    assert resp.status_code == 404


def test_add_entity_incomplete_bbox(img_task_ctx):
    """边界框参数不完整时返回 400"""
    resp = client.post(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities",
        json={
            "task_id": img_task_ctx["task_str_id"],
            "label": "Defect",
            "bbox_x": 10,  # 只提供 x，缺少 y, width, height
        }
    )
    assert resp.status_code == 400


def test_add_entity_bbox_out_of_range(img_task_ctx):
    """边界框超出图片范围返回 400"""
    resp = client.post(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities",
        json={
            "task_id": img_task_ctx["task_str_id"],
            "label": "Defect",
            "bbox_x": 700, "bbox_y": 500,
            "bbox_width": 200, "bbox_height": 200  # 超出 800x600
        }
    )
    assert resp.status_code == 400


# ── 获取图片实体列表 ──────────────────────────────────────────────────────────

def test_get_image_entities_empty(img_task_ctx):
    """无实体时返回空列表"""
    resp = client.get(f"/api/v1/images/{img_task_ctx['image_str_id']}/entities")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] == 0
    assert data["entities"] == []


def test_get_image_entities_after_add(img_task_ctx):
    """添加后列表中可以查到"""
    client.post(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities",
        json={"task_id": img_task_ctx["task_str_id"], "label": "Product"}
    )
    client.post(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities",
        json={
            "task_id": img_task_ctx["task_str_id"],
            "label": "Defect",
            "bbox_x": 0, "bbox_y": 0,
            "bbox_width": 50, "bbox_height": 50
        }
    )
    resp = client.get(f"/api/v1/images/{img_task_ctx['image_str_id']}/entities")
    assert resp.status_code == 200
    assert resp.json()["data"]["total"] == 2


def test_get_image_entities_not_found():
    """图片不存在时返回 404"""
    resp = client.get("/api/v1/images/IMG_NONEXISTENT/entities")
    assert resp.status_code == 404


# ── 更新图片实体 ──────────────────────────────────────────────────────────────

def test_update_image_entity_label(img_task_ctx):
    """更新图片实体 label"""
    add_resp = client.post(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities",
        json={"task_id": img_task_ctx["task_str_id"], "label": "OldLabel"}
    )
    entity_db_id = add_resp.json()["data"]["id"]

    upd_resp = client.put(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities/{entity_db_id}",
        json={"label": "NewLabel"}
    )
    assert upd_resp.status_code == 200
    assert upd_resp.json()["data"]["label"] == "NewLabel"


def test_update_image_entity_not_found(img_task_ctx):
    """更新不存在的图片实体返回 404"""
    resp = client.put(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities/99999",
        json={"label": "NewLabel"}
    )
    assert resp.status_code == 404


# ── 删除图片实体 ──────────────────────────────────────────────────────────────

def test_delete_image_entity(img_task_ctx):
    """删除图片实体成功"""
    add_resp = client.post(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities",
        json={"task_id": img_task_ctx["task_str_id"], "label": "ToDelete"}
    )
    entity_db_id = add_resp.json()["data"]["id"]

    del_resp = client.delete(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities/{entity_db_id}"
    )
    assert del_resp.status_code == 200

    db = SL()
    try:
        assert db.query(ImageEntity).filter(ImageEntity.id == entity_db_id).first() is None
    finally:
        db.close()


def test_delete_image_entity_not_found(img_task_ctx):
    """删除不存在的图片实体返回 404"""
    resp = client.delete(
        f"/api/v1/images/{img_task_ctx['image_str_id']}/entities/99999"
    )
    assert resp.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
