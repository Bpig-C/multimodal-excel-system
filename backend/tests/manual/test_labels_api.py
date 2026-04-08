"""测试标签API是否正常响应"""
import requests
import json

# 测试实体类型API
print("测试实体类型API...")
try:
    response = requests.get("http://localhost:8000/api/v1/labels/entities", timeout=5)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"成功! 返回 {len(data['data']['items'])} 个实体类型")
        print(f"第一个实体: {data['data']['items'][0]['type_name_zh']}")
    else:
        print(f"失败: {response.text}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "="*60 + "\n")

# 测试关系类型API
print("测试关系类型API...")
try:
    response = requests.get("http://localhost:8000/api/v1/labels/relations", timeout=5)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"成功! 返回 {len(data['data']['items'])} 个关系类型")
        print(f"第一个关系: {data['data']['items'][0]['type_name_zh']}")
    else:
        print(f"失败: {response.text}")
except Exception as e:
    print(f"错误: {e}")
