"""QMS Excel 解析器 - 使用 pandas 直读"""
import os
import re
import json
from pathlib import Path
import pandas as pd


# QMS Excel 必须包含的列
REQUIRED_COLUMNS = [
    '制令单号', '录入时间', '客户名称', '型号', '条码', '位号',
    '车间', '产线', '岗位', '不良项目', '质检节点', '状态', '照片',
]


def _extract_filename_from_url(url_text: str) -> str:
    """从 URL 中提取文件名（name= 参数或路径最后一段）"""
    if not url_text or not isinstance(url_text, str):
        return ''
    # 尝试提取 name= 参数
    match = re.search(r'[?&]name=([^&]+)', url_text)
    if match:
        return match.group(1)
    # 尝试提取 URL 最后路径段
    match = re.search(r'/([^/?]+)\??', url_text)
    if match:
        return match.group(1)
    return ''


def _find_image_file(filename: str, image_dirs: list) -> str:
    """在候选目录中查找匹配的图片文件，返回相对路径或空"""
    if not filename:
        return ''
    for img_dir in image_dirs:
        candidate = Path(img_dir) / filename
        if candidate.exists():
            return f"imgs/{filename}"
    return ''


def process_qms_excel(file_path: str, output_dir: str = None) -> dict:
    """
    处理 QMS Excel 文件，输出标准 JSON 格式。

    输出格式与 KF parser 一致：
    {
        "table_count": 1,
        "output_directory": str,
        "status": "success"
    }
    同时将每行数据保存为 page_0.json，键名保持原始中文列名。
    """
    src_file = Path(file_path)
    filename = src_file.stem

    if output_dir is None:
        out_root_dir = './Datas/tree_from_excel/' + filename
    else:
        out_root_dir = output_dir

    os.makedirs(out_root_dir, exist_ok=True)
    out_img_dir = os.path.join(out_root_dir, 'imgs')

    # 先只读表头做列名校验，避免大文件全量读取后才报错
    try:
        df_header = pd.read_excel(file_path, dtype=str, nrows=0)
    except Exception as e:
        raise ValueError(f"无法读取 QMS Excel 文件: {e}")

    missing = [col for col in REQUIRED_COLUMNS if col not in df_header.columns]
    if missing:
        raise ValueError(f"QMS Excel 缺少必要列: {missing}")

    # 校验通过后读取全量数据
    try:
        df = pd.read_excel(file_path, dtype=str)
    except Exception as e:
        raise ValueError(f"无法读取 QMS Excel 文件: {e}")

    # 处理每行数据
    records = []
    for _, row in df.iterrows():
        record = {}
        for col in df.columns:
            val = row[col]
            # 将 NaN/nan 转为空字符串
            if pd.isna(val) or str(val).lower() == 'nan':
                record[col] = ''
            else:
                record[col] = str(val).strip()

        # 处理照片字段：从 URL 提取文件名，尝试匹配本地图片
        photo_url = record.get('照片', '')
        if photo_url:
            img_filename = _extract_filename_from_url(photo_url)
            if img_filename:
                local_path = _find_image_file(img_filename, [out_img_dir])
                if local_path:
                    record['照片'] = f"![{img_filename}]({local_path})"
                else:
                    # 保留文件名引用（图片尚未下载）
                    record['照片'] = f"![{img_filename}](imgs/{img_filename})"
            # 若无法提取文件名，保持 URL 原文

        records.append(record)

    # 保存为 JSON
    json_path = os.path.join(out_root_dir, 'page_0.json')
    result_data = {
        'file_name': filename,
        'table_data': records
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)

    return {
        "table_count": 1,
        "output_directory": out_root_dir,
        "image_directory": out_img_dir,
        "status": "success"
    }
