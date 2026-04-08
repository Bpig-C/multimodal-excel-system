"""
用户管理服务
实现用户CRUD、密码加密、JWT Token生成和权限检查
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.db_models import User
from config import settings


class UserService:
    """用户管理服务类"""
    
    # JWT配置
    SECRET_KEY = settings.SECRET_KEY if hasattr(settings, 'SECRET_KEY') else "your-secret-key-change-in-production"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时
    
    def __init__(self, db: Session):
        self.db = db
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        密码加密
        
        Args:
            password: 明文密码
        
        Returns:
            str: 加密后的密码哈希
        """
        # 使用bcrypt加密
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        Args:
            plain_password: 明文密码
            hashed_password: 加密后的密码哈希
        
        Returns:
            bool: 密码是否匹配
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            print(f"密码验证错误: {e}")
            return False
    
    def create_user(
        self,
        username: str,
        password: str,
        role: str
    ) -> User:
        """
        创建用户
        
        Args:
            username: 用户名
            password: 密码
            role: 角色（admin/annotator/viewer）
        
        Returns:
            User: 创建的用户
        
        Raises:
            ValueError: 用户名已存在或角色无效
        """
        # 验证角色（Task 47: 添加 reviewer 角色）
        valid_roles = ['admin', 'annotator', 'reviewer', 'viewer']
        if role not in valid_roles:
            raise ValueError(f"无效的角色: {role}，必须是 {valid_roles} 之一")
        
        # 检查用户名是否已存在
        existing_user = self.db.query(User).filter(
            User.username == username
        ).first()
        
        if existing_user:
            raise ValueError(f"用户名已存在: {username}")
        
        # 创建用户
        user = User(
            username=username,
            password_hash=self.hash_password(password),
            role=role
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        根据ID获取用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[User]: 用户对象，不存在则返回None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
        
        Returns:
            Optional[User]: 用户对象，不存在则返回None
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def list_users(
        self,
        role: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[User], int]:
        """
        获取用户列表
        
        Args:
            role: 角色筛选
            skip: 跳过记录数
            limit: 返回记录数
        
        Returns:
            tuple: (用户列表, 总数)
        """
        query = self.db.query(User)
        
        # 角色筛选
        if role:
            query = query.filter(User.role == role)
        
        # 获取总数
        total = query.count()
        
        # 分页查询
        users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
        
        return users, total
    
    def update_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        role: Optional[str] = None
    ) -> User:
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            username: 新用户名（可选）
            password: 新密码（可选）
            role: 新角色（可选）
        
        Returns:
            User: 更新后的用户
        
        Raises:
            ValueError: 用户不存在或用户名已被占用
        """
        user = self.get_user_by_id(user_id)
        
        if not user:
            raise ValueError(f"用户不存在: {user_id}")
        
        # 更新用户名
        if username and username != user.username:
            # 检查新用户名是否已被占用
            existing = self.db.query(User).filter(
                User.username == username,
                User.id != user_id
            ).first()
            
            if existing:
                raise ValueError(f"用户名已被占用: {username}")
            
            user.username = username
        
        # 更新密码
        if password:
            user.password_hash = self.hash_password(password)
        
        # 更新角色（Task 47: 添加 reviewer 角色）
        if role:
            valid_roles = ['admin', 'annotator', 'reviewer', 'viewer']
            if role not in valid_roles:
                raise ValueError(f"无效的角色: {role}")
            user.role = role
        
        user.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """
        删除用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 是否删除成功
        
        Raises:
            ValueError: 用户不存在
        """
        user = self.get_user_by_id(user_id)
        
        if not user:
            raise ValueError(f"用户不存在: {user_id}")
        
        self.db.delete(user)
        self.db.commit()
        
        return True
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        用户认证
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            Optional[User]: 认证成功返回用户对象，失败返回None
        """
        user = self.get_user_by_username(username)
        
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        return user
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        用户认证（别名方法，与authenticate相同）
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            Optional[User]: 认证成功返回用户对象，失败返回None
        """
        return self.authenticate(username, password)
    
    def create_access_token(
        self,
        user_id: int,
        username: str,
        role: str
    ) -> str:
        """
        创建JWT访问令牌
        
        Args:
            user_id: 用户ID
            username: 用户名
            role: 角色
        
        Returns:
            str: JWT令牌
        """
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        payload = {
            "user_id": user_id,
            "username": username,
            "role": role,
            "exp": expire
        }
        
        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证JWT令牌
        
        Args:
            token: JWT令牌
        
        Returns:
            Optional[Dict]: 令牌有效返回payload，无效返回None
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            # 令牌已过期
            return None
        except jwt.InvalidTokenError:
            # 令牌无效
            return None
    
    def check_permission(
        self,
        user_id: int,
        required_role: str
    ) -> bool:
        """
        检查用户权限
        
        Args:
            user_id: 用户ID
            required_role: 需要的角色
        
        Returns:
            bool: 是否有权限
        """
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        # 管理员拥有所有权限
        if user.role == 'admin':
            return True
        
        # 检查角色匹配
        return user.role == required_role
    
    def can_review(self, user_id: int, task_assigned_to: Optional[int] = None) -> bool:
        """
        检查用户是否可以进行复核
        
        Args:
            user_id: 用户ID
            task_assigned_to: 任务分配给的用户ID（可选）
        
        Returns:
            bool: 是否可以复核
        """
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        # 管理员可以复核所有任务
        if user.role == 'admin':
            return True
        
        # 标注员可以复核他人的任务
        if user.role == 'annotator':
            # 如果提供了任务分配信息，检查是否是自己的任务
            if task_assigned_to is not None:
                return task_assigned_to != user_id
            # 如果没有提供任务分配信息，默认允许（在API层再做详细检查）
            return True
        
        # 浏览员不能复核
        return False
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """
        获取用户统计信息
        
        Returns:
            Dict: 统计信息
        """
        total_users = self.db.query(User).count()
        admin_count = self.db.query(User).filter(User.role == 'admin').count()
        annotator_count = self.db.query(User).filter(User.role == 'annotator').count()
        reviewer_count = self.db.query(User).filter(User.role == 'reviewer').count()
        
        return {
            "total_users": total_users,
            "admin_count": admin_count,
            "annotator_count": annotator_count,
            "reviewer_count": reviewer_count
        }
