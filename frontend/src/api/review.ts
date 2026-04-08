/**
 * 复核管理API
 */
import { request } from './request'
import type { ReviewTask, ReviewStatistics, PaginatedResponse } from '@/types'

export const reviewApi = {
  /**
   * 提交复核
   */
  submit(taskId: string, reviewerId?: number) {
    return request.post<{ data: { review_id: string } }>(`/review/submit/${taskId}`, {
      reviewer_id: reviewerId
    })
  },

  /**
   * 获取复核任务列表
   */
  list(params?: {
    page?: number
    page_size?: number
    status?: string
    reviewer_id?: number
    skip?: number
    limit?: number
  }) {
    // 转换参数格式
    const queryParams: any = {}
    if (params?.status) queryParams.status = params.status
    if (params?.reviewer_id) queryParams.reviewer_id = params.reviewer_id
    if (params?.skip !== undefined) queryParams.skip = params.skip
    if (params?.limit !== undefined) queryParams.limit = params.limit
    
    return request.get<any>('/review/tasks', { params: queryParams })
  },

  /**
   * 获取复核任务详情
   */
  get(reviewId: string) {
    return request.get<any>(`/review/${reviewId}`)
  },

  /**
   * 批准任务
   */
  approve(reviewId: string, data?: {
    reviewer_id?: number
    review_comment?: string
  }) {
    return request.post(`/review/${reviewId}/approve`, {
      reviewer_id: data?.reviewer_id || 1, // 临时使用固定ID
      review_comment: data?.review_comment || ''
    })
  },

  /**
   * 驳回任务
   */
  reject(reviewId: string, data: {
    reviewer_id?: number
    comment: string
    suggestions?: string
  }) {
    return request.post(`/review/${reviewId}/reject`, {
      reviewer_id: data.reviewer_id || 1, // 临时使用固定ID
      review_comment: data.comment
    })
  },

  /**
   * 获取数据集质量统计
   */
  getStatistics(datasetId: number) {
    return request.get<ReviewStatistics>(`/review/dataset/${datasetId}/statistics`)
  },

  /**
   * 获取数据集复核摘要
   */
  getSummary(datasetId: number) {
    return request.get(`/review/dataset/${datasetId}/summary`)
  }
}
