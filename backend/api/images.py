"""
图片标注API
提供图片实体的CRUD操作,支持整图标注和区域标注(边界框)
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from database import get_db
from models.db_models import Image, ImageEntity, AnnotationTask

router = APIRouter(prefix="/api/v1/images", tags=["images"])


# ============================================================================
# 图片实体管理API
# ============================================================================

@router.post("/{image_id}/entities")
async def add_image_entity(
    image_id: str,
    task_id: str = Body(..., description="标注任务ID"),
    label: str = Body(..., description="实体标签"),
    bbox_x: Optional[int] = Body(None, description="边界框X坐标"),
    bbox_y: Optional[int] = Body(None, description="边界框Y坐标"),
    bbox_width: Optional[int] = Body(None, description="边界框宽度"),
    bbox_height: Optional[int] = Body(None, description="边界框高度"),
    confidence: Optional[float] = Body(None, description="置信度"),
    db: Session = Depends(get_db)
):
    """
    添加图片实体
    
    支持两种标注模式:
    1. 整图标注: 不提供边界框参数
    2. 区域标注: 提供完整的边界框参数(x, y, width, height)
    """
    try:
        # 查询图片
        image = db.query(Image).filter(Image.image_id == image_id).first()
        
        if not image:
            raise HTTPException(status_code=404, detail="图片不存在")
        
        # 查询任务
        task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="标注任务不存在")
        
        # 验证边界框参数
        has_bbox = any([bbox_x is not None, bbox_y is not None, 
                       bbox_width is not None, bbox_height is not None])
        
        if has_bbox:
            # 如果提供了任何边界框参数,则必须全部提供
            if not all([bbox_x is not None, bbox_y is not None, 
                       bbox_width is not None, bbox_height is not None]):
                raise HTTPException(
                    status_code=400, 
                    detail="区域标注必须提供完整的边界框参数(x, y, width, height)"
                )
            
            # 验证边界框在图片范围内
            if image.width and image.height:
                if (bbox_x < 0 or bbox_y < 0 or 
                    bbox_x + bbox_width > image.width or 
                    bbox_y + bbox_height > image.height):
                    raise HTTPException(
                        status_code=400,
                        detail=f"边界框超出图片范围(图片尺寸: {image.width}x{image.height})"
                    )
        
        # 生成实体ID
        entity_id_str = f"img-entity-{uuid.uuid4().hex[:8]}"
        
        # 创建图片实体
        image_entity = ImageEntity(
            entity_id=entity_id_str,
            task_id=task.id,
            image_id=image.id,
            label=label,
            bbox_x=bbox_x,
            bbox_y=bbox_y,
            bbox_width=bbox_width,
            bbox_height=bbox_height,
            confidence=confidence,
            version=task.current_version
        )
        
        db.add(image_entity)
        
        # 更新任务为手动标注
        if task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        db.refresh(image_entity)
        
        return {
            "success": True,
            "message": "图片实体添加成功",
            "data": {
                "id": image_entity.id,
                "entity_id": image_entity.entity_id,
                "image_id": image_id,
                "label": image_entity.label,
                "annotation_type": "region" if has_bbox else "whole_image",
                "bbox": {
                    "x": image_entity.bbox_x,
                    "y": image_entity.bbox_y,
                    "width": image_entity.bbox_width,
                    "height": image_entity.bbox_height
                } if has_bbox else None,
                "confidence": image_entity.confidence
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加图片实体失败: {str(e)}")


@router.get("/{image_id}/entities")
async def get_image_entities(
    image_id: str,
    task_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取图片实体列表
    
    可选参数:
    - task_id: 筛选特定任务的图片实体
    """
    try:
        # 查询图片
        image = db.query(Image).filter(Image.image_id == image_id).first()
        
        if not image:
            raise HTTPException(status_code=404, detail="图片不存在")
        
        # 构建查询
        query = db.query(ImageEntity).filter(ImageEntity.image_id == image.id)
        
        # 如果指定了任务ID,则筛选
        if task_id:
            task = db.query(AnnotationTask).filter(AnnotationTask.task_id == task_id).first()
            if not task:
                raise HTTPException(status_code=404, detail="标注任务不存在")
            query = query.filter(ImageEntity.task_id == task.id)
        
        # 执行查询
        entities = query.all()
        
        # 格式化返回数据
        result = []
        for entity in entities:
            has_bbox = entity.bbox_x is not None
            result.append({
                "id": entity.id,
                "entity_id": entity.entity_id,
                "task_id": entity.task.task_id if entity.task else None,
                "label": entity.label,
                "annotation_type": "region" if has_bbox else "whole_image",
                "bbox": {
                    "x": entity.bbox_x,
                    "y": entity.bbox_y,
                    "width": entity.bbox_width,
                    "height": entity.bbox_height
                } if has_bbox else None,
                "confidence": entity.confidence,
                "version": entity.version,
                "created_at": entity.created_at.isoformat()
            })
        
        return {
            "success": True,
            "message": "获取图片实体列表成功",
            "data": {
                "image_id": image_id,
                "image_info": {
                    "file_path": image.file_path,
                    "width": image.width,
                    "height": image.height
                },
                "total": len(result),
                "entities": result
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取图片实体列表失败: {str(e)}")


@router.put("/{image_id}/entities/{entity_id}")
async def update_image_entity(
    image_id: str,
    entity_id: int,
    label: Optional[str] = Body(None, description="实体标签"),
    bbox_x: Optional[int] = Body(None, description="边界框X坐标"),
    bbox_y: Optional[int] = Body(None, description="边界框Y坐标"),
    bbox_width: Optional[int] = Body(None, description="边界框宽度"),
    bbox_height: Optional[int] = Body(None, description="边界框高度"),
    confidence: Optional[float] = Body(None, description="置信度"),
    db: Session = Depends(get_db)
):
    """
    更新图片实体
    
    注意:
    - 如果要更新边界框,必须提供完整的边界框参数
    - 可以通过将所有边界框参数设为null来转换为整图标注
    """
    try:
        # 查询图片
        image = db.query(Image).filter(Image.image_id == image_id).first()
        
        if not image:
            raise HTTPException(status_code=404, detail="图片不存在")
        
        # 查询实体
        entity = db.query(ImageEntity)\
            .filter(ImageEntity.id == entity_id)\
            .filter(ImageEntity.image_id == image.id)\
            .first()
        
        if not entity:
            raise HTTPException(status_code=404, detail="图片实体不存在")
        
        # 更新标签
        if label is not None:
            entity.label = label
        
        # 更新置信度
        if confidence is not None:
            entity.confidence = confidence
        
        # 更新边界框
        bbox_params = [bbox_x, bbox_y, bbox_width, bbox_height]
        bbox_provided = [p is not None for p in bbox_params]
        
        if any(bbox_provided):
            # 如果提供了任何边界框参数,则必须全部提供
            if not all(bbox_provided):
                raise HTTPException(
                    status_code=400,
                    detail="更新边界框必须提供完整的参数(x, y, width, height)"
                )
            
            # 验证边界框在图片范围内
            if image.width and image.height:
                if (bbox_x < 0 or bbox_y < 0 or 
                    bbox_x + bbox_width > image.width or 
                    bbox_y + bbox_height > image.height):
                    raise HTTPException(
                        status_code=400,
                        detail=f"边界框超出图片范围(图片尺寸: {image.width}x{image.height})"
                    )
            
            entity.bbox_x = bbox_x
            entity.bbox_y = bbox_y
            entity.bbox_width = bbox_width
            entity.bbox_height = bbox_height
        
        # 更新任务为手动标注
        task = entity.task
        if task and task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        db.refresh(entity)
        
        has_bbox = entity.bbox_x is not None
        
        return {
            "success": True,
            "message": "图片实体更新成功",
            "data": {
                "id": entity.id,
                "entity_id": entity.entity_id,
                "image_id": image_id,
                "label": entity.label,
                "annotation_type": "region" if has_bbox else "whole_image",
                "bbox": {
                    "x": entity.bbox_x,
                    "y": entity.bbox_y,
                    "width": entity.bbox_width,
                    "height": entity.bbox_height
                } if has_bbox else None,
                "confidence": entity.confidence
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新图片实体失败: {str(e)}")


@router.delete("/{image_id}/entities/{entity_id}")
async def delete_image_entity(
    image_id: str,
    entity_id: int,
    db: Session = Depends(get_db)
):
    """
    删除图片实体
    """
    try:
        # 查询图片
        image = db.query(Image).filter(Image.image_id == image_id).first()
        
        if not image:
            raise HTTPException(status_code=404, detail="图片不存在")
        
        # 查询实体
        entity = db.query(ImageEntity)\
            .filter(ImageEntity.id == entity_id)\
            .filter(ImageEntity.image_id == image.id)\
            .first()
        
        if not entity:
            raise HTTPException(status_code=404, detail="图片实体不存在")
        
        # 删除实体
        db.delete(entity)
        
        # 更新任务为手动标注
        task = entity.task
        if task and task.annotation_type == 'automatic':
            task.annotation_type = 'manual'
        
        db.commit()
        
        return {
            "success": True,
            "message": "图片实体删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除图片实体失败: {str(e)}")
