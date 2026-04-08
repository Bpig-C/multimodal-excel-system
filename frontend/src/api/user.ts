/**
 * 用户管理API
 */
import { request } from './request'
import type { User, PaginatedResponse } from '@/types'

export const userApi = {
  /**
   * 创建用户
   */
  create(data: {
    username: string
    password: string
    role: 'admin' | 'annotator' | 'viewer'
  }) {
    return request.post<User>('/users', data)
  },

  /**
   * 获取用户列表
   */
  list(params?: {
    role?: string
    skip?: number
    limit?: number
  }) {
    return request.get<User[]>('/users', { params })
  },

  /**
   * 获取用户详情
   */
  get(id: number) {
    return request.get<User>(`/users/${id}`)
  },

  /**
   * 更新用户
   */
  update(id: number, data: {
    username?: string
    password?: string
    role?: 'admin' | 'annotator' | 'viewer'
  }) {
    return request.put<User>(`/users/${id}`, data)
  },

  /**
   * 删除用户
   */
  delete(id: number) {
    return request.delete(`/users/${id}`)
  },

  /**
   * 获取用户统计
   */
  getStatistics(id: number) {
    return request.get(`/users/${id}/statistics`)
  }
}
