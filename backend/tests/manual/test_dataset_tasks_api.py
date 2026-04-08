"""
测试数据集任务列表API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_get_dataset_tasks():
    """测试获取数据集任务列表"""
    print("\n=== 测试获取数据集任务列表 ===")
    
    # 使用实际的数据集ID
    dataset_id = "ds-6679ffb02b3d"
    
    # 测试基本查询
    print(f"\n1. 获取数据集 {dataset_id} 的任务列表（第1页，每页20条）")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/datasets/{dataset_id}/tasks",
            params={"page": 1, "page_size": 20}
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['message']}")
            print(f"总数: {data['data']['total']}")
            print(f"当前页: {data['data']['page']}")
            print(f"每页数量: {data['data']['page_size']}")
            print(f"返回任务数: {len(data['data']['items'])}")
            
            if data['data']['items']:
                print("\n前3个任务详情:")
                for i, task in enumerate(data['data']['items'][:3], 1):
                    print(f"\n任务 {i}:")
                    print(f"  - 任务ID: {task['task_id']}")
                    corpus_preview = task['corpus_text'][:80] + "..." if len(task['corpus_text']) > 80 else task['corpus_text']
                    print(f"  - 语料文本: {corpus_preview}")
                    print(f"  - 状态: {task['status']}")
                    print(f"  - 标注类型: {task['annotation_type']}")
                    print(f"  - 实体数: {task['entity_count']}")
                    print(f"  - 关系数: {task['relation_count']}")
                    print(f"  - 更新时间: {task['updated_at']}")
        else:
            print(f"失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试状态筛选
    print(f"\n2. 获取数据集 {dataset_id} 的待处理任务")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/datasets/{dataset_id}/tasks",
            params={"page": 1, "page_size": 20, "status": "pending"}
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"待处理任务数: {data['data']['total']}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试不存在的数据集
    print(f"\n3. 测试不存在的数据集")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/datasets/non-existent-id/tasks",
            params={"page": 1, "page_size": 20}
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 404:
            print("✓ 正确返回404")
        else:
            print(f"响应: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    test_get_dataset_tasks()

