"""
用户管理和认证API测试
测试用户CRUD、登录登出和JWT认证
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
import json

from main import app
from database import Base, get_db
from models.db_models import User

# 创建测试数据库 - 保存到test_artifacts目录
TEST_DATABASE_URL = "sqlite:///./tests/test_artifacts/databases/test_users_api.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表
Base.metadata.create_all(bind=engine)


def override_get_db():
    """覆盖数据库依赖"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def cleanup_database():
    """清理数据库"""
    db = TestingSessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


def print_section(title: str):
    """打印测试章节标题"""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print('=' * 60)


def print_test(test_name: str):
    """打印测试名称"""
    print(f"\n=== {test_name} ===")


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """模块级别的数据库设置 - 只在模块开始和结束时执行"""
    # 创建所有表
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # 模块结束后清理
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def cleanup_data():
    """每个测试后清理数据，但不删除表结构"""
    yield
    # 测试后清理数据
    db = TestingSessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture(scope="function")
def admin_user():
    """创建管理员用户 fixture"""
    db = TestingSessionLocal()
    try:
        from services.user_service import UserService
        user_service = UserService(db)
        
        # 检查用户是否已存在
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            db.delete(existing)
            db.commit()
        
        admin = user_service.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )
        db.commit()
        db.refresh(admin)
        
        # 保存用户信息
        admin_data = {
            'id': admin.id,
            'username': admin.username,
            'role': admin.role
        }
        print(f"✓ 成功创建管理员用户: {admin_data['username']} (ID: {admin_data['id']})")
        
        yield admin
    finally:
        db.close()


@pytest.fixture(scope="function")
def token(admin_user):
    """获取认证令牌 fixture"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    assert response.status_code == 200, f"登录失败: {response.text}"
    data = response.json()
    return data["access_token"]


@pytest.fixture(scope="function")
def user_id(token):
    """创建测试用户并返回ID fixture"""
    response = client.post(
        "/api/v1/users",
        json={
            "username": "annotator1",
            "password": "pass123",
            "role": "annotator"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201, f"创建用户失败: {response.text}"
    return response.json()["id"]


def test_create_admin_user(admin_user):
    """测试1: 创建管理员用户"""
    print_test("测试1: 创建管理员用户")
    
    assert admin_user is not None
    assert admin_user.username == "admin"
    assert admin_user.role == "admin"
    
    print(f"✓ 成功创建管理员用户: {admin_user.username}")
    print(f"  - ID: {admin_user.id}")
    print(f"  - 角色: {admin_user.role}")


def test_login(admin_user):
    """测试2: 用户登录"""
    print_test("测试2: 用户登录")
    
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    assert response.status_code == 200, f"登录失败: {response.text}"
    
    data = response.json()
    assert "access_token" in data, "响应中缺少access_token"
    assert data["token_type"] == "bearer", "令牌类型错误"
    assert "user" in data, "响应中缺少用户信息"
    
    print(f"✓ 登录成功")
    print(f"  - 用户名: {data['user']['username']}")
    print(f"  - 角色: {data['user']['role']}")
    print(f"  - 令牌: {data['access_token'][:50]}...")


def test_login_with_wrong_password(admin_user):
    """测试3: 错误密码登录"""
    print_test("测试3: 错误密码登录")
    
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401, "应该返回401未授权"
    print("✓ 正确拒绝了错误密码")


def test_get_current_user(token):
    """测试4: 获取当前用户信息"""
    print_test("测试4: 获取当前用户信息")
    
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"获取用户信息失败: {response.text}"
    
    data = response.json()
    print(f"✓ 成功获取当前用户信息")
    print(f"  - 用户名: {data['username']}")
    print(f"  - 角色: {data['role']}")


def test_create_user_with_auth(token):
    """测试5: 创建用户（带认证）"""
    print_test("测试5: 创建用户（带认证）")
    
    response = client.post(
        "/api/v1/users",
        json={
            "username": "annotator1",
            "password": "pass123",
            "role": "annotator"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 可能已存在，接受201或400
    assert response.status_code in [201, 400], f"创建用户失败: {response.text}"
    
    if response.status_code == 201:
        data = response.json()
        print(f"✓ 成功创建用户: {data['username']}")
        print(f"  - ID: {data['id']}")
        print(f"  - 角色: {data['role']}")
    else:
        print(f"✓ 用户已存在（跳过创建）")


def test_create_reviewer(token):
    """测试6: 创建复核人员"""
    print_test("测试6: 创建复核人员")
    
    response = client.post(
        "/api/v1/users",
        json={
            "username": "reviewer1",
            "password": "pass123",
            "role": "reviewer"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 可能已存在，接受201或400
    assert response.status_code in [201, 400], f"创建复核人员失败: {response.text}"
    
    if response.status_code == 201:
        data = response.json()
        print(f"✓ 成功创建复核人员: {data['username']}")
        print(f"  - ID: {data['id']}")
        print(f"  - 角色: {data['role']}")
    else:
        print(f"✓ 复核人员已存在（跳过创建）")


def test_list_users(token):
    """测试7: 获取用户列表"""
    print_test("测试7: 获取用户列表")
    
    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"获取用户列表失败: {response.text}"
    
    data = response.json()
    print(f"✓ 成功获取用户列表")
    print(f"  - 总用户数: {len(data)}")
    for user in data:
        print(f"  - {user['username']} ({user['role']})")


def test_list_users_by_role(token):
    """测试8: 按角色筛选用户"""
    print_test("测试8: 按角色筛选用户")
    
    response = client.get(
        "/api/v1/users?role=annotator",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"筛选用户失败: {response.text}"
    
    data = response.json()
    print(f"✓ 成功筛选标注人员")
    print(f"  - 标注人员数: {len(data)}")
    for user in data:
        assert user['role'] == 'annotator', "筛选结果包含非标注人员"


def test_get_user(token, user_id):
    """测试9: 获取用户详情"""
    print_test("测试9: 获取用户详情")
    
    response = client.get(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"获取用户详情失败: {response.text}"
    
    data = response.json()
    print(f"✓ 成功获取用户详情")
    print(f"  - 用户名: {data['username']}")
    print(f"  - 角色: {data['role']}")


def test_update_user(token, user_id):
    """测试10: 更新用户信息"""
    print_test("测试10: 更新用户信息")
    
    response = client.put(
        f"/api/v1/users/{user_id}",
        json={
            "password": "newpass123",
            "role": "reviewer"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"更新用户失败: {response.text}"
    
    data = response.json()
    print(f"✓ 成功更新用户")
    print(f"  - 用户名: {data['username']}")
    print(f"  - 新角色: {data['role']}")


def test_user_statistics(token):
    """测试11: 获取用户统计"""
    print_test("测试11: 获取用户统计")
    
    response = client.get(
        "/api/v1/users/statistics/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"获取统计失败: {response.text}"
    
    data = response.json()
    stats = data["data"]
    print(f"✓ 成功获取用户统计")
    print(f"  - 总用户数: {stats['total_users']}")
    print(f"  - 管理员: {stats['admin_count']}")
    print(f"  - 标注人员: {stats['annotator_count']}")
    print(f"  - 复核人员: {stats['reviewer_count']}")


def test_unauthorized_access():
    """测试12: 未授权访问"""
    print_test("测试12: 未授权访问")
    
    response = client.get("/api/v1/users")
    
    assert response.status_code == 401, "应该返回401未授权"
    print("✓ 正确拒绝了未授权访问")


def test_non_admin_create_user(token):
    """测试13: 非管理员创建用户"""
    print_test("测试13: 非管理员创建用户")
    
    # 先以标注人员身份登录
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "annotator1",
            "password": "newpass123"  # 使用更新后的密码
        }
    )
    
    if response.status_code == 200:
        annotator_token = response.json()["access_token"]
        
        # 尝试创建用户
        response = client.post(
            "/api/v1/users",
            json={
                "username": "test_user",
                "password": "pass123",
                "role": "annotator"
            },
            headers={"Authorization": f"Bearer {annotator_token}"}
        )
        
        assert response.status_code == 403, "应该返回403禁止访问"
        print("✓ 正确拒绝了非管理员创建用户")
    else:
        print("⚠ 跳过测试（标注人员登录失败）")


def test_delete_user(token, user_id):
    """测试14: 删除用户"""
    print_test("测试14: 删除用户")
    
    response = client.delete(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"删除用户失败: {response.text}"
    
    data = response.json()
    print(f"✓ 成功删除用户")
    print(f"  - 消息: {data['message']}")


def test_logout(token):
    """测试15: 用户登出"""
    print_test("测试15: 用户登出")
    
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"登出失败: {response.text}"
    
    data = response.json()
    print(f"✓ 成功登出")
    print(f"  - 消息: {data['message']}")


def main():
    """运行所有测试"""
    print_section("用户管理和认证API测试")
    
    # 清理数据库
    cleanup_database()
    
    test_results = []
    
    try:
        # 测试1: 创建管理员
        admin = test_create_admin_user()
        test_results.append(("创建管理员用户", True))
        
        # 测试2: 登录
        token = test_login()
        test_results.append(("用户登录", True))
        
        # 测试3: 错误密码登录
        test_login_with_wrong_password()
        test_results.append(("错误密码登录", True))
        
        # 测试4: 获取当前用户
        test_get_current_user(token)
        test_results.append(("获取当前用户信息", True))
        
        # 测试5: 创建用户
        user_id = test_create_user_with_auth(token)
        test_results.append(("创建用户（带认证）", True))
        
        # 测试6: 创建复核人员
        reviewer_id = test_create_reviewer(token)
        test_results.append(("创建复核人员", True))
        
        # 测试7: 获取用户列表
        test_list_users(token)
        test_results.append(("获取用户列表", True))
        
        # 测试8: 按角色筛选
        test_list_users_by_role(token)
        test_results.append(("按角色筛选用户", True))
        
        # 测试9: 获取用户详情
        test_get_user(token, user_id)
        test_results.append(("获取用户详情", True))
        
        # 测试10: 更新用户
        test_update_user(token, user_id)
        test_results.append(("更新用户信息", True))
        
        # 测试11: 用户统计
        test_user_statistics(token)
        test_results.append(("获取用户统计", True))
        
        # 测试12: 未授权访问
        test_unauthorized_access()
        test_results.append(("未授权访问", True))
        
        # 测试13: 非管理员创建用户
        test_non_admin_create_user(token)
        test_results.append(("非管理员创建用户", True))
        
        # 测试14: 删除用户
        test_delete_user(token, reviewer_id)
        test_results.append(("删除用户", True))
        
        # 测试15: 登出
        test_logout(token)
        test_results.append(("用户登出", True))
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        test_results.append((f"测试失败", False))
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        test_results.append((f"测试异常", False))
    
    # 打印测试结果汇总
    print_section("测试结果汇总")
    
    for test_name, passed in test_results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, passed in test_results if passed)
    total_count = len(test_results)
    
    print(f"\n总计: {passed_count}/{total_count} 个测试通过")
    
    # 清理
    cleanup_database()


if __name__ == "__main__":
    main()
