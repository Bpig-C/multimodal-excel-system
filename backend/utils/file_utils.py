"""文件名规范化工具"""
import re
import os


def sanitize_filename(filename: str) -> str:
    """
    规范化文件名，保留中文、英文、数字，其他字符替换为下划线
    """
    name, ext = os.path.splitext(filename)
    sanitized = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', name)
    return sanitized + ext


def rename_all_files(root_path: str):
    """遍历目录下所有文件并规范化文件名"""
    for root, dirs, files in os.walk(root_path):
        for file in files:
            old_path = os.path.join(root, file)
            new_name = sanitize_filename(file)
            new_path = os.path.join(root, new_name)
            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"重命名: {file} -> {new_name}")
                except Exception as e:
                    print(f"重命名失败: {file}, 错误: {e}")
