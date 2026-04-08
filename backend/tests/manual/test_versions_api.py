"""
测试版本管理API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_list_versions():
    """测试获取版本列表"""
    print("=" * 60)
    print("测试: 获取版本列表")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/labels/versions")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"成功: {data['success']}")
        print(f"消息: {data['message']}")
        print(f"\n版本数量: {data['data']['total']}")
        print(f"\n版本列表:")
        for version in data['data']['items']:
            print(f"  - ID: {version['version_id']}")
            print(f"    名称: {version['version_name']}")
            print(f"    激活: {version['is_active']}")
            print(f"    实体类型数: {len(version.get('entity_types', []))}")
            print(f"    关系类型数: {len(version.get('relation_types', []))}")
            print(f"    创建时间: {version['created_at']}")
            print()
    else:
        print(f"错误: {response.text}")

if __name__ == "__main__":
    test_list_versions()
