"""
准备测试用户
为API测试创建必要的测试用户
"""
import requests

BASE_URL = "http://localhost:8000/api/v1"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login():
    """登录获取token"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
    )
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def create_user(token, username, password, role):
    """创建用户"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(
        f"{BASE_URL}/users",
        headers=headers,
        json={
            "username": username,
            "password": password,
            "role": role
        }
    )
    
    if response.status_code == 201:
        user = response.json()
        print(f"✅ 创建用户成功: {username} (ID: {user['id']}, 角色: {role})")
        return user
    elif response.status_code == 400 and "已存在" in response.text:
        print(f"ℹ️  用户已存在: {username}")
        return None
    else:
        print(f"❌ 创建用户失败: {username} - {response.text}")
        return None

def main():
    print("准备测试用户...\n")
    
    # 登录
    token = login()
    if not token:
        print("❌ 登录失败")
        return
    
    print("✅ 登录成功\n")
    
    # 创建测试用户
    test_users = [
        ("test_annotator1", "test123", "annotator"),
        ("test_annotator2", "test123", "annotator"),
        ("test_reviewer1", "test123", "reviewer"),
    ]
    
    for username, password, role in test_users:
        create_user(token, username, password, role)
    
    print("\n✅ 测试用户准备完成！")
    print("\n可用的测试账号：")
    print("  - test_annotator1 / test123 (标注员)")
    print("  - test_annotator2 / test123 (标注员)")
    print("  - test_reviewer1 / test123 (复核员)")

if __name__ == "__main__":
    main()
