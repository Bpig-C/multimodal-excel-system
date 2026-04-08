"""
测试标注任务详情API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_get_annotation_task():
    """测试获取标注任务详情"""
    print("\n=== 测试获取标注任务详情 ===")
    
    # 使用实际的任务ID
    task_id = "task-169dd7b91ec2"
    
    print(f"\n获取任务 {task_id} 的详情")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/annotations/{task_id}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['message']}")
            
            task_data = data['data']
            print(f"\n任务信息:")
            print(f"  - 任务ID: {task_data['task_id']}")
            print(f"  - 数据集ID: {task_data['dataset_id']}")
            print(f"  - 状态: {task_data['status']}")
            print(f"  - 标注类型: {task_data['annotation_type']}")
            print(f"  - 当前版本: {task_data['current_version']}")
            
            if task_data['corpus']:
                corpus = task_data['corpus']
                print(f"\n语料信息:")
                print(f"  - 语料ID: {corpus['text_id']}")
                print(f"  - 文本类型: {corpus['text_type']}")
                print(f"  - 有图片: {corpus['has_images']}")
                corpus_preview = corpus['text'][:100] + "..." if len(corpus['text']) > 100 else corpus['text']
                print(f"  - 文本内容: {corpus_preview}")
            
            print(f"\n标注数据:")
            print(f"  - 实体数量: {len(task_data['entities'])}")
            print(f"  - 关系数量: {len(task_data['relations'])}")
            
            if task_data['entities']:
                print(f"\n前3个实体:")
                for i, entity in enumerate(task_data['entities'][:3], 1):
                    print(f"  实体 {i}:")
                    print(f"    - ID: {entity['entity_id']}")
                    print(f"    - 文本: {entity['token']}")
                    print(f"    - 标签: {entity['label']}")
                    print(f"    - 位置: [{entity['start_offset']}, {entity['end_offset']}]")
            
            if task_data['relations']:
                print(f"\n前3个关系:")
                for i, relation in enumerate(task_data['relations'][:3], 1):
                    print(f"  关系 {i}:")
                    print(f"    - ID: {relation['relation_id']}")
                    print(f"    - 类型: {relation['relation_type']}")
                    print(f"    - 从: {relation['from_entity_id']}")
                    print(f"    - 到: {relation['to_entity_id']}")
            
            print(f"\n时间信息:")
            print(f"  - 创建时间: {task_data['created_at']}")
            print(f"  - 更新时间: {task_data['updated_at']}")
        else:
            print(f"失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试不存在的任务
    print(f"\n测试不存在的任务")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/annotations/non-existent-task")
        print(f"状态码: {response.status_code}")
        if response.status_code == 404:
            print("✓ 正确返回404")
        else:
            print(f"响应: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    test_get_annotation_task()
