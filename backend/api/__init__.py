"""
API路由包
"""
from .corpus import router as corpus_router
from .dataset import router as dataset_router
from .labels import router as labels_router
from .annotations import router as annotations_router
from .images import router as images_router
from .versions import router as versions_router
from .review import router as review_router
from .users import router as users_router, auth_router

__all__ = ['corpus_router', 'dataset_router', 'labels_router', 'annotations_router', 'images_router', 'versions_router', 'review_router', 'users_router', 'auth_router']
