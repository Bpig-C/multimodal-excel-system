/**
 * 任务状态常量和工具函数
 * 统一管理任务状态的显示和颜色
 */

// 任务状态枚举
export enum TaskStatus {
  PENDING = 'pending',           // 待处理
  PROCESSING = 'processing',     // 处理中
  COMPLETED = 'completed',       // 已完成
  UNDER_REVIEW = 'under_review', // 待复核
  APPROVED = 'approved',         // 已批准
  REJECTED = 'rejected',         // 已驳回
  FAILED = 'failed'              // 失败
}

// 状态显示文本映射
export const STATUS_TEXT_MAP: Record<string, string> = {
  [TaskStatus.PENDING]: '待处理',
  [TaskStatus.PROCESSING]: '处理中',
  [TaskStatus.COMPLETED]: '已完成',
  [TaskStatus.UNDER_REVIEW]: '待复核',
  [TaskStatus.APPROVED]: '已批准',
  [TaskStatus.REJECTED]: '已驳回',
  [TaskStatus.FAILED]: '失败'
}

// 状态标签类型映射（Element Plus Tag 类型）
export const STATUS_TYPE_MAP: Record<string, string> = {
  [TaskStatus.PENDING]: 'info',
  [TaskStatus.PROCESSING]: 'warning',
  [TaskStatus.COMPLETED]: 'success',
  [TaskStatus.UNDER_REVIEW]: '',
  [TaskStatus.APPROVED]: 'primary',
  [TaskStatus.REJECTED]: 'danger',
  [TaskStatus.FAILED]: 'danger'
}

// 状态选项（用于下拉框）
export const STATUS_OPTIONS = [
  { label: '待处理', value: TaskStatus.PENDING },
  { label: '处理中', value: TaskStatus.PROCESSING },
  { label: '已完成', value: TaskStatus.COMPLETED },
  { label: '待复核', value: TaskStatus.UNDER_REVIEW },
  { label: '已批准', value: TaskStatus.APPROVED },
  { label: '已驳回', value: TaskStatus.REJECTED },
  { label: '失败', value: TaskStatus.FAILED }
]

/**
 * 获取状态显示文本
 * @param status 状态值
 * @returns 显示文本
 */
export function getStatusText(status: string): string {
  return STATUS_TEXT_MAP[status] || status
}

/**
 * 获取状态标签类型
 * @param status 状态值
 * @returns Element Plus Tag 类型
 */
export function getStatusType(status: string): string {
  return STATUS_TYPE_MAP[status] || 'info'
}

/**
 * 检查状态是否为最终状态（不可再编辑）
 * @param status 状态值
 * @returns 是否为最终状态
 */
export function isFinalStatus(status: string): boolean {
  return [
    TaskStatus.APPROVED,
    TaskStatus.REJECTED,
    TaskStatus.FAILED
  ].includes(status as TaskStatus)
}

/**
 * 检查状态是否可以提交复核
 * @param status 状态值
 * @returns 是否可以提交复核
 */
export function canSubmitForReview(status: string): boolean {
  return status === TaskStatus.COMPLETED
}

/**
 * 检查状态是否可以编辑
 * @param status 状态值
 * @returns 是否可以编辑
 */
export function canEdit(status: string): boolean {
  return ![
    TaskStatus.UNDER_REVIEW,
    TaskStatus.APPROVED
  ].includes(status as TaskStatus)
}
