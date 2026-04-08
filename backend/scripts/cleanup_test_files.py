"""
清理测试生成的临时文件
"""
import os
from pathlib import Path

def cleanup():
    """清理测试文件"""
    backend_dir = Path(__file__).parent.parent
    
    # 要清理的文件模式
    patterns = [
        "test_*.db",
        "*.db-journal",
        "test_report_*.txt",
    ]
    
    cleaned = []
    
    for pattern in patterns:
        for file in backend_dir.glob(pattern):
            try:
                file.unlink()
                cleaned.append(file.name)
                print(f"✓ 删除: {file.name}")
            except Exception as e:
                print(f"✗ 无法删除 {file.name}: {e}")
    
    # 清理 __pycache__
    for pycache in backend_dir.rglob("__pycache__"):
        try:
            import shutil
            shutil.rmtree(pycache)
            print(f"✓ 删除: {pycache.relative_to(backend_dir)}")
        except Exception as e:
            print(f"✗ 无法删除 {pycache}: {e}")
    
    print(f"\n清理完成，共删除 {len(cleaned)} 个文件")

if __name__ == "__main__":
    cleanup()
