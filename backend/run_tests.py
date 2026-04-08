"""
主测试运行脚本
运行所有后端测试并显示汇总结果
"""
import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path

def run_tests(save_report=False, verbose=True):
    """
    运行所有测试
    
    Args:
        save_report: 是否保存测试报告到文件
        verbose: 是否显示详细输出
    """
    print("=" * 80)
    print("运行后端测试套件")
    print("=" * 80)
    print()
    
    # 构建pytest命令
    cmd = [sys.executable, "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    cmd.append("--tb=short")
    
    if save_report:
        # 使用实时输出并保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = Path("tests/test_artifacts/reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"test_report_{timestamp}.txt"
        
        print(f"测试输出将保存到: {report_file}")
        print()
        
        # 运行测试并捕获输出
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时显示并收集输出
        output_lines = []
        for line in process.stdout:
            print(line, end='')  # 实时显示
            output_lines.append(line)  # 收集用于保存
        
        process.wait()
        
        # 保存报告到文件
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"测试报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.writelines(output_lines)
        
        print()
        print("=" * 80)
        print(f"✓ 测试报告已保存: {report_file}")
        print("=" * 80)
        
        return process.returncode
    else:
        # 直接运行，实时输出到终端
        result = subprocess.run(cmd, cwd=".")
        return result.returncode

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='运行后端测试套件')
    parser.add_argument(
        '--save', '-s',
        action='store_true',
        help='保存测试报告到文件'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='简洁模式，减少输出'
    )
    
    args = parser.parse_args()
    
    exit_code = run_tests(
        save_report=args.save,
        verbose=not args.quiet
    )
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
