"""
提取测试失败的详细信息
"""
import subprocess
import sys
import re

def extract_failures():
    """运行测试并提取失败信息"""
    print("运行测试并提取失败信息...")
    print("=" * 80)
    
    # 运行pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--tb=short", "-x"],  # -x: 遇到第一个失败就停止
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    lines = result.stdout.split('\n')
    
    # 查找失败的测试
    failures = []
    current_failure = None
    in_failure = False
    
    for i, line in enumerate(lines):
        # 检测失败的测试
        if 'FAILED' in line and '::' in line:
            if current_failure:
                failures.append(current_failure)
            current_failure = {
                'test': line.strip(),
                'details': []
            }
            in_failure = True
        elif in_failure:
            # 收集失败详情
            if line.startswith('=') or line.startswith('_'):
                in_failure = False
                if current_failure:
                    failures.append(current_failure)
                    current_failure = None
            else:
                if current_failure and line.strip():
                    current_failure['details'].append(line)
    
    # 显示失败信息
    if failures:
        print(f"\n发现 {len(failures)} 个失败的测试:\n")
        for i, failure in enumerate(failures, 1):
            print(f"\n{i}. {failure['test']}")
            print("-" * 80)
            for detail in failure['details'][:20]:  # 只显示前20行
                print(detail)
            if len(failure['details']) > 20:
                print(f"... (还有 {len(failure['details']) - 20} 行)")
    else:
        print("\n✓ 所有测试都通过了!")
    
    # 显示汇总
    print("\n" + "=" * 80)
    for line in lines[-10:]:
        if line.strip():
            print(line)

if __name__ == "__main__":
    extract_failures()
