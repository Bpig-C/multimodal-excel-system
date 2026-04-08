"""
Task 47: 数据集分配API测试脚本
测试所有新增的数据集分配API端点
"""
import requests
import json
from typing import Optional

# 配置
BASE_URL = "http://localhost:8000/api/v1"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# 全局变量
access_token: Optional[str] = None
test_dataset_id: Optional[str] = None
test_user_ids: list = []


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_success(msg: str):
    """打印成功消息"""
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")


def print_error(msg: str):
    """打印错误消息"""
    print(f"{Colors.RED}❌ {msg}{Colors.END}")


def print_info(msg: str):
    """打印信息消息"""
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")


def print_warning(msg: str):
    """打印警告消息"""
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}\n")


def login() -> bool:
    """登录获取token"""
    global access_token
    
    print_section("1. 用户登录")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            print_success(f"登录成功，获取token: {access_token[:20]}...")
            return True
        else:
            print_error(f"登录失败: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print_error(f"登录异常: {str(e)}")
        return False


def get_headers() -> dict:
    """获取请求头"""
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }


def prepare_test_data() -> bool:
    """准备测试数据"""
    global test_dataset_id, test_user_ids
    
    print_section("2. 准备测试数据")
    
    try:
        # 获取数据集列表
        print_info("获取数据集列表...")
        response = requests.get(
            f"{BASE_URL}/datasets",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            datasets = data.get("data", {}).get("items", [])
            
            if datasets:
                test_dataset_id = datasets[0]["dataset_id"]
                print_success(f"找到测试数据集: {test_dataset_id}")
            else:
                print_warning("没有找到数据集，请先创建数据集")
                return False
        else:
            print_error(f"获取数据集失败: {response.status_code}")
            return False
        
        # 获取用户列表
        print_info("获取用户列表...")
        response = requests.get(
            f"{BASE_URL}/users",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            users = response.json()
            # 过滤掉管理员，获取标注员
            test_user_ids = [
                u["id"] for u in users 
                if u["role"] in ["annotator", "reviewer"] and u["id"] != 1
            ]
            
            if len(test_user_ids) >= 2:
                print_success(f"找到测试用户: {test_user_ids}")
            else:
                print_warning("测试用户不足（需要至少2个标注员/复核员）")
                return False
        else:
            print_error(f"获取用户失败: {response.status_code}")
            return False
        
        return True
    
    except Exception as e:
        print_error(f"准备测试数据异常: {str(e)}")
        return False


def test_assign_full() -> bool:
    """测试整体分配"""
    print_section("3. 测试整体分配 (POST /datasets/{id}/assign)")
    
    try:
        user_id = test_user_ids[0]
        
        print_info(f"分配数据集 {test_dataset_id} 给用户 {user_id}（整体分配）...")
        
        response = requests.post(
            f"{BASE_URL}/datasets/{test_dataset_id}/assign",
            headers=get_headers(),
            json={
                "user_id": user_id,
                "role": "annotator",
                "mode": "full"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("整体分配成功")
            print_info(f"分配信息: {json.dumps(data.get('data'), indent=2, ensure_ascii=False)}")
            return True
        else:
            print_error(f"整体分配失败: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print_error(f"整体分配异常: {str(e)}")
        return False


def test_get_assignments() -> bool:
    """测试获取分配情况"""
    print_section("4. 测试获取分配情况 (GET /datasets/{id}/assignments)")
    
    try:
        print_info(f"获取数据集 {test_dataset_id} 的分配情况...")
        
        response = requests.get(
            f"{BASE_URL}/datasets/{test_dataset_id}/assignments",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("获取分配情况成功")
            assignments = data.get("data", {}).get("assignments", [])
            print_info(f"当前分配数: {len(assignments)}")
            
            for assignment in assignments:
                print_info(f"  - 用户: {assignment['username']}, "
                          f"角色: {assignment['role']}, "
                          f"范围: {assignment['task_range']}, "
                          f"任务数: {assignment['task_count']}")
            
            return True
        else:
            print_error(f"获取分配情况失败: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print_error(f"获取分配情况异常: {str(e)}")
        return False


def test_cancel_assignment() -> bool:
    """测试取消分配"""
    print_section("5. 测试取消分配 (DELETE /datasets/{id}/assign/{user_id})")
    
    try:
        user_id = test_user_ids[0]
        
        print_info(f"取消用户 {user_id} 的分配...")
        
        response = requests.delete(
            f"{BASE_URL}/datasets/{test_dataset_id}/assign/{user_id}",
            headers=get_headers(),
            params={"role": "annotator"}
        )
        
        if response.status_code == 200:
            print_success("取消分配成功")
            return True
        elif response.status_code == 400:
            # 可能是因为有已完成任务
            error_data = response.json()
            if isinstance(error_data.get("detail"), dict):
                detail = error_data["detail"]
                if detail.get("action") == "transfer":
                    print_warning("不能直接取消（有已完成任务），需要使用转移功能")
                    return True  # 这是预期行为
            print_error(f"取消分配失败: {response.text}")
            return False
        else:
            print_error(f"取消分配失败: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print_error(f"取消分配异常: {str(e)}")
        return False


def test_assign_range() -> bool:
    """测试范围分配"""
    print_section("6. 测试范围分配 (POST /datasets/{id}/assign)")
    
    try:
        # 先获取数据集的任务数
        response = requests.get(
            f"{BASE_URL}/datasets/{test_dataset_id}",
            headers=get_headers()
        )
        
        if response.status_code != 200:
            print_error("无法获取数据集信息")
            return False
        
        dataset = response.json().get("data", {})
        total_tasks = len(dataset.get("task_list", []))
        
        if total_tasks < 2:
            print_warning(f"任务数太少（{total_tasks}），跳过范围分配测试")
            return True
        
        # 分配给第一个用户：1 到 total_tasks//2
        user1_id = test_user_ids[0]
        mid_point = total_tasks // 2
        
        print_info(f"分配任务 1-{mid_point} 给用户 {user1_id}...")
        
        response = requests.post(
            f"{BASE_URL}/datasets/{test_dataset_id}/assign",
            headers=get_headers(),
            json={
                "user_id": user1_id,
                "role": "annotator",
                "mode": "range",
                "start_index": 1,
                "end_index": mid_point
            }
        )
        
        if response.status_code == 200:
            print_success(f"范围分配成功（1-{mid_point}）")
        else:
            print_error(f"范围分配失败: {response.status_code} - {response.text}")
            return False
        
        # 如果有第二个用户，分配剩余任务
        if len(test_user_ids) >= 2 and mid_point < total_tasks:
            user2_id = test_user_ids[1]
            
            print_info(f"分配任务 {mid_point+1}-{total_tasks} 给用户 {user2_id}...")
            
            response = requests.post(
                f"{BASE_URL}/datasets/{test_dataset_id}/assign",
                headers=get_headers(),
                json={
                    "user_id": user2_id,
                    "role": "annotator",
                    "mode": "range",
                    "start_index": mid_point + 1,
                    "end_index": total_tasks
                }
            )
            
            if response.status_code == 200:
                print_success(f"范围分配成功（{mid_point+1}-{total_tasks}）")
            else:
                print_error(f"范围分配失败: {response.status_code} - {response.text}")
                return False
        
        return True
    
    except Exception as e:
        print_error(f"范围分配异常: {str(e)}")
        return False


def test_auto_assign() -> bool:
    """测试自动分配"""
    print_section("7. 测试自动分配 (POST /datasets/{id}/assign/auto)")
    
    try:
        # 先清理现有分配
        print_info("清理现有分配...")
        for user_id in test_user_ids[:2]:
            requests.delete(
                f"{BASE_URL}/datasets/{test_dataset_id}/assign/{user_id}",
                headers=get_headers(),
                params={"role": "annotator", "force": True}
            )
        
        # 自动分配给多个用户
        print_info(f"自动分配给用户 {test_user_ids[:2]}...")
        
        response = requests.post(
            f"{BASE_URL}/datasets/{test_dataset_id}/assign/auto",
            headers=get_headers(),
            json={
                "user_ids": test_user_ids[:2],
                "role": "annotator"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("自动分配成功")
            assignments = data.get("data", {}).get("assignments", [])
            total_tasks = data.get("data", {}).get("total_tasks", 0)
            
            print_info(f"总任务数: {total_tasks}")
            for assignment in assignments:
                print_info(f"  - 用户: {assignment['username']}, "
                          f"范围: {assignment['task_range']}, "
                          f"任务数: {assignment['task_count']}")
            
            return True
        else:
            print_error(f"自动分配失败: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print_error(f"自动分配异常: {str(e)}")
        return False


def test_transfer_assignment() -> bool:
    """测试转移分配"""
    print_section("8. 测试转移分配 (POST /datasets/{id}/assign/transfer)")
    
    try:
        if len(test_user_ids) < 3:
            print_warning("测试用户不足（需要3个），跳过转移测试")
            return True
        
        # 先清理所有分配
        print_info("清理现有分配...")
        for user_id in test_user_ids:
            requests.delete(
                f"{BASE_URL}/datasets/{test_dataset_id}/assign/{user_id}",
                headers=get_headers(),
                params={"role": "annotator", "force": True}
            )
        
        # 分配给第一个用户
        old_user_id = test_user_ids[0]
        print_info(f"先分配给用户 {old_user_id}...")
        
        response = requests.post(
            f"{BASE_URL}/datasets/{test_dataset_id}/assign",
            headers=get_headers(),
            json={
                "user_id": old_user_id,
                "role": "annotator",
                "mode": "full"
            }
        )
        
        if response.status_code != 200:
            print_error("初始分配失败")
            return False
        
        # 转移给第二个用户（确保第二个用户没有分配）
        new_user_id = test_user_ids[1]
        
        print_info(f"转移分配：从用户 {old_user_id} 到用户 {new_user_id}...")
        
        response = requests.post(
            f"{BASE_URL}/datasets/{test_dataset_id}/assign/transfer",
            headers=get_headers(),
            json={
                "old_user_id": old_user_id,
                "new_user_id": new_user_id,
                "role": "annotator",
                "transfer_mode": "all",
                "transfer_reason": "测试转移功能"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("转移分配成功")
            result = data.get("data", {})
            print_info(f"转移详情: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return True
        else:
            print_error(f"转移分配失败: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print_error(f"转移分配异常: {str(e)}")
        return False


def test_get_my_datasets() -> bool:
    """测试获取我的数据集"""
    print_section("9. 测试获取我的数据集 (GET /datasets/my)")
    
    try:
        print_info("获取我的数据集...")
        
        response = requests.get(
            f"{BASE_URL}/datasets/my",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("获取我的数据集成功")
            
            items = data.get("data", {}).get("items", [])
            total = data.get("data", {}).get("total", 0)
            
            print_info(f"我的数据集数量: {total}")
            
            if items:
                for item in items:
                    print_info(f"  - 数据集: {item['name']}, "
                              f"角色: {item['my_role']}, "
                              f"范围: {item['my_task_range']}, "
                              f"进度: {item['my_completed_count']}/{item['my_task_count']}")
            else:
                print_info("  （管理员账号，返回空列表是正常的）")
            
            return True
        else:
            print_error(f"获取我的数据集失败: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print_error(f"获取我的数据集异常: {str(e)}")
        return False


def test_range_overlap() -> bool:
    """测试范围重叠检查"""
    print_section("10. 测试范围重叠检查")
    
    try:
        # 先清理
        print_info("清理现有分配...")
        for user_id in test_user_ids[:2]:
            requests.delete(
                f"{BASE_URL}/datasets/{test_dataset_id}/assign/{user_id}",
                headers=get_headers(),
                params={"role": "annotator", "force": True}
            )
        
        # 获取任务总数
        response = requests.get(
            f"{BASE_URL}/datasets/{test_dataset_id}",
            headers=get_headers()
        )
        
        if response.status_code != 200:
            print_error("无法获取数据集信息")
            return False
        
        dataset = response.json().get("data", {})
        total_tasks = len(dataset.get("task_list", []))
        
        if total_tasks < 2:
            print_warning(f"任务数太少（{total_tasks}），跳过范围重叠检查")
            return True
        
        # 使用实际的任务数
        end_index = min(10, total_tasks)
        overlap_start = max(1, end_index - 2)
        overlap_end = min(total_tasks, end_index + 5)
        
        # 分配 1-end_index 给用户1
        user1_id = test_user_ids[0]
        print_info(f"分配任务 1-{end_index} 给用户 {user1_id}...")
        
        response = requests.post(
            f"{BASE_URL}/datasets/{test_dataset_id}/assign",
            headers=get_headers(),
            json={
                "user_id": user1_id,
                "role": "annotator",
                "mode": "range",
                "start_index": 1,
                "end_index": end_index
            }
        )
        
        if response.status_code != 200:
            print_error(f"第一次分配失败: {response.text}")
            return False
        
        print_success("第一次分配成功")
        
        # 尝试分配重叠范围给用户2（应该失败）
        if len(test_user_ids) >= 2:
            user2_id = test_user_ids[1]
            print_info(f"尝试分配重叠范围 {overlap_start}-{overlap_end} 给用户 {user2_id}（应该失败）...")
            
            response = requests.post(
                f"{BASE_URL}/datasets/{test_dataset_id}/assign",
                headers=get_headers(),
                json={
                    "user_id": user2_id,
                    "role": "annotator",
                    "mode": "range",
                    "start_index": overlap_start,
                    "end_index": overlap_end
                }
            )
            
            if response.status_code == 400:
                print_success("范围重叠检查生效（正确拒绝了重叠分配）")
                print_info(f"错误信息: {response.json().get('detail')}")
                return True
            else:
                print_error("范围重叠检查失败（应该拒绝但没有拒绝）")
                return False
        
        return True
    
    except Exception as e:
        print_error(f"范围重叠检查异常: {str(e)}")
        return False


def cleanup() -> bool:
    """清理测试数据"""
    print_section("11. 清理测试数据")
    
    try:
        print_info("清理所有测试分配...")
        
        for user_id in test_user_ids:
            response = requests.delete(
                f"{BASE_URL}/datasets/{test_dataset_id}/assign/{user_id}",
                headers=get_headers(),
                params={"role": "annotator", "force": True}
            )
            
            if response.status_code == 200:
                print_success(f"清理用户 {user_id} 的分配")
            elif response.status_code == 400:
                # 可能已经不存在了
                pass
        
        print_success("清理完成")
        return True
    
    except Exception as e:
        print_error(f"清理异常: {str(e)}")
        return False


def main():
    """主函数"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  Task 47: 数据集分配API测试")
    print(f"  测试服务器: {BASE_URL}")
    print(f"{'='*60}{Colors.END}\n")
    
    # 测试结果统计
    results = {}
    
    # 1. 登录
    if not login():
        print_error("登录失败，终止测试")
        return
    results["登录"] = True
    
    # 2. 准备测试数据
    if not prepare_test_data():
        print_error("准备测试数据失败，终止测试")
        return
    results["准备数据"] = True
    
    # 3-11. 执行各项测试
    tests = [
        ("整体分配", test_assign_full),
        ("获取分配情况", test_get_assignments),
        ("取消分配", test_cancel_assignment),
        ("范围分配", test_assign_range),
        ("自动分配", test_auto_assign),
        ("转移分配", test_transfer_assignment),
        ("获取我的数据集", test_get_my_datasets),
        ("范围重叠检查", test_range_overlap),
        ("清理测试数据", cleanup)
    ]
    
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # 打印测试总结
    print_section("测试总结")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"总测试数: {total}")
    print(f"{Colors.GREEN}通过: {passed}{Colors.END}")
    print(f"{Colors.RED}失败: {failed}{Colors.END}")
    print()
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"  {status}  {test_name}")
    
    print()
    
    if failed == 0:
        print_success("🎉 所有测试通过！")
    else:
        print_error(f"⚠️  有 {failed} 个测试失败")


if __name__ == "__main__":
    main()
