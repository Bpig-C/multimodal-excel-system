/**
 * 标注任务API
 */
import { request } from './request'

export interface BatchAnnotationRequest {
  dataset_id: string
  task_ids?: string[]  // 可选：指定要标注的任务ID列表
}

export interface BatchJobResponse {
  job_id: string
  dataset_id: string
  status: string
  total_tasks: number
}

export interface BatchJobStats {
  job_id: string
  dataset_id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  total_tasks: number
  completed_tasks: number
  failed_tasks: number
  processing_tasks: number
  started_at?: string
  completed_at?: string
}

export const annotationApi = {
  /**
   * 获取任务列表（跨数据集）
   */
  getTaskList(params?: {
    dataset_id?: string
    status?: string
    page?: number
    page_size?: number
    sort_by?: string
    sort_order?: string
  }) {
    return request.get('/annotations', { params })
  },

  /**
   * 触发批量自动标注
   */
  triggerBatchAnnotation(data: BatchAnnotationRequest) {
    return request.post<{ data: BatchJobResponse }>('/annotations/batch', data)
  },

  /**
   * 获取批量任务状态
   */
  getBatchJobStatus(jobId: string) {
    return request.get<{ data: BatchJobStats }>(`/annotations/batch/${jobId}`)
  },

  /**
   * 取消批量任务
   */
  cancelBatchJob(jobId: string) {
    return request.post(`/annotations/batch/${jobId}/cancel`)
  },

  /**
   * 获取标注任务详情
   */
  getAnnotationTask(taskId: string) {
    return request.get(`/annotations/${taskId}`)
  },

  /**
   * 更新标注任务
   */
  updateAnnotationTask(taskId: string, data: any) {
    return request.put(`/annotations/${taskId}`, data)
  },

  /**
   * 添加文本实体
   */
  addTextEntity(taskId: string, data: any) {
    return request.post(`/annotations/${taskId}/entities`, data)
  },

  /**
   * 更新文本实体
   */
  updateTextEntity(taskId: string, entityId: number, data: any) {
    return request.put(`/annotations/${taskId}/entities/${entityId}`, data)
  },

  /**
   * 删除文本实体
   */
  deleteTextEntity(taskId: string, entityId: number) {
    return request.delete(`/annotations/${taskId}/entities/${entityId}`)
  },

  /**
   * 添加关系
   */
  addRelation(taskId: string, data: any) {
    return request.post(`/annotations/${taskId}/relations`, data)
  },

  /**
   * 更新关系
   */
  updateRelation(taskId: string, relationId: number, data: any) {
    return request.put(`/annotations/${taskId}/relations/${relationId}`, data)
  },

  /**
   * 删除关系
   */
  deleteRelation(taskId: string, relationId: number) {
    return request.delete(`/annotations/${taskId}/relations/${relationId}`)
  }
}
