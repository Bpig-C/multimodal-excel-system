/**
 * 数据集管理API
 */
import { request } from './request'
import type { Dataset, PaginatedResponse } from '@/types'
import type {
  AssignmentRequest,
  AutoAssignmentRequest,
  TransferAssignmentRequest,
  AssignmentInfo,
  AutoAssignmentInfo,
  MyDatasetInfo,
  AssignmentListData,
  MyDatasetsData,
  TransferResult
} from '@/types/assignment'

export const datasetApi = {
  /**
   * 创建数据集
   */
  create(data: {
    name: string
    description?: string
    corpus_ids: number[]
    created_by: number
    label_schema_version_id?: number
  }) {
    return request.post<{ dataset_id: string }>('/datasets', data)
  },

  /**
   * 获取数据集列表
   */
  list(params?: {
    page?: number
    page_size?: number
    created_by?: number
  }) {
    return request.get<PaginatedResponse<Dataset>>('/datasets', { params })
  },

  /**
   * 获取数据集详情
   */
  get(id: string | number) {
    return request.get<Dataset>(`/datasets/${id}`)
  },

  /**
   * 更新数据集
   */
  update(id: number, data: {
    name?: string
    description?: string
    label_schema_version_id?: number
  }) {
    return request.put<Dataset>(`/datasets/${id}`, data)
  },

  /**
   * 删除数据集
   */
  delete(datasetId: string) {
    return request.delete(`/datasets/${datasetId}`)
  },

  /**
   * 导出数据集
   */
  export(datasetId: string, params?: {
    output_path?: string
    status_filter?: string[]
  }) {
    return request.post(`/datasets/${datasetId}/export`, params || {})
  },

  /**
   * 获取数据集的任务列表
   */
  getTasks(datasetId: string, params?: {
    page?: number
    page_size?: number
    status?: string
  }) {
    return request.get<PaginatedResponse<any>>(`/datasets/${datasetId}/tasks`, { params })
  },

  /**
   * 向数据集添加语料（创建新任务，自动去重）
   */
  addTasks(datasetId: string, corpusIds: number[]) {
    return request.post<{ added: number; skipped: number }>(
      `/datasets/${datasetId}/tasks`,
      { corpus_ids: corpusIds }
    )
  },

  /**
   * 从数据集删除一个任务（级联删除实体/关系）
   */
  removeTask(datasetId: string, taskId: string) {
    return request.delete(`/datasets/${datasetId}/tasks/${taskId}`)
  },

  // ============================================================================
  // 数据集分配相关API (Task 47)
  // ============================================================================

  /**
   * 分配数据集（整体或范围）
   */
  assign(datasetId: string, data: AssignmentRequest) {
    return request.post<AssignmentInfo>(`/datasets/${datasetId}/assign`, data)
  },

  /**
   * 自动平均分配数据集
   */
  autoAssign(datasetId: string, data: AutoAssignmentRequest) {
    return request.post<{
      assignments: AutoAssignmentInfo[]
      total_tasks: number
    }>(`/datasets/${datasetId}/assign/auto`, data)
  },

  /**
   * 批量分配
   */
  batchAssign(datasetId: string, data: {
    assignments: Array<{
      user_id: number
      role: string
      mode: string
      start_index?: number
      end_index?: number
    }>
    clear_existing: boolean
    role_filter?: string
  }) {
    return request.post(`/datasets/${datasetId}/assignments/batch`, data)
  },

  /**
   * 取消分配
   */
  cancelAssignment(datasetId: string, userId: number, role: string, force: boolean = false) {
    return request.delete(`/datasets/${datasetId}/assign/${userId}`, {
      params: { role, force }
    })
  },

  /**
   * 批量清空分配
   */
  clearAssignments(datasetId: string, role?: string, force: boolean = false) {
    return request.delete(`/datasets/${datasetId}/assignments/clear`, {
      params: { role, force }
    })
  },

  /**
   * 转移分配
   */
  transferAssignment(datasetId: string, data: TransferAssignmentRequest) {
    return request.post<TransferResult>(`/datasets/${datasetId}/assign/transfer`, data)
  },

  /**
   * 获取数据集分配情况
   */
  getAssignments(datasetId: string, includeInactive: boolean = false) {
    return request.get<AssignmentListData>(`/datasets/${datasetId}/assignments`, {
      params: { include_inactive: includeInactive }
    })
  },

  /**
   * 获取我的数据集
   */
  getMyDatasets(params?: {
    role?: string
    page?: number
    page_size?: number
  }) {
    return request.get<MyDatasetsData>('/datasets/my', { params })
  }
}
