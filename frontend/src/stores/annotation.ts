/**
 * 标注任务Store
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { annotationApi } from '@/api'
import type { AnnotationTask, TextEntity, BatchJobProgress } from '@/types'

export const useAnnotationStore = defineStore('annotation', () => {
  // State
  const currentTask = ref<AnnotationTask | null>(null)
  const batchJobs = ref<Map<string, BatchJobProgress>>(new Map())
  const loading = ref(false)

  // Getters
  const textEntities = computed(() => currentTask.value?.text_entities || [])
  const imageEntities = computed(() => currentTask.value?.image_entities || [])
  const relations = computed(() => currentTask.value?.relations || [])

  const entityMap = computed(() => {
    const map = new Map<number, TextEntity>()
    textEntities.value.forEach(e => map.set(e.entity_id, e))
    return map
  })

  // Actions - 任务管理
  const fetchTask = async (taskId: string) => {
    loading.value = true
    try {
      const task = await annotationApi.get(taskId)
      currentTask.value = task
      return task
    } finally {
      loading.value = false
    }
  }

  const updateTask = async (taskId: string, data: {
    status?: string
    assigned_to?: number
  }) => {
    loading.value = true
    try {
      const task = await annotationApi.update(taskId, data)
      if (currentTask.value?.task_id === taskId) {
        currentTask.value = task
      }
      return task
    } finally {
      loading.value = false
    }
  }

  // Actions - 批量标注
  const startBatchAnnotation = async (data: {
    dataset_id: string
    annotation_type: 'automatic' | 'manual'
    assigned_to: number
  }) => {
    loading.value = true
    try {
      const result = await annotationApi.batchAnnotate(data)
      // 初始化批量任务状态
      batchJobs.value.set(result.job_id, {
        job_id: result.job_id,
        status: 'pending',
        progress: {
          total: 0,
          completed: 0,
          failed: 0
        }
      })
      return result
    } finally {
      loading.value = false
    }
  }

  const fetchBatchStatus = async (jobId: string) => {
    try {
      const status = await annotationApi.getBatchStatus(jobId)
      batchJobs.value.set(jobId, status)
      return status
    } catch (error) {
      console.error('获取批量任务状态失败:', error)
      throw error
    }
  }

  const pollBatchStatus = (jobId: string, interval = 2000): NodeJS.Timeout => {
    const timer = setInterval(async () => {
      try {
        const status = await fetchBatchStatus(jobId)
        if (status.status === 'completed' || status.status === 'failed' || status.status === 'cancelled') {
          clearInterval(timer)
        }
      } catch (error) {
        clearInterval(timer)
      }
    }, interval)
    return timer
  }

  // Actions - 实体管理
  const addEntity = async (taskId: string, data: {
    token: string
    label: string
    start_offset: number
    end_offset: number
  }) => {
    loading.value = true
    try {
      const entity = await annotationApi.addEntity(taskId, data)
      if (currentTask.value?.task_id === taskId) {
        currentTask.value.text_entities.push(entity)
      }
      return entity
    } finally {
      loading.value = false
    }
  }

  const updateEntity = async (taskId: string, entityId: number, data: {
    token?: string
    label?: string
    start_offset?: number
    end_offset?: number
  }) => {
    loading.value = true
    try {
      const entity = await annotationApi.updateEntity(taskId, entityId, data)
      if (currentTask.value?.task_id === taskId) {
        const index = currentTask.value.text_entities.findIndex(e => e.entity_id === entityId)
        if (index !== -1) {
          currentTask.value.text_entities[index] = entity
        }
      }
      return entity
    } finally {
      loading.value = false
    }
  }

  const deleteEntity = async (taskId: string, entityId: number) => {
    loading.value = true
    try {
      await annotationApi.deleteEntity(taskId, entityId)
      if (currentTask.value?.task_id === taskId) {
        currentTask.value.text_entities = currentTask.value.text_entities.filter(
          e => e.entity_id !== entityId
        )
        // 同时删除相关的关系
        currentTask.value.relations = currentTask.value.relations.filter(
          r => r.from_entity_id !== entityId && r.to_entity_id !== entityId
        )
      }
    } finally {
      loading.value = false
    }
  }

  // Actions - 关系管理
  const addRelation = async (taskId: string, data: {
    from_entity_id: number
    to_entity_id: number
    relation_type: string
  }) => {
    loading.value = true
    try {
      const relation = await annotationApi.addRelation(taskId, data)
      if (currentTask.value?.task_id === taskId) {
        currentTask.value.relations.push(relation)
      }
      return relation
    } finally {
      loading.value = false
    }
  }

  const updateRelation = async (taskId: string, relationId: number, data: {
    from_entity_id?: number
    to_entity_id?: number
    relation_type?: string
  }) => {
    loading.value = true
    try {
      const relation = await annotationApi.updateRelation(taskId, relationId, data)
      if (currentTask.value?.task_id === taskId) {
        const index = currentTask.value.relations.findIndex(r => r.relation_id === relationId)
        if (index !== -1) {
          currentTask.value.relations[index] = relation
        }
      }
      return relation
    } finally {
      loading.value = false
    }
  }

  const deleteRelation = async (taskId: string, relationId: number) => {
    loading.value = true
    try {
      await annotationApi.deleteRelation(taskId, relationId)
      if (currentTask.value?.task_id === taskId) {
        currentTask.value.relations = currentTask.value.relations.filter(
          r => r.relation_id !== relationId
        )
      }
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    currentTask.value = null
    batchJobs.value.clear()
    loading.value = false
  }

  return {
    // State
    currentTask,
    batchJobs,
    loading,
    // Getters
    textEntities,
    imageEntities,
    relations,
    entityMap,
    // Actions - 任务管理
    fetchTask,
    updateTask,
    // Actions - 批量标注
    startBatchAnnotation,
    fetchBatchStatus,
    pollBatchStatus,
    // Actions - 实体管理
    addEntity,
    updateEntity,
    deleteEntity,
    // Actions - 关系管理
    addRelation,
    updateRelation,
    deleteRelation,
    // 工具方法
    reset
  }
})
