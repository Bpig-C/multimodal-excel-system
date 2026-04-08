"""
验证测试结构是否正确
检查测试文件组织和pytest配置
"""
import os
from pathlib import Path

def check_test_structure():
    """检查测试目录结构"""
    print("=" * 60)
    print("验证测试目录结构")
    print("=" * 60)
    
    tests_dir = Path("tests")
    
    # 检查主要测试目录
    required_dirs = ["unit", "api", "agents", "integration", "manual", "test_artifacts"]
    
    print("\n1. 检查测试目录:")
    for dir_name in required_dirs:
        dir_path = tests_dir / dir_name
        exists = dir_path.exists()
        status = "✓" if exists else "✗"
        print(f"   {status} tests/{dir_name}/")
    
    # 检查manual目录中的文件
    print("\n2. 检查手动测试脚本:")
    manual_dir = tests_dir / "manual"
    if manual_dir.exists():
        manual_scripts = list(manual_dir.glob("test_*.py"))
        print(f"   找到 {len(manual_scripts)} 个手动测试脚本:")
        for script in manual_scripts:
            print(f"   ✓ {script.name}")
        
        # 检查README
        readme = manual_dir / "README.md"
        if readme.exists():
            print(f"   ✓ README.md")
        else:
            print(f"   ✗ README.md (缺失)")
    else:
        print("   ✗ manual目录不存在")
    
    # 检查pytest配置
    print("\n3. 检查pytest配置:")
    pytest_ini = Path("pytest.ini")
    if pytest_ini.exists():
        print("   ✓ pytest.ini 存在")
        
        # 读取配置检查norecursedirs
        content = pytest_ini.read_text(encoding='utf-8')
        if "norecursedirs" in content and "manual" in content:
            print("   ✓ pytest.ini 配置了忽略manual目录")
        else:
            print("   ⚠ pytest.ini 未配置忽略manual目录")
    else:
        print("   ✗ pytest.ini 不存在")
    
    # 检查根目录是否还有测试文件
    print("\n4. 检查backend根目录:")
    root_test_files = list(Path(".").glob("test_*.py"))
    if root_test_files:
        print(f"   ⚠ 发现 {len(root_test_files)} 个测试文件在根目录:")
        for f in root_test_files:
            print(f"     - {f.name}")
    else:
        print("   ✓ 根目录没有测试文件")
    
    print("\n" + "=" * 60)
    print("验证完成")
    print("=" * 60)

if __name__ == "__main__":
    check_test_structure()
