"""
测试"我的数据集"API
"""
import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def login(username: str, password: str):
    """登录获取token"""
    response = requests.post(
        f"{API_BASE}/auth/login",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    else:
        print(f"登录失败: {response.status_code}")
        print(response.text)
        return None

def get_my_datasets(token: str):
    """获取我的数据集"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE}/datasets/my",
        headers=headers
    )
    print(f"\n状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json()

def get_all_datasets(token: str):
    """获取所有数据集（管理员）"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_BASE}/datasets",
        headers=headers
    )
    print(f"\n状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json()

def main():
    print("=" * 60)
    print("测试1: 管理员登录并查看所有数据集")
    print("=" * 60)
    
    admin_token = login("admin", "admin123")
    if admin_token:
        print(f"✓ 管理员登录成功")
        get_all_datasets(admin_token)
    
    print("\n" + "=" * 60)
    print("测试2: 标注员登录并查看我的数据集")
    print("=" * 60)
    
    # 尝试几个可能的标注员账号
    annotator_accounts = [
        ("annotationer", "annotationer123"),
        ("test_annotator1", "password123"),
        ("test_annotator2", "password123")
    ]
    
    for username, password in annotator_accounts:
        print(f"\n尝试登录: {username}")
        token = login(username, password)
        if token:
            print(f"✓ {username} 登录成功")
            get_my_datasets(token)
            break
    else:
        print("❌ 没有可用的标注员账号")
    
    print("\n" + "=" * 60)
    print("测试3: 复核员登录并查看我的数据集")
    print("=" * 60)
    
    reviewer_token = login("test_reviewer1", "password123")
    if reviewer_token:
        print(f"✓ 复核员登录成功")
        get_my_datasets(reviewer_token)

if __name__ == "__main__":
    main()
