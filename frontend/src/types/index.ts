// ==================== 用户相关 ====================

export interface User {
  id: number
  username: string
  role: 'admin' | 'annotator' | 'reviewer' | 'viewer'
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

// ==================== 语料相关 ====================

export interface Corpus {
  id?: number  // 数据库ID（可选，因为API返回的是text_id）
  text_id: string
  text: string
  text_type: string  // 句子分类：问题描述、原因分析、采取措施等
  source_file: string
  source_row: number
  source_field: string
  has_images: boolean
  images?: Image[]
  created_at: string
}

export interface Image {
  id?: number  // 数据库ID（可选）
  image_id: string
  corpus_id?: number
  file_path: string
  original_name: string
  width: number
  height: number
}

// ==================== 数据集相关 ====================

export interface Dataset {
  id: number
  dataset_id: string
  name: string
  description: string
  label_schema_version_id?: number
  created_by: number
  created_at: string
  updated_at: string
  statistics?: DatasetStatistics
}

export interface DatasetStatistics {
  total_tasks: number
  completed_tasks: number
  reviewed_tasks: number
  pending_tasks: number
}

export type DatasetStatus = 'empty' | 'in_progress' | 'completed'

// ==================== 标注任务相关 ====================

export interface AnnotationTask {
  id: number
  task_id: string
  dataset_id: number
  corpus_id: number
  corpus: Corpus
  status: TaskStatus
  annotation_type: AnnotationType | null
  assigned_to: number
  current_version: number
  text_entities: TextEntity[]
  image_entities: ImageEntity[]
  relations: Relation[]
  created_at: string
  updated_at: string
}

export interface TaskListItem {
  id: number
  task_id: string
  dataset_id: string
  dataset_name: string
  corpus_id: number
  corpus_text: string
  status: TaskStatus
  annotation_type: AnnotationType | null
  entity_count: number
  relation_count: number
  current_version: number
  created_at: string
  updated_at: string
}

export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'reviewed'
export type AnnotationType = 'automatic' | 'manual'

// ==================== 实体相关 ====================

export interface TextEntity {
  id: number
  entity_id: string  // 任务内唯一ID (字符串格式: entity-xxx)
  task_id: number
  version: number
  token: string
  label: string
  start_offset: number
  end_offset: number
  confidence?: number
}

export interface ImageEntity {
  id: number
  entity_id: string
  image_id: number
  task_id: number
  version: number
  label: string
  annotation_type: 'whole_image' | 'region'
  bbox?: BoundingBox
  confidence?: number
}

export interface BoundingBox {
  x: number
  y: number
  width: number
  height: number
}

// ==================== 关系相关 ====================

export interface Relation {
  id: number
  relation_id: string  // 任务内唯一ID (字符串格式: relation-xxx)
  task_id: number
  version: number
  from_entity_id: string  // 字符串格式的entity_id
  to_entity_id: string    // 字符串格式的entity_id
  relation_type: string
}

// ==================== 标签配置相关 ====================

export interface EntityType {
  id: number
  type_name: string
  type_name_zh: string
  color: string
  description?: string
  definition?: string  // LLM生成的标准定义
  examples?: string[]  // LLM生成的示例
  disambiguation?: string  // LLM生成的辨析
  is_active: boolean
  is_reviewed: boolean  // 是否已审核
  reviewed_by?: number
  reviewed_at?: string
}

export interface RelationType {
  id: number
  type_name: string
  type_name_zh: string
  color: string
  description?: string
  definition?: string  // LLM生成的标准定义
  direction_rule?: string  // LLM生成的方向规则
  examples?: string[]  // LLM生成的示例
  disambiguation?: string  // LLM生成的辨析
  is_active: boolean
  is_reviewed: boolean
  reviewed_by?: number
  reviewed_at?: string
}

export interface LabelSchema {
  entity_types: EntityType[]
  relation_types: RelationType[]
}

// 标签体系版本
export interface LabelSchemaVersion {
  id: number
  version_id: string
  version_name: string
  description: string
  is_active: boolean
  entity_types: EntityType[]
  relation_types: RelationType[]
  created_by: number
  created_at: string
}

// ==================== 批量任务相关 ====================

export interface BatchJob {
  id: number
  job_id: string
  dataset_id: number
  status: BatchJobStatus
  total_tasks: number
  completed_tasks: number
  failed_tasks: number
  started_at?: string
  completed_at?: string
  created_at: string
}

export type BatchJobStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'

export interface BatchJobProgress {
  job_id: string
  status: BatchJobStatus
  progress: {
    total: number
    completed: number
    failed: number
  }
  started_at?: string
  completed_at?: string
}

// ==================== 复核相关 ====================

export interface ReviewTask {
  id: number
  review_id: string
  task_id: number
  task: AnnotationTask
  status: ReviewStatus
  reviewer_id?: number
  review_comment?: string
  reviewed_at?: string
  created_at: string
}

export type ReviewStatus = 'pending' | 'approved' | 'rejected'

export interface ReviewStatistics {
  total_reviews: number
  approved: number
  rejected: number
  pending: number
  approval_rate: number
  avg_review_time: number
}

// ==================== 版本管理相关 ====================

export interface Version {
  id: number
  history_id: string
  task_id: number
  version: number
  change_type: ChangeType
  change_description?: string
  changed_by: number
  snapshot_data: VersionSnapshot
  created_at: string
}

export type ChangeType = 'create' | 'update' | 'delete'

export interface VersionSnapshot {
  text_entities: TextEntity[]
  image_entities: ImageEntity[]
  relations: Relation[]
}

export interface VersionDiff {
  added_entities: TextEntity[]
  removed_entities: TextEntity[]
  modified_entities: Array<{
    old: TextEntity
    new: TextEntity
  }>
  added_relations: Relation[]
  removed_relations: Relation[]
  modified_relations: Array<{
    old: Relation
    new: Relation
  }>
}

// ==================== API响应相关 ====================

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface ErrorResponse {
  detail: string
}

// ==================== 文档管理模块类型 ====================

export interface ProcessorInfo {
  name: string
  display_name: string
}

export interface ProcessedFile {
  filename: string
  data_source: string
  table_count: number
  processed_time: string
  output_dir: string
}

export interface UploadResult {
  success: boolean
  is_duplicate: boolean
  message: string
  data_source?: string
  table_count?: number
  image_count?: number
  corpus_count?: number
}

export interface ImportResult {
  success: boolean
  message: string
  total_records: number
  inserted_records: number
  skipped_records: number
}

export interface ExportResult {
  success: boolean
  data: any[]
  count: number
}

export type ExportFormat = 'entity_text' | 'clip_alignment' | 'qa_alignment'

export interface BatchExportParams {
  data_sources?: string[]
  formats: ExportFormat[]
  include_images?: boolean
}

export interface StatisticsData {
  total_events: number
  defect_distribution: { name: string; count: number }[]
  customer_ranking: { name: string; count: number }[]
  four_m_distribution?: { element: string; count: number }[]
  workshop_distribution?: { name: string; count: number }[]
  line_distribution?: { name: string; count: number }[]
  inspection_node_distribution?: { name: string; count: number }[]
  status_distribution?: { status: string; count: number }[]
}
