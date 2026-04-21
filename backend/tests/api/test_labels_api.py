"""
标签管理API集成测试（重写）

覆盖接口：
  GET    /api/v1/labels/entities                             实体类型列表
  POST   /api/v1/labels/entities                             创建实体类型
  PUT    /api/v1/labels/entities/{id}                        更新实体类型
  DELETE /api/v1/labels/entities/{id}                        删除实体类型
  GET    /api/v1/labels/relations                            关系类型列表
  POST   /api/v1/labels/relations                            创建关系类型
  PUT    /api/v1/labels/relations/{id}                       更新关系类型
  DELETE /api/v1/labels/relations/{id}                       删除关系类型
  GET    /api/v1/labels/export                               导出标签配置
  POST   /api/v1/labels/import                               导入标签配置
  GET    /api/v1/labels/prompt-preview                       Prompt 预览
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, get_db
from models.db_models import EntityType, RelationType, User
from conftest import (
    make_test_db, get_db_override, login, auth,
    create_user, truncate_all
)

# ── 模块级 DB 初始化 ──────────────────────────────────────────────────────────
engine, SL = make_test_db("test_labels_integration.db")
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


# ── 实体类型 CRUD ─────────────────────────────────────────────────────────────

def test_list_entity_types_empty():
    """初始时实体类型列表为空"""
    resp = client.get("/api/v1/labels/entities")
    assert resp.status_code == 200
    assert resp.json()["data"]["items"] == []


def test_create_entity_type():
    """创建实体类型成功"""
    resp = client.post(
        "/api/v1/labels/entities",
        json={
            "type_name": "Product",
            "type_name_zh": "产品",
            "color": "#FF5733",
            "description": "产品型号实体"
        }
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["type_name"] == "Product"
    assert data["color"] == "#FF5733"


def test_list_entity_types_after_create():
    """创建后列表中能查到"""
    client.post("/api/v1/labels/entities", json={"type_name": "Product", "type_name_zh": "产品", "color": "#FF0000"})
    client.post("/api/v1/labels/entities", json={"type_name": "Defect", "type_name_zh": "缺陷", "color": "#00FF00"})

    resp = client.get("/api/v1/labels/entities")
    assert resp.status_code == 200
    items = resp.json()["data"]["items"]
    names = [i["type_name"] for i in items]
    assert "Product" in names
    assert "Defect" in names


def test_update_entity_type():
    """更新实体类型颜色和描述"""
    create_resp = client.post(
        "/api/v1/labels/entities",
        json={"type_name": "Customer", "type_name_zh": "客户", "color": "#AABBCC"}
    )
    et_id = create_resp.json()["data"]["id"]

    upd_resp = client.put(
        f"/api/v1/labels/entities/{et_id}",
        json={"color": "#112233", "description": "客户名称"}
    )
    assert upd_resp.status_code == 200
    assert upd_resp.json()["data"]["type_name"] == "Customer"


def test_delete_entity_type():
    """删除实体类型后列表中不再出现"""
    create_resp = client.post(
        "/api/v1/labels/entities",
        json={"type_name": "TempEntity", "type_name_zh": "临时", "color": "#999999"}
    )
    et_id = create_resp.json()["data"]["id"]

    del_resp = client.delete(f"/api/v1/labels/entities/{et_id}")
    assert del_resp.status_code == 200

    resp = client.get("/api/v1/labels/entities")
    names = [i["type_name"] for i in resp.json()["data"]["items"]]
    assert "TempEntity" not in names


def test_delete_entity_type_not_found():
    """删除不存在的实体类型返回 404"""
    resp = client.delete("/api/v1/labels/entities/99999")
    assert resp.status_code == 404


# ── 关系类型 CRUD ─────────────────────────────────────────────────────────────

def test_list_relation_types_empty():
    """初始时关系类型列表为空"""
    resp = client.get("/api/v1/labels/relations")
    assert resp.status_code == 200
    assert resp.json()["data"]["items"] == []


def test_create_relation_type():
    """创建关系类型成功"""
    resp = client.post(
        "/api/v1/labels/relations",
        json={
            "type_name": "has_defect",
            "type_name_zh": "存在缺陷",
            "color": "#FF0000",
            "description": "产品存在缺陷现象"
        }
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["type_name"] == "has_defect"


def test_update_relation_type():
    """更新关系类型描述"""
    create_resp = client.post(
        "/api/v1/labels/relations",
        json={"type_name": "caused_by", "type_name_zh": "由...导致", "color": "#0000FF"}
    )
    rt_id = create_resp.json()["data"]["id"]

    upd_resp = client.put(
        f"/api/v1/labels/relations/{rt_id}",
        json={"description": "缺陷由原因导致"}
    )
    assert upd_resp.status_code == 200


def test_delete_relation_type():
    """删除关系类型（软删除：is_active=False）"""
    create_resp = client.post(
        "/api/v1/labels/relations",
        json={"type_name": "TempRelation", "type_name_zh": "临时关系", "color": "#888888"}
    )
    rt_id = create_resp.json()["data"]["id"]

    del_resp = client.delete(f"/api/v1/labels/relations/{rt_id}")
    assert del_resp.status_code == 200

    db = SL()
    try:
        rt = db.query(RelationType).filter(RelationType.id == rt_id).first()
        assert rt is not None  # 软删除，记录仍存在
        assert rt.is_active is False  # 但已被标记为不活跃
    finally:
        db.close()


# ── 导入 / 导出 ───────────────────────────────────────────────────────────────

def test_export_labels_empty():
    """空配置时导出返回空列表"""
    resp = client.get("/api/v1/labels/export")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "entity_types" in data
    assert "relation_types" in data


def test_import_labels():
    """导入标签配置后可以查询到"""
    schema = {
        "entity_types": [
            {"type_name": "ImportedEntity", "type_name_zh": "导入实体", "color": "#ABCDEF"}
        ],
        "relation_types": [
            {"type_name": "ImportedRelation", "type_name_zh": "导入关系", "color": "#FEDCBA"}
        ]
    }
    resp = client.post("/api/v1/labels/import", json={"schema_data": schema})
    assert resp.status_code == 200

    list_resp = client.get("/api/v1/labels/entities")
    names = [i["type_name"] for i in list_resp.json()["data"]["items"]]
    assert "ImportedEntity" in names


# ── Prompt 预览 ───────────────────────────────────────────────────────────────

def test_prompt_preview():
    """Prompt 预览接口返回成功"""
    resp = client.get("/api/v1/labels/prompt-preview")
    assert resp.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
