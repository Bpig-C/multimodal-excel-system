"""
Excel处理服务
提取WPS Excel内嵌图片、解析表格数据、生成语料记录
"""
import zipfile
import xml.etree.ElementTree as ET
import os
import re
import uuid
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session

from models.db_models import Corpus, Image
from config import settings
from services.storage_service import storage_service


CANONICAL_SECOND_FIELD = '客户/发生工程/供应商'
SECOND_FIELD_ALIASES = [
    '客户/发生工程/供应商',
    '问题来源',
    '供应商',
    '客户',
]


def _normalize_header_name(name: str) -> str:
    """统一列名比较口径：去首尾空白并移除中间空白。"""
    return ''.join(str(name).strip().split())


class ExcelProcessingService:
    """Excel文件处理服务"""
    
    def __init__(self, db: Session):
        self.db = db
        
    def process_excel_file(
        self, 
        xlsx_path: str, 
        source_filename: str
    ) -> Dict:
        """
        处理Excel文件，提取图片和文本数据
        
        Args:
            xlsx_path: Excel文件路径
            source_filename: 原始文件名
            
        Returns:
            处理结果字典，包含语料ID列表、图片数量、统计信息
        """
        # 1. 提取图片
        image_mapping = self.extract_wps_excel_images(xlsx_path, source_filename)

        # 2. 读取Excel数据
        df = pd.read_excel(xlsx_path, engine='openpyxl')
        df.columns = [str(c).strip() for c in df.columns]
        df = self._normalize_failure_case_columns(df)

        # 3. 校验必要列，拒绝格式不符的文件
        REQUIRED_COLUMNS = [
            '问题分类', '质量问题',
            '问题描述', '问题处理', '原因分析', '采取措施',
        ]
        normalized_to_actual = {
            _normalize_header_name(col): col
            for col in df.columns
        }
        missing = [
            col for col in REQUIRED_COLUMNS
            if _normalize_header_name(col) not in normalized_to_actual
        ]
        has_second_field = _normalize_header_name(CANONICAL_SECOND_FIELD) in normalized_to_actual
        if missing or not has_second_field:
            detail = []
            if missing:
                detail.append(f"缺少必要列 {missing}")
            if not has_second_field:
                detail.append(
                    f"缺少字段“{CANONICAL_SECOND_FIELD}”（支持别名：{SECOND_FIELD_ALIASES}）"
                )
            raise ValueError(
                f"文件格式不符：品质失效案例 Excel {'；'.join(detail)}，"
                f"请确认上传了正确的文件。"
            )

        # 4. 转换DISPIMG公式为Markdown格式
        df = self._convert_dispimg_in_dataframe(df)
        
        # 4. 生成语料记录
        corpus_ids = []
        total_sentences = 0
        
        for row_idx, row in df.iterrows():
            # 为每一行的每个字段生成语料
            for col_name, cell_value in row.items():
                if pd.isna(cell_value) or str(cell_value).strip() == '':
                    continue
                    
                text = str(cell_value)
                
                # 分句处理
                sentences = self._split_text_to_sentences(text)
                
                for sentence in sentences:
                    if not sentence.strip():
                        continue
                        
                    # 提取图片引用
                    image_refs = self._extract_image_paths(sentence)
                    
                    # 创建语料记录
                    corpus = self._create_corpus_record(
                        text=sentence,
                        source_file=source_filename,
                        source_row=int(row_idx) + 2,  # Excel行号从1开始，加上表头
                        source_field=col_name,
                        text_type=col_name,
                        image_refs=image_refs,
                        image_mapping=image_mapping
                    )
                    
                    corpus_ids.append(corpus.text_id)
                    total_sentences += 1
        
        return {
            "status": "success",
            "corpus_count": len(corpus_ids),
            "sentence_count": total_sentences,
            "image_count": len(image_mapping),
            "corpus_ids": corpus_ids,
            "source_file": source_filename
        }

    def _normalize_failure_case_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """将品质案例表头中的同义字段统一为标准字段名。"""
        alias_map = {
            _normalize_header_name(alias): alias
            for alias in SECOND_FIELD_ALIASES
        }

        rename_map = {}
        second_field_candidates = []
        for col in df.columns:
            normalized = _normalize_header_name(col)
            if normalized in alias_map:
                second_field_candidates.append(col)
                rename_map[col] = CANONICAL_SECOND_FIELD

        if rename_map:
            df = df.rename(columns=rename_map)

        # 若多个同义列同时存在，按从左到右取第一个非空值进行合并。
        if len(second_field_candidates) > 1 and CANONICAL_SECOND_FIELD in df.columns:
            second_cols = [c for c in df.columns if c == CANONICAL_SECOND_FIELD]
            merged = df[second_cols].bfill(axis=1).iloc[:, 0]
            dedup = df.loc[:, df.columns != CANONICAL_SECOND_FIELD]
            df = pd.concat([dedup, merged.rename(CANONICAL_SECOND_FIELD)], axis=1)

        return df

    def extract_wps_excel_images(
        self, 
        xlsx_path: str, 
        source_filename: str
    ) -> Dict[str, str]:
        """
        从WPS Excel文件中提取内嵌图片
        
        WPS Excel使用特殊的cellimages.xml存储图片信息：
        1. cellimages.xml: 包含图片名称(如ID_XXX)和关系ID(rId)的映射
        2. cellimages.xml.rels: 包含关系ID和实际图片路径的映射
        
        Args:
            xlsx_path: Excel文件路径
            source_filename: 原始文件名（用于组织输出目录）
            
        Returns:
            图片名称到文件路径的映射字典 {image_name: file_path}
        """
        # 创建输出目录
        file_stem = Path(source_filename).stem
        out_dir = settings.IMAGE_DIR / file_stem
        out_dir.mkdir(parents=True, exist_ok=True)
        
        image_mapping = {}
        
        try:
            with zipfile.ZipFile(xlsx_path) as z:
                # 检查cellimages.xml是否存在
                if 'xl/cellimages.xml' not in z.namelist():
                    print(f"警告: {xlsx_path} 中没有找到cellimages.xml，可能没有内嵌图片")
                    return image_mapping
                
                # 1. 解析 cellimages.xml 得到 <name, rId>
                root = ET.fromstring(z.read('xl/cellimages.xml'))
                ns = {
                    'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
                    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
                }
                
                name2rid = {}
                for pic in root.findall('.//xdr:pic', ns):
                    cNvPr = pic.find('.//xdr:cNvPr', ns)
                    blip = pic.find('.//a:blip', ns)
                    if cNvPr is not None and blip is not None:
                        name = cNvPr.get('name')
                        rid = blip.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if name and rid:
                            name2rid[name] = rid

                # 2. 解析 .rels 得到 <rId, 真实路径>
                rel_root = ET.fromstring(z.read('xl/_rels/cellimages.xml.rels'))
                rid2path = {c.get('Id'): c.get('Target') for c in rel_root}

                # 3. 合并映射并导出图片
                for name, rid in name2rid.items():
                    if rid not in rid2path:
                        continue
                    img_path = 'xl/' + rid2path[rid]
                    ext = os.path.splitext(img_path)[1] or '.png'
                    
                    # 读取图片数据
                    try:
                        img_data = z.read(img_path)
                        
                        # 使用存储服务保存图片（支持本地/MinIO）
                        relative_path = f"{file_stem}/{name}{ext}"
                        storage_service.save_image(
                            file_data=img_data,
                            relative_path=relative_path,
                            content_type=f'image/{ext[1:]}'  # 去掉点号
                        )
                        
                        image_mapping[name] = relative_path
                        
                    except Exception as e:
                        print(f"提取图片失败 {name}: {e}")
                        
        except zipfile.BadZipFile:
            print(f"错误: {xlsx_path} 不是有效的zip/xlsx文件")
        except KeyError as e:
            print(f"警告: 缺少必要的文件 {e}")
        except Exception as e:
            print(f"提取图片时出错: {e}")
        
        return image_mapping
    
    def _convert_dispimg_in_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        将DataFrame中的DISPIMG公式转换为Markdown图片格式
        
        WPS Excel中的图片显示为公式: =DISPIMG("ID_XXX",数字)
        转换为Markdown格式: ![图片](ID_XXX)
        
        Args:
            df: 原始DataFrame
            
        Returns:
            转换后的DataFrame
        """
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: self._convert_dispimg_to_markdown(str(x)) if pd.notna(x) else x
            )
        return df
    
    def _convert_dispimg_to_markdown(self, text: str) -> str:
        """
        将WPS图片函数转换为Markdown图片格式
        
        Args:
            text: 包含DISPIMG公式的文本
            
        Returns:
            转换后的文本
        """
        # 匹配 =DISPIMG("ID_XXX",数字) 并替换成 ![图片](ID_XXX)
        pattern = r'=DISPIMG\("([A-Za-z0-9_]+)",\d+\)'
        result = re.sub(pattern, r'![图片](\1)', text, flags=re.I)
        return result
    
    def _extract_image_paths(self, text: str) -> List[str]:
        """
        从文本中提取Markdown格式的图片引用
        
        匹配格式: ![图片](ID_XXX)
        
        Args:
            text: 包含Markdown图片引用的文本
            
        Returns:
            图片名称列表，如 ['ID_XXX', ...]
        """
        pattern = r'!\[图片\]\(([A-Za-z0-9_]+)\)'
        return re.findall(pattern, text)

    def _split_text_to_sentences(self, text: str) -> List[str]:
        """
        将单元格文本作为一个完整句子进行清洗

        处理规则：
        1. 删除换行符影响（按空白统一处理）
        2. 清理多余空格（保留单个空格，删除首尾空格和连续空格）
        3. 不再按标点或序号进一步分句
        
        Args:
            text: 原始文本
            
        Returns:
            句子列表
        """
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        if not cleaned_text:
            return []
        return [cleaned_text]
    
    def _create_corpus_record(
        self,
        text: str,
        source_file: str,
        source_row: int,
        source_field: str,
        text_type: str,
        image_refs: List[str],
        image_mapping: Dict[str, str]
    ) -> Corpus:
        """
        创建语料记录并关联图片
        
        Args:
            text: 文本内容
            source_file: 源文件名
            source_row: 源文件行号
            source_field: 源字段名
            text_type: 文本类型（字段分类）
            image_refs: 图片引用列表
            image_mapping: 图片名称到路径的映射
            
        Returns:
            创建的Corpus对象
        """
        # 生成唯一ID
        text_id = f"corpus_{uuid.uuid4().hex[:16]}"
        
        # 创建语料记录
        corpus = Corpus(
            text_id=text_id,
            text=text,
            text_type=text_type,
            source_file=source_file,
            source_row=source_row,
            source_field=source_field,
            has_images=len(image_refs) > 0
        )
        
        self.db.add(corpus)
        self.db.flush()  # 获取corpus.id
        
        # 创建关联的图片记录
        for img_name in image_refs:
            if img_name in image_mapping:
                image_id = f"img_{uuid.uuid4().hex[:16]}"
                
                # 获取图片文件路径
                file_path = image_mapping[img_name]
                full_path = settings.IMAGE_DIR / file_path
                
                # 获取图片尺寸（可选）
                width, height = self._get_image_dimensions(full_path)
                
                image = Image(
                    image_id=image_id,
                    corpus_id=corpus.id,
                    file_path=file_path,
                    original_name=img_name,
                    width=width,
                    height=height
                )
                
                self.db.add(image)
        
        self.db.commit()
        return corpus
    
    def _get_image_dimensions(self, image_path: Path) -> Tuple[Optional[int], Optional[int]]:
        """
        获取图片尺寸
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            (width, height) 元组，如果无法获取则返回 (None, None)
        """
        try:
            from PIL import Image as PILImage
            with PILImage.open(image_path) as img:
                return img.size
        except Exception as e:
            print(f"无法获取图片尺寸 {image_path}: {e}")
            return None, None
    
    def validate_excel_file(self, xlsx_path: str, required_columns: List[str] = None) -> Dict:
        """
        验证Excel文件格式
        
        Args:
            xlsx_path: Excel文件路径
            required_columns: 必需的列名列表（可选）
            
        Returns:
            验证结果字典
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(xlsx_path):
                return {
                    "valid": False,
                    "error": "文件不存在"
                }
            
            # 检查文件扩展名
            if not xlsx_path.lower().endswith(('.xlsx', '.xls')):
                return {
                    "valid": False,
                    "error": "文件格式不正确，仅支持.xlsx和.xls格式"
                }
            
            # 尝试读取Excel文件
            df = pd.read_excel(xlsx_path, engine='openpyxl')
            
            # 检查是否为空
            if df.empty:
                return {
                    "valid": False,
                    "error": "Excel文件为空"
                }
            
            # 检查必需列
            if required_columns:
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    return {
                        "valid": False,
                        "error": f"缺少必需的列: {', '.join(missing_columns)}"
                    }
            
            return {
                "valid": True,
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns)
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"验证失败: {str(e)}"
            }
