/**
 * 版本管理API
 */
import { request } from './request'
import type { Version, VersionDiff } from '@/types'

export const versionApi = {
  /**
   * 获取版本历史
   */
  getHistory(taskId: string) {
    return request.get<Version[]>(`/versions/${taskId}`)
  },

  /**
   * 回滚版本
   */
  rollback(taskId: string, data: {
    version: number
  }) {
    return request.post(`/versions/${taskId}/rollback`, data)
  },

  /**
   * 比较版本差异
   */
  compare(params: {
    task_id: string
    version_1: number
    version_2: number
  }) {
    return request.get<VersionDiff>('/versions/compare', { params })
  },

  /**
   * 获取版本详情
   */
  get(taskId: string, version: number) {
    return request.get<Version>(`/versions/${taskId}/${version}`)
  },

  /**
   * 创建版本快照
   */
  createSnapshot(taskId: string, data?: {
    comment?: string
  }) {
    return request.post(`/versions/${taskId}/snapshot`, data)
  }
}
