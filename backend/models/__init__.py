"""
数据模型包
"""
# SQLAlchemy数据库模型
from .db_models import (
    User, Corpus, Image, Dataset, DatasetCorpus,
    AnnotationTask, TextEntity, ImageEntity, Relation,
    EntityType, RelationType, ReviewTask, VersionHistory, BatchJob
)

# Pydantic数据模型
from .schemas import (
    # 枚举
    TaskStatus, AnnotationType, ReviewStatus, ChangeType, UserRole,
    # 基础模型
    BoundingBox, Entity as EntitySchema, ImageEntity as ImageEntitySchema, 
    Relation as RelationSchema,
    # 用户模型
    UserCreate, UserUpdate, UserResponse, LoginRequest, LoginResponse,
    # 语料模型
    ImageInfo, CorpusRecord, CorpusListResponse, ExcelUploadResponse,
    # 数据集模型
    DatasetCreateRequest, DatasetUpdateRequest, DatasetResponse, DatasetListResponse,
    DatasetStatisticsResponse, DatasetExportRequest,
    # 标注任务模型
    AnnotationTask as AnnotationTaskSchema, AddEntityRequest, UpdateEntityRequest,
    AddImageEntityRequest, AddRelationRequest, UpdateRelationRequest,
    # 批量标注模型
    BatchAnnotationRequest, BatchJobResponse,
    # 标签配置模型
    EntityTypeConfig, RelationTypeConfig, LabelSchema,
    # 复核模型
    SubmitReviewRequest, ReviewActionRequest, ReviewTaskResponse,
    # 版本模型
    VersionResponse, VersionDiff,
    # 导出模型
    ExportRequest, ExportResponse,
    # 通用响应
    SuccessResponse, ErrorResponse
)

__all__ = [
    # 数据库模型
    "User", "Corpus", "Image", "Dataset", "DatasetCorpus",
    "AnnotationTask", "TextEntity", "ImageEntity", "Relation",
    "EntityType", "RelationType", "ReviewTask", "VersionHistory", "BatchJob",
    # Pydantic模型
    "TaskStatus", "AnnotationType", "ReviewStatus", "ChangeType", "UserRole",
    "BoundingBox", "EntitySchema", "ImageEntitySchema", "RelationSchema",
    "UserCreate", "UserUpdate", "UserResponse", "LoginRequest", "LoginResponse",
    "ImageInfo", "CorpusRecord", "CorpusListResponse", "ExcelUploadResponse",
    "DatasetCreateRequest", "DatasetUpdateRequest", "DatasetResponse", "DatasetListResponse",
    "DatasetStatisticsResponse", "DatasetExportRequest",
    "AnnotationTaskSchema", "AddEntityRequest", "UpdateEntityRequest",
    "AddImageEntityRequest", "AddRelationRequest", "UpdateRelationRequest",
    "BatchAnnotationRequest", "BatchJobResponse",
    "EntityTypeConfig", "RelationTypeConfig", "LabelSchema",
    "SubmitReviewRequest", "ReviewActionRequest", "ReviewTaskResponse",
    "VersionResponse", "VersionDiff",
    "ExportRequest", "ExportResponse",
    "SuccessResponse", "ErrorResponse"
]
