"""
SQLAlchemy数据库模型
定义所有数据库表结构
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, 
    DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # 'admin', 'annotator', 'reviewer'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    datasets = relationship("Dataset", back_populates="creator")
    annotation_tasks = relationship("AnnotationTask", back_populates="assignee")
    dataset_assignments = relationship("DatasetAssignment", foreign_keys="DatasetAssignment.user_id", back_populates="user")


class Corpus(Base):
    """原始语料表"""
    __tablename__ = "corpus"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text_id = Column(String(100), unique=True, nullable=False, index=True)
    text = Column(Text, nullable=False)
    text_type = Column(String(100))  # 句子分类（字段来源）
    source_file = Column(String(255))
    source_row = Column(Integer)
    source_field = Column(String(100), index=True)
    has_images = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    images = relationship("Image", back_populates="corpus", cascade="all, delete-orphan")
    dataset_associations = relationship("DatasetCorpus", back_populates="corpus")


class Image(Base):
    """图片表"""
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(String(100), unique=True, nullable=False, index=True)
    corpus_id = Column(Integer, ForeignKey("corpus.id", ondelete="CASCADE"))
    file_path = Column(String(500), nullable=False)
    original_name = Column(String(255))
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    corpus = relationship("Corpus", back_populates="images")
    image_entities = relationship("ImageEntity", back_populates="image", cascade="all, delete-orphan")


class Dataset(Base):
    """数据集表"""
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    label_schema_version_id = Column(Integer, ForeignKey("label_schema_versions.id"))  # 使用的标签体系版本
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    creator = relationship("User", back_populates="datasets")
    label_schema_version = relationship("LabelSchemaVersion", back_populates="datasets")
    corpus_associations = relationship("DatasetCorpus", back_populates="dataset", cascade="all, delete-orphan")
    annotation_tasks = relationship("AnnotationTask", back_populates="dataset", cascade="all, delete-orphan")
    batch_jobs = relationship("BatchJob", back_populates="dataset", cascade="all, delete-orphan")
    assignments = relationship("DatasetAssignment", back_populates="dataset", cascade="all, delete-orphan")


class DatasetCorpus(Base):
    """数据集-语料关联表"""
    __tablename__ = "dataset_corpus"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    corpus_id = Column(Integer, ForeignKey("corpus.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 唯一约束
    __table_args__ = (UniqueConstraint('dataset_id', 'corpus_id', name='uix_dataset_corpus'),)
    
    # 关系
    dataset = relationship("Dataset", back_populates="corpus_associations")
    corpus = relationship("Corpus", back_populates="dataset_associations")


class DatasetAssignment(Base):
    """数据集分配表"""
    __tablename__ = "dataset_assignments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False, index=True)  # 'annotator' 或 'reviewer'
    
    # 任务范围（可选，NULL表示分配所有任务）
    task_start_index = Column(Integer)  # 起始索引（从1开始，包含）
    task_end_index = Column(Integer)    # 结束索引（包含）
    
    # 分配状态
    is_active = Column(Boolean, default=True, nullable=False, index=True)  # 是否激活
    
    # 转移信息
    transferred_to = Column(Integer, ForeignKey("users.id"))  # 转移给谁
    transferred_at = Column(DateTime)  # 转移时间
    transfer_reason = Column(Text)  # 转移原因
    
    # 分配信息
    assigned_by = Column(Integer, ForeignKey("users.id"))  # 分配人
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    dataset = relationship("Dataset", back_populates="assignments")
    user = relationship("User", foreign_keys=[user_id], back_populates="dataset_assignments")
    assigner = relationship("User", foreign_keys=[assigned_by])
    transferred_to_user = relationship("User", foreign_keys=[transferred_to])
    
    # 索引
    __table_args__ = (
        UniqueConstraint('dataset_id', 'user_id', 'role', 'is_active', name='uix_dataset_user_role_active'),
    )


class AnnotationTask(Base):
    """标注任务表"""
    __tablename__ = "annotation_tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(100), unique=True, nullable=False, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    corpus_id = Column(Integer, ForeignKey("corpus.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default='pending', index=True)  # 'pending', 'processing', 'completed', 'failed'
    annotation_type = Column(String(20))  # 'automatic', 'manual'，为空表示未选择
    current_version = Column(Integer, default=1)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    dataset = relationship("Dataset", back_populates="annotation_tasks")
    assignee = relationship("User", back_populates="annotation_tasks")
    text_entities = relationship("TextEntity", back_populates="task", cascade="all, delete-orphan")
    image_entities = relationship("ImageEntity", back_populates="task", cascade="all, delete-orphan")
    relations = relationship("Relation", back_populates="task", cascade="all, delete-orphan")
    review_tasks = relationship("ReviewTask", back_populates="task", cascade="all, delete-orphan")
    version_history = relationship("VersionHistory", back_populates="task", cascade="all, delete-orphan")


class TextEntity(Base):
    """文本实体表"""
    __tablename__ = "text_entities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(Integer, nullable=False)  # 实体在任务内的ID
    task_id = Column(Integer, ForeignKey("annotation_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(Integer, nullable=False, index=True)
    token = Column(Text, nullable=False)
    label = Column(String(50), nullable=False)
    start_offset = Column(Integer, nullable=False)
    end_offset = Column(Integer, nullable=False)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    task = relationship("AnnotationTask", back_populates="text_entities")


class ImageEntity(Base):
    """图片实体表"""
    __tablename__ = "image_entities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_id = Column(Integer, nullable=False)  # 实体在任务内的ID
    task_id = Column(Integer, ForeignKey("annotation_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    image_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer, nullable=False, index=True)
    label = Column(String(50), nullable=False)
    bbox_x = Column(Integer)
    bbox_y = Column(Integer)
    bbox_width = Column(Integer)
    bbox_height = Column(Integer)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    task = relationship("AnnotationTask", back_populates="image_entities")
    image = relationship("Image", back_populates="image_entities")


class Relation(Base):
    """关系表"""
    __tablename__ = "relations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    relation_id = Column(Integer, nullable=False)  # 关系在任务内的ID
    task_id = Column(Integer, ForeignKey("annotation_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(Integer, nullable=False, index=True)
    from_entity_id = Column(Integer, nullable=False)
    to_entity_id = Column(Integer, nullable=False)
    relation_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    task = relationship("AnnotationTask", back_populates="relations")


class EntityType(Base):
    """实体类型配置表"""
    __tablename__ = "entity_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), unique=True, nullable=False)
    type_name_zh = Column(String(50), nullable=False)
    color = Column(String(20), nullable=False)
    description = Column(Text)  # 简短描述
    definition = Column(Text)  # LLM生成的标准定义
    examples = Column(Text)  # LLM生成的示例（JSON格式存储列表）
    disambiguation = Column(Text)  # LLM生成的类别辨析
    prompt_template = Column(Text)  # 用于生成该实体类型的Prompt模板
    supports_bbox = Column(Boolean, default=False)  # 是否支持边界框（图片实体）
    is_active = Column(Boolean, default=True)
    is_reviewed = Column(Boolean, default=False)  # 是否已人工审核
    reviewed_by = Column(Integer, ForeignKey("users.id"))  # 审核人
    reviewed_at = Column(DateTime)  # 审核时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RelationType(Base):
    """关系类型配置表"""
    __tablename__ = "relation_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), unique=True, nullable=False)
    type_name_zh = Column(String(50), nullable=False)
    color = Column(String(20), nullable=False)
    description = Column(Text)  # 简短描述
    definition = Column(Text)  # LLM生成的标准定义
    direction_rule = Column(Text)  # LLM生成的方向规则
    examples = Column(Text)  # LLM生成的示例（JSON格式存储列表）
    disambiguation = Column(Text)  # LLM生成的类别辨析
    prompt_template = Column(Text)  # 用于生成该关系类型的Prompt模板
    is_active = Column(Boolean, default=True)
    is_reviewed = Column(Boolean, default=False)  # 是否已人工审核
    reviewed_by = Column(Integer, ForeignKey("users.id"))  # 审核人
    reviewed_at = Column(DateTime)  # 审核时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ReviewTask(Base):
    """复核任务表"""
    __tablename__ = "review_tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(String(100), unique=True, nullable=False, index=True)
    task_id = Column(Integer, ForeignKey("annotation_tasks.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default='pending')  # 'pending', 'approved', 'rejected'
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    review_comment = Column(Text)
    reviewed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    task = relationship("AnnotationTask", back_populates="review_tasks")


class VersionHistory(Base):
    """版本历史表"""
    __tablename__ = "version_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(String(100), unique=True, nullable=False, index=True)
    task_id = Column(Integer, ForeignKey("annotation_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    change_type = Column(String(20), nullable=False)  # 'create', 'update', 'delete'
    change_description = Column(Text)
    changed_by = Column(Integer, ForeignKey("users.id"))
    snapshot_data = Column(Text)  # JSON格式存储完整快照
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    task = relationship("AnnotationTask", back_populates="version_history")


class BatchJob(Base):
    """批量任务表"""
    __tablename__ = "batch_jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(100), unique=True, nullable=False, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default='pending')  # 'pending', 'processing', 'completed', 'completed_with_errors', 'failed', 'cancelled'
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    progress = Column(Float, default=0.0)  # 进度 0.0-1.0
    error_message = Column(Text)  # 错误信息
    created_by = Column(Integer, ForeignKey("users.id"))  # 创建人
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    dataset = relationship("Dataset", back_populates="batch_jobs")
    creator = relationship("User", foreign_keys=[created_by])


class LabelSchemaVersion(Base):
    """标签体系版本表"""
    __tablename__ = "label_schema_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(String(100), unique=True, nullable=False, index=True)
    version_name = Column(String(255), nullable=False)  # 如: "品质失效v1.0", "供应链风险v1.0"
    description = Column(Text)
    schema_data = Column(Text, nullable=False)  # JSON格式存储完整的标签配置快照
    is_active = Column(Boolean, default=False)  # 是否为当前活跃版本
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    datasets = relationship("Dataset", back_populates="label_schema_version")


# ============================================
# KF/QMS 处理器相关模型
# ============================================

class Customer(Base):
    """客户表（KF和QMS共用）"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # 关系
    quick_response_events = relationship("QuickResponseEvent", back_populates="customer")
    qms_defect_orders = relationship("QMSDefectOrder", back_populates="customer")


class Product(Base):
    """产品型号表"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(255), unique=True, nullable=False)
    product_category = Column(String(255))
    industry_category = Column(String(255))

    # 关系
    quick_response_events = relationship("QuickResponseEvent", back_populates="product")


class Defect(Base):
    """缺陷类型表（KF和QMS共用）"""
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # 关系
    quick_response_events = relationship("QuickResponseEvent", back_populates="defect")
    qms_defect_orders = relationship("QMSDefectOrder", back_populates="defect")


class RootCause(Base):
    """异常原因表"""
    __tablename__ = "root_causes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(255))
    process_category = Column(String(255))

    # 关系
    quick_response_events = relationship("QuickResponseEvent", back_populates="root_cause")


class FourMElement(Base):
    """4M要素表"""
    __tablename__ = "four_m_elements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    element = Column(String(255), unique=True, nullable=False)

    # 关系
    quick_response_events = relationship("QuickResponseEvent", back_populates="four_m_element")


class QuickResponseEvent(Base):
    """快反事件表"""
    __tablename__ = "quick_response_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(100), nullable=True)  # 快反编号，非唯一，同一编号可对应多条记录
    content_hash = Column(String(64), unique=True, nullable=True)  # 整行内容哈希，唯一约束，作为去重依据
    occurrence_time = Column(DateTime)
    problem_analysis = Column(Text)
    short_term_measure = Column(Text)
    long_term_measure = Column(Text)
    images = Column(Text)
    data_source = Column(String(255))
    classification = Column(String(255))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    defect_id = Column(Integer, ForeignKey("defects.id"))
    root_cause_id = Column(Integer, ForeignKey("root_causes.id"))
    four_m_id = Column(Integer, ForeignKey("four_m_elements.id"))

    # 关系
    customer = relationship("Customer", back_populates="quick_response_events")
    product = relationship("Product", back_populates="quick_response_events")
    defect = relationship("Defect", back_populates="quick_response_events")
    root_cause = relationship("RootCause", back_populates="quick_response_events")
    four_m_element = relationship("FourMElement", back_populates="quick_response_events")


class QMSWorkshop(Base):
    """QMS车间表"""
    __tablename__ = "qms_workshops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # 关系
    production_lines = relationship("QMSProductionLine", back_populates="workshop")
    defect_orders = relationship("QMSDefectOrder", back_populates="workshop")


class QMSProductionLine(Base):
    """QMS产线表"""
    __tablename__ = "qms_production_lines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    workshop_id = Column(Integer, ForeignKey("qms_workshops.id"))

    # 唯一约束
    __table_args__ = (UniqueConstraint('name', 'workshop_id', name='uix_line_name_workshop'),)

    # 关系
    workshop = relationship("QMSWorkshop", back_populates="production_lines")
    defect_orders = relationship("QMSDefectOrder", back_populates="production_line")


class QMSStation(Base):
    """QMS岗位表"""
    __tablename__ = "qms_stations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # 关系
    defect_orders = relationship("QMSDefectOrder", back_populates="station")


class QMSInspectionNode(Base):
    """QMS质检节点表"""
    __tablename__ = "qms_inspection_nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # 关系
    defect_orders = relationship("QMSDefectOrder", back_populates="inspection_node")


class QMSDefectOrder(Base):
    """QMS不合格品记录表"""
    __tablename__ = "qms_defect_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(100), nullable=True)  # 制令单号，非唯一，同一单号可对应多条缺陷记录
    content_hash = Column(String(64), unique=True, nullable=True)  # 全行内容哈希，唯一约束，用于去重
    entry_time = Column(String(255))
    model = Column(String(255))
    barcode = Column(String(255))
    position = Column(String(255))
    photo_path = Column(Text)
    status = Column(String(255))
    data_source = Column(String(255))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    workshop_id = Column(Integer, ForeignKey("qms_workshops.id"))
    line_id = Column(Integer, ForeignKey("qms_production_lines.id"))
    station_id = Column(Integer, ForeignKey("qms_stations.id"))
    defect_id = Column(Integer, ForeignKey("defects.id"))
    inspection_node_id = Column(Integer, ForeignKey("qms_inspection_nodes.id"))

    # 关系
    customer = relationship("Customer", back_populates="qms_defect_orders")
    workshop = relationship("QMSWorkshop", back_populates="defect_orders")
    production_line = relationship("QMSProductionLine", back_populates="defect_orders")
    station = relationship("QMSStation", back_populates="defect_orders")
    defect = relationship("Defect", back_populates="qms_defect_orders")
    inspection_node = relationship("QMSInspectionNode", back_populates="defect_orders")
