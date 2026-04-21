"""
处理器配置API集成测试（新增）

覆盖接口：
  GET /api/v1/config/processors                          处理器列表
  GET /api/v1/config/processors/{name}/graph-config      图谱可视化配置
  GET /api/v1/config/processors/{name}/field-mapping     字段映射配置
  错误场景：处理器不存在返回 404
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, get_db
from models.db_models import User
from conftest import make_test_db, get_db_override, login, auth, create_user, truncate_all

# ── 模块级 DB 初始化 ──────────────────────────────��───────────────────────────
engine, SL = make_test_db("test_config_api.db")
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


@pytest.fixture(scope="function")
def admin_tok():
    create_user(SL, "admin", "admin123", "admin")
    return login(client, "admin", "admin123")


# ── 处理器列表 ────────────────────────────────────────────────────────────────

def test_list_processors(admin_tok):
    """获取所有可用处理器列表，至少包含一个处理器"""
    resp = client.get("/api/v1/config/processors", headers=auth(admin_tok))
    assert resp.status_code == 200
    data = resp.json()
    assert "processors" in data
    assert isinstance(data["processors"], list)
    assert len(data["processors"]) >= 1


def test_list_processors_no_auth():
    """未认证访问处理器列表返回 401"""
    resp = client.get("/api/v1/config/processors")
    assert resp.status_code == 401


def test_processor_names_have_required_fields(admin_tok):
    """每个处理器条目应有 name 和 display_name 字段"""
    resp = client.get("/api/v1/config/processors", headers=auth(admin_tok))
    for processor in resp.json()["processors"]:
        assert "name" in processor, f"处理器缺少 name 字段: {processor}"
        assert "display_name" in processor, f"处理器缺少 display_name 字段: {processor}"


# ── 图谱配置 ──────────────────────────────────────────────────────────────────

def test_get_graph_config_valid(admin_tok):
    """用第一个处理器的名称获取图谱配置"""
    processors = client.get(
        "/api/v1/config/processors", headers=auth(admin_tok)
    ).json()["processors"]

    if not processors:
        pytest.skip("没有注册的处理器，跳过此测试")

    first_name = processors[0]["name"]
    resp = client.get(
        f"/api/v1/config/processors/{first_name}/graph-config",
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["processor"] == first_name
    assert "node_types" in data
    assert "edge_labels" in data


def test_get_graph_config_not_found(admin_tok):
    """不存在的处理器返回 404"""
    resp = client.get(
        "/api/v1/config/processors/nonexistent_processor/graph-config",
        headers=auth(admin_tok)
    )
    assert resp.status_code == 404


# ── 字段映射 ──────────────────────────────────────────────────────────────────

def test_get_field_mapping_valid(admin_tok):
    """用第一个处理器的名称获取字段映射"""
    processors = client.get(
        "/api/v1/config/processors", headers=auth(admin_tok)
    ).json()["processors"]

    if not processors:
        pytest.skip("没有注册的处理器，跳过此测试")

    first_name = processors[0]["name"]
    resp = client.get(
        f"/api/v1/config/processors/{first_name}/field-mapping",
        headers=auth(admin_tok)
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["processor"] == first_name
    assert "field_mapping" in data


def test_get_field_mapping_not_found(admin_tok):
    """不存在的处理器返回 404"""
    resp = client.get(
        "/api/v1/config/processors/nonexistent_processor/field-mapping",
        headers=auth(admin_tok)
    )
    assert resp.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
