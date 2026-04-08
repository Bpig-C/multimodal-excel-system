/**
 * 文档管理 API - KF/QMS 文档上传、处理和导出
 */
import type { AxiosProgressEvent } from 'axios'
import { request } from './request'
import type {
  ProcessorInfo,
  ProcessedFile,
  UploadResult,
  ImportResult,
  ExportResult,
  ExportFormat,
  BatchExportParams,
  StatisticsData
} from '@/types'

// 本文件内部使用的响应包装类型（不在全局 types 中）
export interface ProcessedFilesResult {
  success: boolean
  files: ProcessedFile[]
  total: number
}

export interface ProcessorListResult {
  processors: ProcessorInfo[]
}

export interface FieldMappingResult {
  processor: string
  display_name: string
  field_mapping: Record<string, string>
}

export interface StatisticsResult {
  success: boolean
  data: StatisticsData
  processor: string
}

export interface DataListResult {
  success: boolean
  data: any[]
  count: number
  total_count?: number
  page?: number
  page_size?: number
  processor: string
}

export interface TransferProgress {
  loaded: number
  total?: number
  percentage: number
}

export interface TransferProgressOptions {
  onUploadProgress?: (progress: TransferProgress) => void
  onDownloadProgress?: (progress: TransferProgress) => void
}

// Re-export shared types so consumers can import from one place
export type { ProcessorInfo, ProcessedFile, UploadResult, ImportResult, ExportResult, ExportFormat, BatchExportParams, StatisticsData }

// ============ API函数 ============

const toTransferProgress = (event: AxiosProgressEvent): TransferProgress => {
  const total = typeof event.total === 'number' && event.total > 0 ? event.total : undefined

  return {
    loaded: event.loaded,
    total,
    percentage: total ? Math.min(100, Math.round((event.loaded / total) * 100)) : 0
  }
}

export const documentApi = {
  /**
   * 上传Excel文件
   */
  uploadExcel(file: File, processorName: string, options?: TransferProgressOptions): Promise<UploadResult> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('processor_name', processorName)
    return request.upload<UploadResult>('/documents/upload', formData, {
      onUploadProgress: options?.onUploadProgress
        ? (event) => options.onUploadProgress?.(toTransferProgress(event))
        : undefined
    })
  },

  /**
   * 导入JSON数据
   */
  importJsonData(processorName: string, dataSource: string): Promise<ImportResult> {
    const formData = new FormData()
    formData.append('processor_name', processorName)
    formData.append('data_source', dataSource)
    return request.upload<ImportResult>('/documents/import', formData)
  },

  /**
   * 上传图片ZIP包
   */
  uploadImagesZip(file: File, dataSource: string, processorName: string, options?: TransferProgressOptions): Promise<any> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('data_source', dataSource)
    formData.append('processor_name', processorName)
    return request.upload<any>('/documents/images', formData, {
      onUploadProgress: options?.onUploadProgress
        ? (event) => options.onUploadProgress?.(toTransferProgress(event))
        : undefined
    })
  },

  /**
   * 查询指定数据源已上传图片数量
   */
  getImagesInfo(dataSource: string): Promise<any> {
    return request.get<any>('/documents/images', { params: { data_source: dataSource } })
  },

  /**
   * 删除已处理文件
   */
  deleteProcessedFile(processorName: string, dataSource: string): Promise<any> {
    return request.delete<any>('/documents/processed-files', {
      params: { processor_name: processorName, data_source: dataSource }
    })
  },

  /**
   * 获取已处理文件列表
   */
  getProcessedFiles(processorName: string): Promise<ProcessedFilesResult> {
    return request.get<ProcessedFilesResult>('/documents/processed-files', {
      params: { processor_name: processorName }
    })
  },

  /**
   * 获取处理器列表
   */
  getProcessors(): Promise<ProcessorListResult> {
    return request.get<ProcessorListResult>('/config/processors')
  },

  /**
   * 获取字段映射
   */
  getFieldMapping(processorName: string): Promise<FieldMappingResult> {
    return request.get<FieldMappingResult>(`/config/processors/${processorName}/field-mapping`)
  },

  /**
   * 获取数据列表
   */
  getDataList(
    processorName: string,
    params?: { page?: number; page_size?: number; limit?: number; offset?: number }
  ): Promise<DataListResult> {
    return request.get<DataListResult>('/data/list', {
      params: { processor_name: processorName, ...params }
    })
  },

  /**
   * 获取统计数据
   */
  getStatistics(processorName: string): Promise<StatisticsResult> {
    return request.get<StatisticsResult>('/data/statistics', {
      params: { processor_name: processorName }
    })
  },

  /**
   * 导出实体文本格式
   */
  exportEntityText(processorName: string, dataSources?: string[]): Promise<ExportResult> {
    return request.post<ExportResult>(`/export/corpus/${processorName}/entity-text`, {
      data_sources: dataSources
    })
  },

  /**
   * 导出CLIP对齐格式
   */
  exportClipAlignment(processorName: string, dataSources?: string[]): Promise<ExportResult> {
    return request.post<ExportResult>(`/export/corpus/${processorName}/clip-alignment`, {
      data_sources: dataSources
    })
  },

  /**
   * 导出QA对齐格式
   */
  exportQaAlignment(processorName: string, dataSources?: string[]): Promise<ExportResult> {
    return request.post<ExportResult>(`/export/corpus/${processorName}/qa-alignment`, {
      data_sources: dataSources
    })
  },

  /**
   * 批量导出（返回ZIP文件流）
   */
  batchExport(processorName: string, params: BatchExportParams, options?: TransferProgressOptions): Promise<Blob> {
    return request.post<Blob>(`/export/corpus/${processorName}/batch`, params, {
      responseType: 'blob',
      timeout: 300000, // 大文件导出单独设 5 分钟超时
      onDownloadProgress: options?.onDownloadProgress
        ? (event) => options.onDownloadProgress?.(toTransferProgress(event))
        : undefined
    } as any)
  }
}
