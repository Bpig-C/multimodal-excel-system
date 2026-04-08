import { defineStore } from 'pinia'
import { ref } from 'vue'
import { documentApi } from '@/api/document'
import type { TransferProgress } from '@/api/document'
import type { BatchExportParams, ProcessorInfo, ProcessedFile, StatisticsData } from '@/types'

type TransferPhase = 'idle' | 'uploading' | 'processing' | 'downloading' | 'success' | 'exception'

interface TransferState {
  percentage: number
  loaded: number
  total: number | null
  phase: TransferPhase
  message: string
}

const createTransferState = (): TransferState => ({
  percentage: 0,
  loaded: 0,
  total: null,
  phase: 'idle',
  message: ''
})

export const useDocumentStore = defineStore('document', () => {
  const currentProcessor = ref<string>('kf')
  const processors = ref<ProcessorInfo[]>([])
  const processedFiles = ref<ProcessedFile[]>([])
  const isUploading = ref(false)
  const isImageUploading = ref(false)
  const isExporting = ref(false)
  const loading = ref(false)

  const excelUploadProgress = ref<TransferState>(createTransferState())
  const imageUploadProgress = ref<TransferState>(createTransferState())
  const exportProgress = ref<TransferState>(createTransferState())

  const resetTransferState = (target: typeof excelUploadProgress) => {
    target.value = createTransferState()
  }

  const updateTransferState = (
    target: typeof excelUploadProgress,
    progress: TransferProgress,
    phase: TransferPhase,
    message: string
  ) => {
    target.value = {
      percentage: progress.total ? progress.percentage : target.value.percentage,
      loaded: progress.loaded,
      total: progress.total ?? null,
      phase,
      message
    }
  }

  const fetchProcessors = async () => {
    loading.value = true
    try {
      const response = await documentApi.getProcessors()
      processors.value = response.processors
      return response.processors
    } finally {
      loading.value = false
    }
  }

  const fetchProcessedFiles = async () => {
    loading.value = true
    try {
      const response = await documentApi.getProcessedFiles(currentProcessor.value)
      processedFiles.value = response.files
      return response.files
    } finally {
      loading.value = false
    }
  }

  const setCurrentProcessor = async (name: string) => {
    currentProcessor.value = name
    await fetchProcessedFiles()
  }

  const handleUploadProgress = (target: typeof excelUploadProgress, progress: TransferProgress) => {
    const uploadFinished = typeof progress.total === 'number' && progress.loaded >= progress.total

    updateTransferState(
      target,
      progress,
      uploadFinished ? 'processing' : 'uploading',
      uploadFinished ? '文件已上传，正在等待服务器处理...' : '正在上传文件...'
    )
  }

  const finalizeTransferSuccess = (target: typeof excelUploadProgress, message: string) => {
    target.value = {
      percentage: 100,
      loaded: target.value.total ?? target.value.loaded,
      total: target.value.total,
      phase: 'success',
      message
    }
  }

  const finalizeTransferError = (target: typeof excelUploadProgress, message: string) => {
    target.value = {
      ...target.value,
      phase: 'exception',
      message
    }
  }

  const uploadExcel = async (file: File) => {
    isUploading.value = true
    resetTransferState(excelUploadProgress)
    excelUploadProgress.value = {
      ...createTransferState(),
      phase: 'uploading',
      message: '正在上传文件...'
    }

    try {
      const result = await documentApi.uploadExcel(file, currentProcessor.value, {
        onUploadProgress: (progress) => handleUploadProgress(excelUploadProgress, progress)
      })

      await fetchProcessedFiles()
      finalizeTransferSuccess(excelUploadProgress, result.message || '上传成功')
      return result
    } catch (error: any) {
      finalizeTransferError(excelUploadProgress, error?.message || '上传失败')
      throw error
    } finally {
      isUploading.value = false
    }
  }

  const uploadImagesZip = async (file: File, dataSource: string) => {
    isImageUploading.value = true
    resetTransferState(imageUploadProgress)
    imageUploadProgress.value = {
      ...createTransferState(),
      phase: 'uploading',
      message: '正在上传图片压缩包...'
    }

    try {
      const result = await documentApi.uploadImagesZip(file, dataSource, currentProcessor.value, {
        onUploadProgress: (progress) => handleUploadProgress(imageUploadProgress, progress)
      })

      finalizeTransferSuccess(imageUploadProgress, result.message || '图片上传成功')
      return result
    } catch (error: any) {
      finalizeTransferError(imageUploadProgress, error?.message || '图片上传失败')
      throw error
    } finally {
      isImageUploading.value = false
    }
  }

  const importJsonData = async (dataSource: string) => {
    isUploading.value = true
    try {
      const result = await documentApi.importJsonData(currentProcessor.value, dataSource)
      await fetchProcessedFiles()
      return result
    } finally {
      isUploading.value = false
    }
  }

  const getStatistics = async (): Promise<StatisticsData | null> => {
    try {
      const response = await documentApi.getStatistics(currentProcessor.value)
      return response.data
    } catch {
      return null
    }
  }

  const exportEntityText = async (dataSources?: string[]) => {
    isExporting.value = true
    try {
      return await documentApi.exportEntityText(currentProcessor.value, dataSources)
    } finally {
      isExporting.value = false
    }
  }

  const exportClipAlignment = async (dataSources?: string[]) => {
    isExporting.value = true
    try {
      return await documentApi.exportClipAlignment(currentProcessor.value, dataSources)
    } finally {
      isExporting.value = false
    }
  }

  const exportQaAlignment = async (dataSources?: string[]) => {
    isExporting.value = true
    try {
      return await documentApi.exportQaAlignment(currentProcessor.value, dataSources)
    } finally {
      isExporting.value = false
    }
  }

  const batchExport = async (params: BatchExportParams) => {
    isExporting.value = true
    resetTransferState(exportProgress)
    exportProgress.value = {
      ...createTransferState(),
      phase: 'processing',
      message: '正在打包导出文件...'
    }

    try {
      const blob = await documentApi.batchExport(currentProcessor.value, params, {
        onDownloadProgress: (progress) => {
          updateTransferState(
            exportProgress,
            progress,
            'downloading',
            progress.total ? '正在下载导出文件...' : '导出文件已生成，正在接收数据...'
          )
        }
      })

      finalizeTransferSuccess(exportProgress, '导出完成')
      return blob
    } catch (error: any) {
      finalizeTransferError(exportProgress, error?.message || '导出失败')
      throw error
    } finally {
      isExporting.value = false
    }
  }

  const resetExcelUploadProgress = () => {
    resetTransferState(excelUploadProgress)
  }

  const resetImageUploadProgress = () => {
    resetTransferState(imageUploadProgress)
  }

  const resetExportProgress = () => {
    resetTransferState(exportProgress)
  }

  const reset = () => {
    currentProcessor.value = 'kf'
    processedFiles.value = []
    isUploading.value = false
    isImageUploading.value = false
    isExporting.value = false
    loading.value = false
    resetExcelUploadProgress()
    resetImageUploadProgress()
    resetExportProgress()
  }

  return {
    currentProcessor,
    processors,
    processedFiles,
    isUploading,
    isImageUploading,
    isExporting,
    loading,
    excelUploadProgress,
    imageUploadProgress,
    exportProgress,
    fetchProcessors,
    fetchProcessedFiles,
    setCurrentProcessor,
    uploadExcel,
    uploadImagesZip,
    importJsonData,
    getStatistics,
    exportEntityText,
    exportClipAlignment,
    exportQaAlignment,
    batchExport,
    resetExcelUploadProgress,
    resetImageUploadProgress,
    resetExportProgress,
    reset
  }
})
