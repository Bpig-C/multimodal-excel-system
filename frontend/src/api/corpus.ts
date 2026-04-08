/**
 * 语料管理API
 */
import { request } from './request'
import type { Corpus, PaginatedResponse } from '@/types'

// Excel上传响应
export interface ExcelUploadResponse {
  success: boolean
  message: string
  total_records: number
  total_sentences: number
  total_images: number
  field_distribution: Record<string, number>
}

export const corpusApi = {
  /**
   * 上传Excel文件
   */
  upload(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return request.upload<ExcelUploadResponse>('/corpus/upload', formData)
  },

  /**
   * 获取语料列表
   */
  list(params?: {
    page?: number
    page_size?: number
    source_file?: string
    source_field?: string  // 修改为 source_field 以匹配后端
    has_images?: boolean
  }) {
    return request.get<PaginatedResponse<Corpus>>('/corpus', { params })
  },

  /**
   * 获取语料详情
   */
  get(id: number) {
    return request.get<Corpus>(`/corpus/${id}`)
  },

  /**
   * 删除语料（使用text_id）
   */
  delete(textId: string) {
    return request.delete(`/corpus/${textId}`)
  },

  /**
   * 获取语料关联图片
   */
  getImages(id: number) {
    return request.get(`/corpus/${id}/images`)
  }
}
