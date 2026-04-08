"""KF Excel 工具函数 - 图片提取、列名映射等"""
import zipfile
import xml.etree.ElementTree as ET
import os
import re
import json
import pandas as pd


def detect_excel_type(xlsx_path):
    """
    检测Excel文件类型（WPS或Microsoft）

    Returns:
        'wps': WPS Excel格式
        'microsoft': Microsoft Excel格式
        'unknown': 无法确定或没有图片
    """
    try:
        with zipfile.ZipFile(xlsx_path, 'r') as z:
            file_list = z.namelist()
            if 'xl/cellimages.xml' in file_list:
                return 'wps'
            if any(f.startswith('xl/drawings/drawing') and f.endswith('.xml') for f in file_list):
                return 'microsoft'
            return 'unknown'
    except Exception as e:
        print(f"检测Excel类型失败: {e}")
        return 'unknown'


def extract_wps_excel_images(xlsx_path, out_dir='images'):
    """从WPS Excel中提取图片"""
    os.makedirs(out_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(xlsx_path) as z:
            if 'xl/cellimages.xml' not in z.namelist():
                print(f"Excel文件中没有图片（cellimages.xml不存在），跳过图片提取")
                return 0

            root = ET.fromstring(z.read('xl/cellimages.xml'))
            ns = {'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
                  'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            name2rid = {p.find('.//xdr:cNvPr', ns).get('name'):
                        p.find('.//a:blip', ns).attrib[
                            '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed']
                        for p in root.findall('.//xdr:pic', ns)}

            rel_root = ET.fromstring(z.read('xl/_rels/cellimages.xml.rels'))
            rid2path = {c.get('Id'): c.get('Target') for c in rel_root}

            image_count = 0
            for name, rid in name2rid.items():
                if rid not in rid2path:
                    continue
                img_path = 'xl/' + rid2path[rid]
                ext = os.path.splitext(img_path)[1] or '.png'
                open(os.path.join(out_dir, name + ext), 'wb').write(z.read(img_path))
                image_count += 1

            return image_count
    except KeyError as e:
        print(f"提取图片时出错（可能是标准Excel格式）: {e}")
        return 0
    except Exception as e:
        print(f"提取图片时出错: {e}")
        return 0


def extract_microsoft_excel_images(xlsx_path, out_dir='images'):
    """从Microsoft Excel格式中提取图片，并使用UUID重命名"""
    import uuid

    os.makedirs(out_dir, exist_ok=True)
    image_mapping = {}

    try:
        with zipfile.ZipFile(xlsx_path, 'r') as z:
            file_list = z.namelist()

            drawing_files = [f for f in file_list
                             if f.startswith('xl/drawings/drawing') and f.endswith('.xml')
                             and '_rels' not in f]

            if not drawing_files:
                print(f"Microsoft Excel文件中没有找到drawing文件")
                return image_mapping

            for drawing_file in drawing_files:
                try:
                    drawing_xml = z.read(drawing_file)
                    drawing_root = ET.fromstring(drawing_xml)

                    rel_file = drawing_file.replace('xl/drawings/', 'xl/drawings/_rels/') + '.rels'
                    if rel_file not in file_list:
                        continue

                    rel_xml = z.read(rel_file)
                    rel_root = ET.fromstring(rel_xml)

                    ns_rel = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}

                    for rel in rel_root.findall('.//rel:Relationship', ns_rel):
                        rel_type = rel.get('Type', '')
                        target = rel.get('Target', '')

                        if 'image' in rel_type.lower() and target:
                            if target.startswith('../media/'):
                                image_path = 'xl/media/' + target.split('/')[-1]
                            elif target.startswith('media/'):
                                image_path = 'xl/' + target
                            else:
                                image_path = 'xl/drawings/' + target

                            if image_path in file_list:
                                image_data = z.read(image_path)
                                original_name = os.path.basename(image_path)

                                file_ext = os.path.splitext(original_name)[1]
                                uuid_name = f"ID_{uuid.uuid4().hex.upper()}{file_ext}"

                                output_path = os.path.join(out_dir, uuid_name)
                                with open(output_path, 'wb') as f:
                                    f.write(image_data)

                                image_mapping[original_name] = uuid_name
                                print(f"提取图片: {original_name} -> {uuid_name}")

                except Exception as e:
                    print(f"处理drawing文件 {drawing_file} 时出错: {e}")
                    continue

            return image_mapping

    except Exception as e:
        print(f"提取Microsoft Excel图片失败: {e}")
        return image_mapping


def extract_excel_images(xlsx_path, out_dir='images'):
    """统一的Excel图片提取接口，自动检测类型"""
    excel_type = detect_excel_type(xlsx_path)
    print(f"检测到Excel类型: {excel_type}")

    if excel_type == 'wps':
        return extract_wps_excel_images(xlsx_path, out_dir)
    elif excel_type == 'microsoft':
        return extract_microsoft_excel_images(xlsx_path, out_dir)
    else:
        print(f"未检测到图片或未知Excel类型，跳过图片提取")
        return 0


def table_str_wps_image_name_2_markdown_img_name(table_str: str, image_files_map: dict = None):
    """将WPS Excel的DISPIMG格式转换为Markdown格式"""
    # 先处理带扩展名的格式
    out = re.sub(
        r'=DISPIMG\("([A-Za-z0-9_]+\.(png|jpeg|jpg))",\d+\)',
        r'![图片](imgs/\1)',
        table_str,
        flags=re.I
    )

    # 再处理不带扩展名的格式
    if image_files_map:
        def replace_with_map(match):
            uuid = match.group(1)
            if uuid in image_files_map:
                full_name = image_files_map[uuid]
                return f'![图片](imgs/{full_name})'
            else:
                return f'![图片](imgs/{uuid}.png)'

        out = re.sub(
            r'=DISPIMG\("([A-Za-z0-9_]+)",\d+\)',
            replace_with_map,
            out,
            flags=re.I
        )
    else:
        out = re.sub(
            r'=DISPIMG\("([A-Za-z0-9_]+)",\d+\)',
            r'![图片](imgs/\1.png)',
            out,
            flags=re.I
        )

    return out


def extract_image_paths(text):
    """从文本中提取图片路径"""
    pattern = r'!\[图片\]\((imgs/[A-Za-z0-9_]+\.(png|jpeg|jpg))\)'
    matches = re.findall(pattern, text, flags=re.I)
    return [match[0] for match in matches]


def update_column_names(json_file_path, column_mappings=None):
    """
    更新JSON文件中的列名

    Args:
        json_file_path: JSON文件路径
        column_mappings: 列名映射字典，如果为None则使用KF默认映射
    """
    if column_mappings is None:
        from .config import COLUMN_MAPPINGS
        column_mappings = COLUMN_MAPPINGS

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    table_data = data['table_data']

    for item in table_data:
        keys_to_modify = list(item.keys())
        for key in keys_to_modify:
            if key in column_mappings:
                item[column_mappings[key]] = item.pop(key)

    data['table_data'] = table_data
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"列名已成功更新，数据未丢失!")
