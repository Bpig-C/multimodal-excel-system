/**
 * 图片标注API
 */
import { request } from './request'
import type { ImageEntity } from '@/types'

export const imageApi = {
  /**
   * 添加图片实体
   */
  addEntity(imageId: number, data: {
    label: string
    annotation_type: 'whole_image' | 'region'
    bbox?: {
      x: number
      y: number
      width: number
      height: number
    }
  }) {
    return request.post<ImageEntity>(`/images/${imageId}/entities`, data)
  },

  /**
   * 获取图片实体列表
   */
  getEntities(imageId: number) {
    return request.get<ImageEntity[]>(`/images/${imageId}/entities`)
  },

  /**
   * 更新图片实体
   */
  updateEntity(imageId: number, entityId: number, data: {
    label?: string
    annotation_type?: 'whole_image' | 'region'
    bbox?: {
      x: number
      y: number
      width: number
      height: number
    }
  }) {
    return request.put<ImageEntity>(`/images/${imageId}/entities/${entityId}`, data)
  },

  /**
   * 删除图片实体
   */
  deleteEntity(imageId: number, entityId: number) {
    return request.delete(`/images/${imageId}/entities/${entityId}`)
  }
}
