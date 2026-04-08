"""
语料分组API - 按Excel行分组显示
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict
from collections import defaultdict

from database import get_db
from models.db_models import Corpus, Image
from models.schemas import ImageInfo
from pydantic import BaseModel


# 定义分组语料模型
class GroupedCorpusItem(BaseModel):
    """单个语料项"""
    text_id: str
    text: str
    text_type: str
    source_field: str
    has_images: bool
    images: List[ImageInfo] = []


class GroupedCorpusRow(BaseModel):
    """按行分组的语料"""
    source_file: str
    source_row: int
    items: List[GroupedCorpusItem]
    total_images: int
    created_at: str


class GroupedCorpusListResponse(BaseModel):
    """分组语料列表响应"""
    total: int
    items: List[GroupedCorpusRow]


router = APIRouter(prefix="/api/v1", tags=["corpus"])


@router.get("/corpus/grouped", response_model=GroupedCorpusListResponse)
async def get_grouped_corpus_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    source_file: Optional[str] = Query(None, description="按文件名筛选"),
    source_field: Optional[str] = Query(None, description="按字段分类筛选"),
    has_images: Optional[bool] = Query(None, description="是否包含图片"),
    db: Session = Depends(get_db)
):
    """
    获取按Excel行分组的语料列表
    
    - 同一行的多个字段内容会合并显示
    - 支持分页（按行分页）
    - 支持筛选
    """
    # 构建查询
    query = db.query(Corpus)
    
    # 应用筛选条件
    if source_file:
        query = query.filter(Corpus.source_file.like(f"%{source_file}%"))
    if source_field:
        query = query.filter(Corpus.source_field == source_field)
    if has_images is not None:
        query = query.filter(Corpus.has_images == has_images)
    
    # 获取所有语料（先不分页，因为需要按行分组）
    all_corpus = query.order_by(
        Corpus.source_file,
        Corpus.source_row,
        Corpus.created_at
    ).all()
    
    # 按 (source_file, source_row) 分组
    grouped_data = defaultdict(list)
    for corpus in all_corpus:
        key = (corpus.source_file, corpus.source_row)
        grouped_data[key].append(corpus)
    
    # 转换为列表并排序
    grouped_rows = []
    for (source_file, source_row), corpus_list in grouped_data.items():
        # 获取该行的所有图片
        total_images = 0
        items = []
        
        for corpus in corpus_list:
            # 获取关联的图片
            images = db.query(Image).filter(Image.corpus_id == corpus.id).all()
            image_infos = [
                ImageInfo(
                    image_id=img.image_id,
                    file_path=img.file_path,
                    original_name=img.original_name,
                    width=img.width,
                    height=img.height
                )
                for img in images
            ]
            
            total_images += len(images)
            
            items.append(GroupedCorpusItem(
                text_id=corpus.text_id,
                text=corpus.text,
                text_type=corpus.text_type or "",
                source_field=corpus.source_field or "",
                has_images=corpus.has_images,
                images=image_infos
            ))
        
        grouped_rows.append(GroupedCorpusRow(
            source_file=source_file,
            source_row=source_row,
            items=items,
            total_images=total_images,
            created_at=corpus_list[0].created_at.isoformat()
        ))
    
    # 按文件名和行号排序
    grouped_rows.sort(key=lambda x: (x.source_file, x.source_row))
    
    # 分页
    total = len(grouped_rows)
    offset = (page - 1) * page_size
    paginated_rows = grouped_rows[offset:offset + page_size]
    
    return GroupedCorpusListResponse(
        total=total,
        items=paginated_rows
    )
