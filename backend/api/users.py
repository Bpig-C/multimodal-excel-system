"""
用户管理和认证API
实现用户CRUD、登录登出和JWT认证
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from services.user_service import UserService
from models.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    LoginRequest,
    LoginResponse,
    SuccessResponse
)

router = APIRouter(prefix="/api/v1/users", tags=["users"])
auth_router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

# HTTPBearer 安全方案（Swagger UI 🔒 Authorize 按钮使用）
_bearer_scheme = HTTPBearer(auto_error=False)


# ============================================================================
# 依赖注入
# ============================================================================

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """获取用户服务实例"""
    return UserService(db)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
    user_service: UserService = Depends(get_user_service)
) -> dict:
    """
    从JWT令牌获取当前用户（支持 Swagger UI Authorize 按钮）
    
    Args:
        credentials: HTTPBearer 自动解析的 Bearer 令牌
        user_service: 用户服务
    
    Returns:
        dict: 用户信息
    
    Raises:
        HTTPException: 认证失败
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证令牌"
        )
    
    token = credentials.credentials
    
    # 验证令牌
    payload = user_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌无效或已过期"
        )
    
    return payload


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    要求管理员权限
    
    Args:
        current_user: 当前用户
    
    Returns:
        dict: 用户信息
    
    Raises:
        HTTPException: 权限不足
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    
    return current_user


# ============================================================================
# 认证API
# ============================================================================

@auth_router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    用户登录
    
    Args:
        request: 登录请求
        user_service: 用户服务
    
    Returns:
        LoginResponse: 登录响应（包含JWT令牌）
    
    Raises:
        HTTPException: 用户名或密码错误
    """
    # 认证用户
    user = user_service.authenticate(request.username, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 生成JWT令牌
    access_token = user_service.create_access_token(
        user_id=user.id,
        username=user.username,
        role=user.role
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@auth_router.post("/logout", response_model=SuccessResponse)
def logout(current_user: dict = Depends(get_current_user)):
    """
    用户登出
    
    Note: JWT是无状态的，登出主要由前端处理（删除token）
    此接口主要用于记录登出日志或执行其他清理操作
    
    Args:
        current_user: 当前用户
    
    Returns:
        SuccessResponse: 成功响应
    """
    return SuccessResponse(
        success=True,
        message=f"用户 {current_user['username']} 已登出"
    )


@auth_router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    获取当前用户信息
    
    Args:
        current_user: 当前用户
        user_service: 用户服务
    
    Returns:
        UserResponse: 用户信息
    
    Raises:
        HTTPException: 用户不存在
    """
    user = user_service.get_user_by_id(current_user["user_id"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return UserResponse.model_validate(user)


# ============================================================================
# 用户管理API
# ============================================================================

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserCreate,
    user_service: UserService = Depends(get_user_service),
    admin: dict = Depends(require_admin)
):
    """
    创建用户（需要管理员权限）
    
    Args:
        request: 创建用户请求
        user_service: 用户服务
        admin: 管理员用户
    
    Returns:
        UserResponse: 创建的用户
    
    Raises:
        HTTPException: 用户名已存在或角色无效
    """
    try:
        user = user_service.create_user(
            username=request.username,
            password=request.password,
            role=request.role.value
        )
        
        return UserResponse.model_validate(user)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=List[UserResponse])
def list_users(
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user)
):
    """
    获取用户列表
    
    Args:
        role: 角色筛选（可选）
        skip: 跳过记录数
        limit: 返回记录数
        user_service: 用户服务
        current_user: 当前用户
    
    Returns:
        List[UserResponse]: 用户列表
    """
    users, total = user_service.list_users(role=role, skip=skip, limit=limit)
    
    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user)
):
    """
    获取用户详情
    
    Args:
        user_id: 用户ID
        user_service: 用户服务
        current_user: 当前用户
    
    Returns:
        UserResponse: 用户信息
    
    Raises:
        HTTPException: 用户不存在
    """
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户不存在: {user_id}"
        )
    
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    request: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    admin: dict = Depends(require_admin)
):
    """
    更新用户信息（需要管理员权限）
    
    Args:
        user_id: 用户ID
        request: 更新用户请求
        user_service: 用户服务
        admin: 管理员用户
    
    Returns:
        UserResponse: 更新后的用户
    
    Raises:
        HTTPException: 用户不存在或用户名已被占用
    """
    try:
        user = user_service.update_user(
            user_id=user_id,
            password=request.password,
            role=request.role.value if request.role else None
        )
        
        return UserResponse.model_validate(user)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", response_model=SuccessResponse)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    admin: dict = Depends(require_admin)
):
    """
    删除用户（需要管理员权限）
    
    Args:
        user_id: 用户ID
        user_service: 用户服务
        admin: 管理员用户
    
    Returns:
        SuccessResponse: 成功响应
    
    Raises:
        HTTPException: 用户不存在
    """
    try:
        user_service.delete_user(user_id)
        
        return SuccessResponse(
            success=True,
            message=f"用户已删除: {user_id}"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/statistics/summary")
def get_user_statistics(
    user_service: UserService = Depends(get_user_service),
    admin: dict = Depends(require_admin)
):
    """
    获取用户统计信息（需要管理员权限）
    
    Args:
        user_service: 用户服务
        admin: 管理员用户
    
    Returns:
        dict: 统计信息
    """
    stats = user_service.get_user_statistics()
    
    return SuccessResponse(
        success=True,
        message="获取用户统计成功",
        data=stats
    )
