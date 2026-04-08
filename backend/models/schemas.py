"""
Pydantic数据模型
用于API请求和响应的数据验证
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


# ============================================================================
# 枚举类型
# ============================================================================

class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnnotationType(str, Enum):
    """标注类型"""
    AUTOMATIC = "automatic"
    MANUAL = "manual"


class ReviewStatus(str, Enum):
    """复核状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ChangeType(str, Enum):
    """变更类型"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class UserRole(str, Enum):
    """用户角色"""
    ADMIN = "admin"
    ANNOTATOR = "annotator"
    REVIEWER = "reviewer"  # Task 47: 新增复核员角色
    VIEWER = "viewer"


# ============================================================================
# 基础模型
# ============================================================================

class BoundingBox(BaseModel):
    """边界框模型"""
    x: int = Field(..., description="X坐标")
    y: int = Field(..., description="Y坐标")
    width: int = Field(..., description="宽度")
    height: int = Field(..., description="高度")


class Entity(BaseModel):
    """文本实体模型"""
    id: int = Field(..., description="实体ID")
    token: str = Field(..., description="实体文本")
    label: str = Field(..., description="实体标签")
    start_offset: int = Field(..., description="起始偏移量")
    end_offset: int = Field(..., description="结束偏移量")
    confidence: Optional[float] = Field(None, description="置信度")


class ImageEntity(BaseModel):
    """图片实体模型"""
    id: int = Field(..., description="实体ID")
    image_id: str = Field(..., description="图片ID")
    label: str = Field(..., description="实体标签")
    bbox: Optional[BoundingBox] = Field(None, description="边界框（区域实体）")
    confidence: Optional[float] = Field(None, description="置信度")


class Relation(BaseModel):
    """关系模型"""
    id: int = Field(..., description="关系ID")
    from_id: int = Field(..., description="源实体ID")
    to_id: int = Field(..., description="目标实体ID")
    type: str = Field(..., description="关系类型")


# ============================================================================
# 用户相关模型
# ============================================================================

class UserCreate(BaseModel):
    """创建用户请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    role: UserRole = Field(..., description="用户角色")


class UserUpdate(BaseModel):
    """更新用户请求"""
    password: Optional[str] = Field(None, min_length=6, description="新密码")
    role: Optional[UserRole] = Field(None, description="用户角色")


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    role: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    user: UserResponse


# ============================================================================
# 语料相关模型
# ============================================================================

class ImageInfo(BaseModel):
    """图片信息"""
    image_id: str
    file_path: str
    original_name: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class CorpusRecord(BaseModel):
    """语料记录"""
    id: Optional[int] = None  # 数据库ID，用于创建数据集
    text_id: str
    text: str
    text_type: Optional[str] = None  # 句子分类
    source_file: Optional[str] = None
    source_row: Optional[int] = None
    source_field: Optional[str] = None
    has_images: bool = False
    images: List[ImageInfo] = []
    created_at: datetime
    
    model_config = {"from_attributes": True}


class CorpusListResponse(BaseModel):
    """语料列表响应"""
    total: int
    items: List[CorpusRecord]


class ExcelUploadResponse(BaseModel):
    """Excel上传响应"""
    success: bool
    message: str
    total_records: int
    total_sentences: int
    total_images: int
    field_distribution: Dict[str, int]  # 各字段句子分布


# ============================================================================
# 数据集相关模型
# ============================================================================

class DatasetCreateRequest(BaseModel):
    """创建数据集请求"""
    name: str = Field(..., min_length=1, max_length=255, description="数据集名称")
    description: Optional[str] = Field(None, description="数据集描述")
    corpus_ids: List[int] = Field(..., min_length=1, description="语料ID列表")
    created_by: int = Field(..., description="创建人ID")
    label_schema_version_id: Optional[int] = Field(None, description="标签体系版本ID")


class DatasetUpdateRequest(BaseModel):
    """更新数据集请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="数据集名称")
    description: Optional[str] = Field(None, description="数据集描述")


class DatasetResponse(BaseModel):
    """数据集响应"""
    success: bool = True
    message: str
    data: Dict[str, Any]


class DatasetListResponse(BaseModel):
    """数据集列表响应"""
    success: bool = True
    message: str
    data: Dict[str, Any]


class DatasetStatisticsResponse(BaseModel):
    """数据集统计响应"""
    success: bool = True
    message: str
    data: Dict[str, Any]


class DatasetExportRequest(BaseModel):
    """数据集导出请求"""
    output_path: Optional[str] = Field(None, description="导出路径")
    status_filter: Optional[List[str]] = Field(None, description="状态筛选")


# ============================================================================
# 标注任务相关模型
# ============================================================================

class AnnotationTask(BaseModel):
    """标注任务"""
    task_id: str
    dataset_id: str
    corpus_id: str
    text: str
    text_type: Optional[str] = None
    images: List[ImageInfo] = []
    status: TaskStatus
    annotation_type: AnnotationType
    current_version: int
    entities: List[Entity] = []
    image_entities: List[ImageEntity] = []
    relations: List[Relation] = []
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AddEntityRequest(BaseModel):
    """添加实体请求"""
    token: str = Field(..., description="实体文本")
    label: str = Field(..., description="实体标签")
    start_offset: int = Field(..., description="起始偏移量")
    end_offset: int = Field(..., description="结束偏移量")


class UpdateEntityRequest(BaseModel):
    """更新实体请求"""
    token: Optional[str] = None
    label: Optional[str] = None
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None


class AddImageEntityRequest(BaseModel):
    """添加图片实体请求"""
    image_id: str = Field(..., description="图片ID")
    label: str = Field(..., description="实体标签")
    bbox: Optional[BoundingBox] = Field(None, description="边界框（可选）")


class AddRelationRequest(BaseModel):
    """添加关系请求"""
    from_id: int = Field(..., description="源实体ID")
    to_id: int = Field(..., description="目标实体ID")
    type: str = Field(default="relates_to", description="关系类型")


class UpdateRelationRequest(BaseModel):
    """更新关系请求"""
    from_id: Optional[int] = None
    to_id: Optional[int] = None
    type: Optional[str] = None


# ============================================================================
# 批量标注相关模型
# ============================================================================

class BatchAnnotationRequest(BaseModel):
    """批量标注请求"""
    dataset_id: str = Field(..., description="数据集ID")


class BatchJobResponse(BaseModel):
    """批量任务响应"""
    job_id: str
    dataset_id: str
    status: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    progress: float  # 进度百分比
    started_at: Optional[datetime]
    completed_at: Optional[datetime]


# ============================================================================
# 标签配置相关模型
# ============================================================================

class EntityTypeConfig(BaseModel):
    """实体类型配置"""
    type_name: str = Field(..., description="类型名称")
    type_name_zh: str = Field(..., description="中文名称")
    color: str = Field(..., description="颜色代码")
    description: Optional[str] = Field(None, description="描述")
    supports_bbox: bool = Field(default=False, description="是否支持边界框")
    is_active: bool = Field(default=True, description="是否激活")


class RelationTypeConfig(BaseModel):
    """关系类型配置"""
    type_name: str = Field(..., description="类型名称")
    type_name_zh: str = Field(..., description="中文名称")
    color: str = Field(..., description="颜色代码")
    description: Optional[str] = Field(None, description="描述")
    is_active: bool = Field(default=True, description="是否激活")


class LabelSchema(BaseModel):
    """标签体系"""
    entity_types: List[EntityTypeConfig]
    relation_types: List[RelationTypeConfig]


# ============================================================================
# 复核相关模型
# ============================================================================

class SubmitReviewRequest(BaseModel):
    """提交复核请求"""
    task_id: str = Field(..., description="任务ID")


class ReviewActionRequest(BaseModel):
    """复核操作请求"""
    reviewer_id: Optional[int] = Field(1, description="复核人员ID")
    review_comment: Optional[str] = Field(None, description="复核意见")


class ReviewTaskResponse(BaseModel):
    """复核任务响应"""
    review_id: str
    task_id: str
    status: ReviewStatus
    reviewer_id: Optional[int]  # 改为 int 类型
    review_comment: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime


# ============================================================================
# 版本管理相关模型
# ============================================================================

class VersionResponse(BaseModel):
    """版本响应"""
    history_id: str
    task_id: str
    version: int
    change_type: ChangeType
    change_description: Optional[str]
    changed_by: str
    created_at: datetime


class VersionDiff(BaseModel):
    """版本差异"""
    from_version: int
    to_version: int
    added_entities: List[Entity] = []
    deleted_entities: List[Entity] = []
    modified_entities: List[Dict[str, Any]] = []
    added_relations: List[Relation] = []
    deleted_relations: List[Relation] = []
    modified_relations: List[Dict[str, Any]] = []


# ============================================================================
# 导出相关模型
# ============================================================================

class ExportRequest(BaseModel):
    """导出请求"""
    dataset_id: str = Field(..., description="数据集ID")
    status_filter: Optional[List[str]] = Field(None, description="状态筛选")
    text_type_filter: Optional[List[str]] = Field(None, description="句子分类筛选")
    train_test_split: Optional[float] = Field(None, ge=0, le=1, description="训练集比例")


class ExportResponse(BaseModel):
    """导出响应"""
    success: bool
    file_path: str
    total_records: int
    message: str


# ============================================================================
# 通用响应模型
# ============================================================================

class SuccessResponse(BaseModel):
    """成功响应"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = False
    error_code: str
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# 数据集分配相关模型 (Task 47)
# ============================================================================

class AssignmentMode(str, Enum):
    """分配模式"""
    FULL = "full"  # 整体分配
    RANGE = "range"  # 范围分配


class TransferMode(str, Enum):
    """转移模式"""
    ALL = "all"  # 转移所有任务
    REMAINING = "remaining"  # 只转移未完成的任务
    COMPLETED = "completed"  # 只转移已完成的任务


class AssignmentRole(str, Enum):
    """分配角色"""
    ANNOTATOR = "annotator"
    REVIEWER = "reviewer"


class AssignmentRequest(BaseModel):
    """分配数据集请求"""
    user_id: int = Field(..., description="用户ID")
    role: AssignmentRole = Field(..., description="分配角色")
    mode: AssignmentMode = Field(AssignmentMode.FULL, description="分配模式")
    start_index: Optional[int] = Field(None, description="起始任务索引（范围模式必需）")
    end_index: Optional[int] = Field(None, description="结束任务索引（范围模式必需）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 2,
                "role": "annotator",
                "mode": "range",
                "start_index": 1,
                "end_index": 200
            }
        }


class AutoAssignmentRequest(BaseModel):
    """自动分配数据集请求"""
    user_ids: List[int] = Field(..., min_length=1, description="用户ID列表")
    role: AssignmentRole = Field(..., description="分配角色")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_ids": [2, 3, 4],
                "role": "annotator"
            }
        }


class BatchAssignmentItem(BaseModel):
    """批量分配项"""
    user_id: int = Field(..., description="用户ID")
    role: AssignmentRole = Field(..., description="分配角色")
    mode: AssignmentMode = Field(AssignmentMode.FULL, description="分配模式")
    start_index: Optional[int] = Field(None, description="起始任务索引（范围模式必需）")
    end_index: Optional[int] = Field(None, description="结束任务索引（范围模式必需）")


class BatchAssignmentRequest(BaseModel):
    """批量分配请求"""
    assignments: List[BatchAssignmentItem] = Field(..., min_length=1, description="分配列表")
    clear_existing: bool = Field(True, description="是否清空现有分配")
    role_filter: Optional[AssignmentRole] = Field(None, description="清空时的角色筛选")
    
    class Config:
        json_schema_extra = {
            "example": {
                "assignments": [
                    {
                        "user_id": 2,
                        "role": "annotator",
                        "mode": "range",
                        "start_index": 1,
                        "end_index": 50
                    },
                    {
                        "user_id": 3,
                        "role": "annotator",
                        "mode": "range",
                        "start_index": 51,
                        "end_index": 100
                    }
                ],
                "clear_existing": True,
                "role_filter": "annotator"
            }
        }


class TransferAssignmentRequest(BaseModel):
    """转移分配请求"""
    old_user_id: int = Field(..., description="原用户ID")
    new_user_id: int = Field(..., description="新用户ID")
    role: AssignmentRole = Field(..., description="角色")
    transfer_mode: TransferMode = Field(TransferMode.ALL, description="转移模式")
    transfer_reason: Optional[str] = Field(None, description="转移原因")
    
    class Config:
        json_schema_extra = {
            "example": {
                "old_user_id": 2,
                "new_user_id": 3,
                "role": "annotator",
                "transfer_mode": "all",
                "transfer_reason": "标注员离职"
            }
        }


class AssignmentInfo(BaseModel):
    """分配信息"""
    assignment_id: int = Field(..., description="分配ID")
    dataset_id: str = Field(..., description="数据集ID")
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    role: str = Field(..., description="角色")
    task_range: Optional[str] = Field(None, description="任务范围（如：1-200）")
    task_count: int = Field(..., description="任务数量")
    completed_count: int = Field(0, description="已完成数量")
    in_review_count: int = Field(0, description="复核中数量")
    is_active: bool = Field(True, description="是否激活")
    transferred_to: Optional[int] = Field(None, description="转移给谁")
    transferred_to_username: Optional[str] = Field(None, description="转移给谁（用户名）")
    transferred_at: Optional[datetime] = Field(None, description="转移时间")
    transfer_reason: Optional[str] = Field(None, description="转移原因")
    assigned_by: Optional[int] = Field(None, description="分配人ID")
    assigned_at: datetime = Field(..., description="分配时间")


class AssignmentResponse(BaseModel):
    """分配响应"""
    success: bool = True
    message: str
    data: AssignmentInfo


class AutoAssignmentInfo(BaseModel):
    """自动分配信息"""
    user_id: int
    username: str
    task_range: str
    task_count: int


class AutoAssignmentResponse(BaseModel):
    """自动分配响应"""
    success: bool = True
    message: str
    data: Dict[str, Any] = Field(..., description="包含 assignments 和 total_tasks")


class AssignmentListResponse(BaseModel):
    """分配列表响应"""
    success: bool = True
    message: str = "获取分配列表成功"
    data: Dict[str, Any] = Field(..., description="包含 dataset_id, assignments, unassigned_count 等")


class MyDatasetInfo(BaseModel):
    """我的数据集信息"""
    dataset_id: str
    name: str
    description: Optional[str]
    my_role: str
    my_task_range: Optional[str]
    my_task_count: int
    my_completed_count: int
    total_tasks: int
    assigned_at: datetime


class MyDatasetsResponse(BaseModel):
    """我的数据集列表响应"""
    success: bool = True
    message: str = "获取我的数据集成功"
    data: Dict[str, Any] = Field(..., description="包含 items, total, page, page_size")


class TransferAssignmentResponse(BaseModel):
    """转移分配响应"""
    success: bool = True
    message: str
    data: Dict[str, Any] = Field(..., description="包含转移详情")


class CancelAssignmentCheckResponse(BaseModel):
    """取消分配检查响应"""
    can_cancel: bool
    reason: str
    stats: Dict[str, int]
    action: Optional[str] = None  # 'transfer' 表示需要使用转移功能
