"""
版本管理API
提供标注任务的版本历史查询、回滚和比较功能
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session

from database import get_db
from services.version_management_service import VersionManagementService

router = APIRouter(prefix="/api/v1/versions", tags=["versions"])


# ============================================================================
# 版本历史API
# ============================================================================

@router.get("/{task_id}")
async def get_version_history(
    task_id: str,
    limit: Optional[int] = Query(None, description="返回数量限制"),
    db: Session = Depends(get_db)
):
    """
    获取标注任务的版本历史
    
    返回按时间倒序排列的版本历史列表
    """
    try:
        service = VersionManagementService(db)
        history = service.get_version_history(task_id, limit)
        
        return {
            "success": True,
            "message": "获取版本历史成功",
            "data": {
                "task_id": task_id,
                "total": len(history),
                "versions": history
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取版本历史失败: {str(e)}")


# ============================================================================
# 版本回滚API
# ============================================================================

@router.post("/{task_id}/rollback")
async def rollback_version(
    task_id: str,
    target_version: int = Body(..., description="目标版本号"),
    changed_by: Optional[int] = Body(None, description="操作人ID"),
    db: Session = Depends(get_db)
):
    """
    回滚到指定版本
    
    注意:
    - 回滚前会自动创建当前版本的备份
    - 回滚后会创建新的版本记录
    - 回滚操作不可撤销,请谨慎操作
    """
    try:
        service = VersionManagementService(db)
        success = service.rollback_to_version(
            task_id=task_id,
            target_version=target_version,
            changed_by=changed_by
        )
        
        if success:
            return {
                "success": True,
                "message": f"成功回滚到版本 {target_version}",
                "data": {
                    "task_id": task_id,
                    "target_version": target_version
                }
            }
        else:
            raise HTTPException(status_code=400, detail="回滚失败")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"版本回滚失败: {str(e)}")


# ============================================================================
# 版本比较API
# ============================================================================

@router.get("/compare")
async def compare_versions(
    task_id: str = Query(..., description="任务ID"),
    version1: int = Query(..., description="版本1"),
    version2: int = Query(..., description="版本2"),
    db: Session = Depends(get_db)
):
    """
    比较两个版本的差异
    
    返回两个版本之间的详细差异信息,包括:
    - 新增的实体、图片实体、关系
    - 删除的实体、图片实体、关系
    - 修改的实体、图片实体、关系
    """
    try:
        service = VersionManagementService(db)
        diff = service.compare_versions(
            task_id=task_id,
            version1=version1,
            version2=version2
        )
        
        return {
            "success": True,
            "message": "版本比较成功",
            "data": diff
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"版本比较失败: {str(e)}")


# ============================================================================
# 版本详情API
# ============================================================================

@router.get("/{task_id}/{version}")
async def get_version_detail(
    task_id: str,
    version: int,
    db: Session = Depends(get_db)
):
    """
    获取指定版本的详细信息
    
    返回该版本的完整快照数据
    """
    try:
        from models.db_models import AnnotationTask, VersionHistory
        import json
        
        # 查询任务
        task = db.query(AnnotationTask).filter(
            AnnotationTask.task_id == task_id
        ).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        # 查询版本
        version_history = db.query(VersionHistory)\
            .filter(VersionHistory.task_id == task.id)\
            .filter(VersionHistory.version == version)\
            .first()
        
        if not version_history:
            raise HTTPException(status_code=404, detail=f"版本 {version} 不存在")
        
        # 解析快照数据
        snapshot_data = json.loads(version_history.snapshot_data)
        
        return {
            "success": True,
            "message": "获取版本详情成功",
            "data": {
                "history_id": version_history.history_id,
                "task_id": task_id,
                "version": version,
                "change_type": version_history.change_type,
                "change_description": version_history.change_description,
                "changed_by": version_history.changed_by,
                "created_at": version_history.created_at.isoformat(),
                "is_current": version == task.current_version,
                "snapshot": snapshot_data
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取版本详情失败: {str(e)}")


# ============================================================================
# 创建版本快照API
# ============================================================================

@router.post("/{task_id}/snapshot")
async def create_version_snapshot(
    task_id: str,
    change_description: Optional[str] = Body(None, description="变更描述"),
    changed_by: Optional[int] = Body(None, description="操作人ID"),
    db: Session = Depends(get_db)
):
    """
    手动创建版本快照
    
    用于在重要操作前手动保存当前状态
    """
    try:
        service = VersionManagementService(db)
        version_history = service.create_version(
            task_id=task_id,
            change_type='update',
            change_description=change_description or '手动创建快照',
            changed_by=changed_by
        )
        
        return {
            "success": True,
            "message": "版本快照创建成功",
            "data": {
                "history_id": version_history.history_id,
                "task_id": task_id,
                "version": version_history.version,
                "created_at": version_history.created_at.isoformat()
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建版本快照失败: {str(e)}")
