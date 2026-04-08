"""
存储服务 - 支持本地文件系统和MinIO对象存储
提供统一的文件存储接口，可通过配置切换存储方式
"""
from pathlib import Path
from typing import Optional, BinaryIO
import io
from config import settings


class StorageService:
    """统一存储服务接口"""
    
    def __init__(self):
        self.storage_type = settings.STORAGE_TYPE  # 'local' or 'minio'
        
        if self.storage_type == 'minio':
            try:
                from minio import Minio
                self.minio_client = Minio(
                    settings.MINIO_ENDPOINT,
                    access_key=settings.MINIO_ACCESS_KEY,
                    secret_key=settings.MINIO_SECRET_KEY,
                    secure=settings.MINIO_SECURE
                )
                # 确保bucket存在
                if not self.minio_client.bucket_exists(settings.MINIO_BUCKET):
                    self.minio_client.make_bucket(settings.MINIO_BUCKET)
                print(f"✓ MinIO存储已初始化: {settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}")
            except ImportError:
                print("⚠️  MinIO库未安装，切换到本地存储模式")
                print("   安装方法: pip install minio")
                self.storage_type = 'local'
            except Exception as e:
                print(f"⚠️  MinIO连接失败，切换到本地存储模式: {e}")
                self.storage_type = 'local'
    
    def save_image(
        self, 
        file_data: bytes, 
        relative_path: str,
        content_type: str = 'image/png'
    ) -> str:
        """
        保存图片文件
        
        Args:
            file_data: 文件二进制数据
            relative_path: 相对路径，如 "文件名/ID_XXX.png"
            content_type: 文件MIME类型
            
        Returns:
            文件访问路径（相对路径）
        """
        if self.storage_type == 'minio':
            return self._save_to_minio(file_data, relative_path, content_type)
        else:
            return self._save_to_local(file_data, relative_path)
    
    def _save_to_local(self, file_data: bytes, relative_path: str) -> str:
        """保存到本地文件系统"""
        full_path = settings.IMAGE_DIR / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'wb') as f:
            f.write(file_data)
        
        return relative_path
    
    def _save_to_minio(self, file_data: bytes, relative_path: str, content_type: str) -> str:
        """保存到MinIO对象存储"""
        # 将bytes转换为BytesIO对象
        file_stream = io.BytesIO(file_data)
        file_size = len(file_data)
        
        # 上传到MinIO
        self.minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=relative_path,
            data=file_stream,
            length=file_size,
            content_type=content_type
        )
        
        return relative_path
    
    def get_image(self, relative_path: str) -> Optional[bytes]:
        """
        获取图片文件
        
        Args:
            relative_path: 相对路径
            
        Returns:
            文件二进制数据，如果不存在返回None
        """
        if self.storage_type == 'minio':
            return self._get_from_minio(relative_path)
        else:
            return self._get_from_local(relative_path)
    
    def _get_from_local(self, relative_path: str) -> Optional[bytes]:
        """从本地文件系统获取"""
        full_path = settings.IMAGE_DIR / relative_path
        
        if not full_path.exists():
            return None
        
        with open(full_path, 'rb') as f:
            return f.read()
    
    def _get_from_minio(self, relative_path: str) -> Optional[bytes]:
        """从MinIO获取"""
        try:
            response = self.minio_client.get_object(
                bucket_name=settings.MINIO_BUCKET,
                object_name=relative_path
            )
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except Exception as e:
            print(f"从MinIO获取文件失败 {relative_path}: {e}")
            return None
    
    def delete_image(self, relative_path: str) -> bool:
        """
        删除图片文件
        
        Args:
            relative_path: 相对路径
            
        Returns:
            是否删除成功
        """
        if self.storage_type == 'minio':
            return self._delete_from_minio(relative_path)
        else:
            return self._delete_from_local(relative_path)
    
    def _delete_from_local(self, relative_path: str) -> bool:
        """从本地文件系统删除"""
        full_path = settings.IMAGE_DIR / relative_path
        
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    
    def _delete_from_minio(self, relative_path: str) -> bool:
        """从MinIO删除"""
        try:
            self.minio_client.remove_object(
                bucket_name=settings.MINIO_BUCKET,
                object_name=relative_path
            )
            return True
        except Exception as e:
            print(f"从MinIO删除文件失败 {relative_path}: {e}")
            return False
    
    def get_public_url(self, relative_path: str) -> str:
        """
        获取文件的公开访问URL
        
        Args:
            relative_path: 相对路径
            
        Returns:
            完整的访问URL
        """
        if self.storage_type == 'minio' and settings.MINIO_PUBLIC_URL:
            # 如果配置了MinIO公开URL，直接返回
            return f"{settings.MINIO_PUBLIC_URL}/{settings.MINIO_BUCKET}/{relative_path}"
        else:
            # 否则通过后端代理访问
            return f"/images/{relative_path}"


# 创建全局存储服务实例
storage_service = StorageService()
