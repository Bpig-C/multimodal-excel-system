"""
测试不同任务的文本内容
"""
import requests

BASE_URL = "http://localhost:8000"

# 测试几个不同的任务
task_ids = [
    "task-169dd7b91ec2",  # 第一个任务
    "task-5c6c1c39a7a2",  # 第二个任务
    "task-3840c24e8f2e",  # 第三个任务
]

for task_id in task_ids:
    print(f"\n{'='*60}")
    print(f"任务ID: {task_id}")
    print('='*60)
    
    response = requests.get(f"{BASE_URL}/api/v1/annotations/{task_id}")
    
    if response.status_code == 200:
        data = response.json()['data']
        corpus = data['corpus']
        
        print(f"语料ID: {corpus['text_id']}")
        print(f"文本类型: {corpus['text_type']}")
        print(f"有图片: {corpus['has_images']}")
        print(f"文本长度: {len(corpus['text'])}")
        print(f"文本内容:")
        print(corpus['text'])
        print()
    else:
        print(f"获取失败: {response.status_code}")
