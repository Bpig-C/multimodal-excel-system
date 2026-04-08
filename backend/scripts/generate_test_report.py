"""
生成测试报告到文件
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def generate_report():
    """生成测试报告"""
    print("正在运行测试...")
    
    # 运行pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--tb=short"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    # 生成报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.txt"
    
    # 写入报告
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"测试报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(result.stdout)
        if result.stderr:
            f.write("\n\n错误输出:\n")
            f.write(result.stderr)
    
    print(f"\n✓ 测试报告已生成: {report_file}")
    
    # 提取并显示汇总
    lines = result.stdout.split('\n')
    print("\n测试汇总:")
    print("-" * 80)
    for line in lines[-15:]:
        if line.strip():
            print(line)
    
    return report_file

if __name__ == "__main__":
    report_file = generate_report()
    print(f"\n查看完整报告: {report_file}")
