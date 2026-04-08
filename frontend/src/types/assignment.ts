/**
 * 数据集分配相关类型定义
 * Task 47: 数据集级别任务分配功能
 */

/**
 * 分配模式
 */
export type AssignmentMode = 'full' | 'range'

/**
 * 转移模式
 */
export type TransferMode = 'all' | 'remaining' | 'completed'

/**
 * 分配角色
 */
export type AssignmentRole = 'annotator' | 'reviewer'

/**
 * 分配请求
 */
export interface AssignmentRequest {
  user_id: number
  role: AssignmentRole
  mode: AssignmentMode
  start_index?: number
  end_index?: number
}

/**
 * 自动分配请求
 */
export interface AutoAssignmentRequest {
  user_ids: number[]
  role: AssignmentRole
}

/**
 * 转移分配请求
 */
export interface TransferAssignmentRequest {
  old_user_id: number
  new_user_id: number
  role: AssignmentRole
  transfer_mode: TransferMode
  transfer_reason?: string
}

/**
 * 分配信息
 */
export interface AssignmentInfo {
  assignment_id: number
  dataset_id: string
  user_id: number
  username: string
  role: string
  task_range: string | null
  task_count: number
  completed_count: number
  in_review_count: number
  is_active: boolean
  transferred_to?: number
  transferred_to_username?: string
  transferred_at?: string
  transfer_reason?: string
  assigned_by?: number
  assigned_at: string
}

/**
 * 自动分配信息
 */
export interface AutoAssignmentInfo {
  user_id: number
  username: string
  task_range: string
  task_count: number
}

/**
 * 我的数据集信息
 */
export interface MyDatasetInfo {
  dataset_id: string
  name: string
  description?: string
  my_role: string
  my_task_range: string | null
  my_task_count: number
  my_completed_count: number
  total_tasks: number
  assigned_at: string
}

/**
 * 分配列表数据
 */
export interface AssignmentListData {
  dataset_id: string
  dataset_name: string
  total_tasks: number
  assignments: AssignmentInfo[]
  unassigned_count: number
  annotator_count: number
  reviewer_count: number
}

/**
 * 我的数据集列表数据
 */
export interface MyDatasetsData {
  items: MyDatasetInfo[]
  total: number
  page: number
  page_size: number
}

/**
 * 转移结果
 */
export interface TransferResult {
  old_assignment_id: number
  new_assignment_id: number
  old_user: {
    id: number
    username: string
  }
  new_user: {
    id: number
    username: string
  }
  transferred_tasks: number
  transfer_mode: string
  transferred_at: string
}

/**
 * 取消分配检查结果
 */
export interface CancelCheckResult {
  can_cancel: boolean
  reason: string
  stats: {
    total_tasks: number
    completed_count: number
    in_review_count: number
    processing_count: number
    pending_count: number
  }
  action?: string
}
