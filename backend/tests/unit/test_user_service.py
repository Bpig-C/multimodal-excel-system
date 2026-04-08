"""
用户管理服务测试脚本
测试用户CRUD、认证和权限检查
"""
import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base
from services.user_service import UserService


@pytest.fixture(scope="module")
def db():
    """创建测试数据库 fixture"""
    engine = create_engine('sqlite:///./tests/test_artifacts/databases/test_user_service.db', echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def service(db):
    """创建 UserService fixture"""
    return UserService(db)


@pytest.fixture(scope="module")
def admin(service):
    """创建管理员用户 fixture"""
    return service.create_user("admin", "admin123", "admin")


@pytest.fixture(scope="module")
def annotator(service):
    """创建标注人员 fixture"""
    return service.create_user("annotator1", "pass123", "annotator")


@pytest.fixture(scope="module")
def reviewer(service):
    """创建复核人员 fixture"""
    return service.create_user("reviewer1", "pass123", "reviewer")


def test_create_user(service, admin, annotator, reviewer):
    """测试创建用户"""
    # 验证用户已创建
    assert admin is not None
    assert admin.username == "admin"
    assert admin.role == "admin"
    
    assert annotator is not None
    assert annotator.username == "annotator1"
    assert annotator.role == "annotator"
    
    assert reviewer is not None
    assert reviewer.username == "reviewer1"
    assert reviewer.role == "reviewer"


def test_duplicate_username(service):
    """测试重复用户名"""
    with pytest.raises(ValueError):
        service.create_user("admin", "password", "admin")


def test_invalid_role(service):
    """测试无效角色"""
    with pytest.raises(ValueError):
        service.create_user("test_user", "password", "invalid_role")


def test_get_user(service, admin):
    """测试获取用户"""
    # 根据ID获取
    user = service.get_user_by_id(admin.id)
    assert user is not None
    assert user.username == admin.username
    
    # 根据用户名获取
    user = service.get_user_by_username(admin.username)
    assert user is not None
    assert user.id == admin.id


def test_list_users(service):
    """测试获取用户列表"""
    # 获取所有用户
    users, total = service.list_users()
    assert total >= 3  # At least admin, annotator, reviewer
    
    # 按角色筛选
    admins, admin_count = service.list_users(role='admin')
    assert admin_count >= 1
    
    annotators, annotator_count = service.list_users(role='annotator')
    assert annotator_count >= 1


def test_update_user(service):
    """测试更新用户"""
    # Create a separate user for update testing
    test_user = service.create_user("test_update_user", "pass123", "annotator")
    
    # 更新用户名
    updated = service.update_user(test_user.id, username="annotator_new")
    assert updated.username == "annotator_new"
    
    # 更新角色
    updated = service.update_user(test_user.id, role="reviewer")
    assert updated.role == "reviewer"
    
    # 更新密码
    updated = service.update_user(test_user.id, password="newpass123")
    assert updated is not None


def test_authenticate(service, admin):
    """测试用户认证"""
    # 正确的用户名和密码
    user = service.authenticate("admin", "admin123")
    assert user is not None
    assert user.id == admin.id
    
    # 错误的密码
    user = service.authenticate("admin", "wrongpassword")
    assert user is None
    
    # 不存在的用户
    user = service.authenticate("nonexistent", "password")
    assert user is None


def test_jwt_token(service, admin):
    """测试JWT令牌"""
    # 创建令牌
    token = service.create_access_token(
        admin.id,
        admin.username,
        admin.role
    )
    assert token is not None
    assert len(token) > 0
    
    # 验证令牌
    payload = service.verify_token(token)
    assert payload is not None
    assert payload['user_id'] == admin.id
    assert payload['username'] == admin.username
    assert payload['role'] == admin.role
    
    # 验证无效令牌
    invalid_payload = service.verify_token("invalid_token")
    assert invalid_payload is None


def test_permissions(service, admin, annotator, reviewer):
    """测试权限检查"""
    # 管理员拥有所有权限
    assert service.check_permission(admin.id, 'admin') == True
    assert service.check_permission(admin.id, 'annotator') == True
    
    # 标注人员只有标注权限
    assert service.check_permission(annotator.id, 'annotator') == True
    assert service.check_permission(annotator.id, 'admin') == False
    
    # 复核权限检查
    assert service.can_review(admin.id) == True
    assert service.can_review(reviewer.id) == True
    assert service.can_review(annotator.id) == True


def test_user_statistics(service):
    """测试用户统计"""
    stats = service.get_user_statistics()
    
    assert 'total_users' in stats
    assert 'admin_count' in stats
    assert 'annotator_count' in stats
    assert 'reviewer_count' in stats
    assert stats['total_users'] >= 3


def test_delete_user(service, reviewer):
    """测试删除用户"""
    # 删除用户
    result = service.delete_user(reviewer.id)
    assert result == True
    
    # 验证用户已删除
    user = service.get_user_by_id(reviewer.id)
    assert user is None
