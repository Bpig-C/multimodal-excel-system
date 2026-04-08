"""
测试数据库连接和用户创建
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models.db_models import User
from services.user_service import UserService

# 创建测试数据库
TEST_DATABASE_URL = "sqlite:///./test_connection.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# 创建用户
db = TestingSessionLocal()
try:
    user_service = UserService(db)
    
    # 创建用户
    admin = user_service.create_user(
        username="admin",
        password="admin123",
        role="admin"
    )
    db.commit()
    db.refresh(admin)
    
    print(f"✓ 创建用户成功: {admin.username} (ID: {admin.id})")
    print(f"  - 密码哈希: {admin.password_hash[:50]}...")
    
    # 验证用户存在
    found_user = db.query(User).filter(User.username == "admin").first()
    if found_user:
        print(f"✓ 用户在数据库中: {found_user.username}")
    else:
        print("✗ 用户不在数据库中!")
    
    # 测试认证
    auth_user = user_service.authenticate("admin", "admin123")
    if auth_user:
        print(f"✓ 认证成功: {auth_user.username}")
    else:
        print("✗ 认证失败!")
    
    # 测试错误密码
    auth_user = user_service.authenticate("admin", "wrongpassword")
    if not auth_user:
        print("✓ 正确拒绝错误密码")
    else:
        print("✗ 错误密码被接受!")
    
finally:
    db.close()

# 清理
Base.metadata.drop_all(bind=engine)
print("\n✓ 测试完成")
