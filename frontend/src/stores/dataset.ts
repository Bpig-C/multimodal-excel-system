/**
 * 数据集管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { datasetApi } from '@/api'
import type { Dataset } from '@/types'

export const useDatasetStore = defineStore('dataset', () => {
  // State
  const datasetList = ref<Dataset[]>([])
  const currentDataset = ref<Dataset | null>(null)
  const total = ref(0)
  const loading = ref(false)

  // Actions
  const fetchList = async (params?: {
    page?: number
    page_size?: number
    created_by?: number
  }) => {
    loading.value = true
    try {
      const response = await datasetApi.list(params)
      // 后端返回格式: { success, message, data: { items, total } }
      datasetList.value = response.data?.items || []
      total.value = response.data?.total || 0
      return response
    } finally {
      loading.value = false
    }
  }

  const fetchDetail = async (id: string | number) => {
    loading.value = true
    try {
      const response = await datasetApi.get(id)
      // 后端返回格式: { success, message, data: {...} }
      currentDataset.value = response.data || null
      return response.data
    } finally {
      loading.value = false
    }
  }

  const create = async (data: {
    name: string
    description?: string
    corpus_ids: number[]
    created_by: number
    label_schema_version_id?: number
  }) => {
    loading.value = true
    try {
      const response = await datasetApi.create(data)
      // 创建成功后刷新列表
      await fetchList()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const update = async (id: number, data: {
    name?: string
    description?: string
    label_schema_version_id?: number
  }) => {
    loading.value = true
    try {
      const response = await datasetApi.update(id, data)
      const dataset = response.data
      // 更新列表中的数据
      const index = datasetList.value.findIndex(d => d.id === id)
      if (index !== -1) {
        datasetList.value[index] = dataset
      }
      if (currentDataset.value?.id === id) {
        currentDataset.value = dataset
      }
      return dataset
    } finally {
      loading.value = false
    }
  }

  const deleteDataset = async (datasetId: string) => {
    loading.value = true
    try {
      await datasetApi.delete(datasetId)
      // 删除成功后从列表中移除
      datasetList.value = datasetList.value.filter(d => d.dataset_id !== datasetId)
      total.value--
      if (currentDataset.value?.dataset_id === datasetId) {
        currentDataset.value = null
      }
    } finally {
      loading.value = false
    }
  }

  const exportDataset = async (datasetId: string, params?: {
    output_path?: string
    status_filter?: string[]
  }) => {
    loading.value = true
    try {
      return await datasetApi.export(datasetId, params)
    } finally {
      loading.value = false
    }
  }

  const fetchDatasetTasks = async (
    datasetId: string,
    params?: {
      page?: number
      page_size?: number
      status?: string
    }
  ) => {
    loading.value = true
    try {
      const response = await datasetApi.getTasks(datasetId, params)
      return response.data || { items: [], total: 0 }
    } finally {
      loading.value = false
    }
  }

  const addTasksToDataset = async (datasetId: string, corpusIds: number[]) => {
    loading.value = true
    try {
      const response = await datasetApi.addTasks(datasetId, corpusIds)
      return response.data || { added: 0, skipped: 0 }
    } finally {
      loading.value = false
    }
  }

  const removeTaskFromDataset = async (datasetId: string, taskId: string) => {
    loading.value = true
    try {
      await datasetApi.removeTask(datasetId, taskId)
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    datasetList.value = []
    currentDataset.value = null
    total.value = 0
    loading.value = false
  }

  return {
    datasetList,
    currentDataset,
    total,
    loading,
    fetchList,
    fetchDetail,
    create,
    update,
    deleteDataset,
    exportDataset,
    fetchDatasetTasks,
    addTasksToDataset,
    removeTaskFromDataset,
    reset
  }
})
