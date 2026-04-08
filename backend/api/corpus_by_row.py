"""
获取同行语料API - 用于标注任务详情中显示上下文
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.db_models import Corpus, Image
from models.schemas import CorpusResponse, ImageInfo
from pydantic import BaseModel


router = APIRouter(prefix="/api/v1", tags=["corpus"])


@router.get("/corpus/by-row", response_model=List[CorpusResponse])
async def get_corpus_by_row(
    source_file: str = Query(..., description="源文件名"),
    source_row: int = Query(..., description="行号"),
    db: Session = Depends(get_db)
):
    """
    获取指定Excel行的所有语料记录
    用于在标注任务详情中显示上下文（同行的其他字段）
    
    Args:
        source_file: 源文件名
        source_row: 行号
        db: 数据库会话
    
    Returns:
        该行的所有语料记录列表
    """
    # 查询该行的所有语料
    corpus_list = db.query(Corpus).filter(
        Corpus.source_file == source_file,
        Corpus.source_row == source_row
    ).order_by(Corpus.created_at).all()
    
    # 构建响应
    result = []
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
        
        result.append(CorpusResponse(
            text_id=corpus.text_id,
            text=corpus.text,
            text_type=corpus.text_type or "",
            source_file=corpus.source_file,
            source_row=corpus.source_row,
            source_field=corpus.source_field or "",
            has_images=corpus.has_images,
            images=image_infos,
            created_at=corpus.created_at.isoformat()
        ))
    
    return result
