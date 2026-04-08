"""
简单的API测试
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. 登录
print("1. 登录 annotationer...")
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "annotationer", "password": "annotationer123"}
)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    token = response.json().get("access_token")
    print(f"✓ 登录成功，token: {token[:20]}...")
    
    # 2. 获取我的数据集
    print("\n2. 获取我的数据集...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/datasets/my", headers=headers)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 成功获取数据")
        print(f"\n响应数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if data.get("data", {}).get("items"):
            print(f"\n✓ 找到 {len(data['data']['items'])} 个数据集")
        else:
            print("\n❌ 没有找到数据集")
    else:
        print(f"❌ 请求失败")
        print(response.text)
else:
    print(f"❌ 登录失败")
    print(response.text)
