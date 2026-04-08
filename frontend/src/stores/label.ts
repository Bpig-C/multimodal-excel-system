/**
 * 标签管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { labelApi, type EntityType, type RelationType, type LabelSchemaVersion } from '@/api/label'

export const useLabelStore = defineStore('label', () => {
  // State
  const entityTypes = ref<EntityType[]>([])
  const relationTypes = ref<RelationType[]>([])
  const versions = ref<LabelSchemaVersion[]>([])
  const currentVersion = ref<LabelSchemaVersion | null>(null)
  const loading = ref(false)

  // Actions
  const fetchEntityTypes = async (params?: {
    include_inactive?: boolean
    include_unreviewed?: boolean
  }) => {
    loading.value = true
    try {
      const response = await labelApi.listEntityTypes(params)
      entityTypes.value = response.data?.items || []
      return response
    } finally {
      loading.value = false
    }
  }

  const createEntityType = async (data: {
    type_name: string
    type_name_zh: string
    color: string
    description?: string
    supports_bbox?: boolean
  }) => {
    loading.value = true
    try {
      const response = await labelApi.createEntityType(data)
      // 刷新列表
      await fetchEntityTypes()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const updateEntityType = async (id: number, data: {
    type_name?: string
    type_name_zh?: string
    color?: string
    description?: string
    supports_bbox?: boolean
    is_active?: boolean
  }) => {
    loading.value = true
    try {
      const response = await labelApi.updateEntityType(id, data)
      // 更新列表中的数据
      const index = entityTypes.value.findIndex(et => et.id === id)
      if (index !== -1) {
        entityTypes.value[index] = response.data
      }
      return response.data
    } finally {
      loading.value = false
    }
  }

  const deleteEntityType = async (id: number) => {
    loading.value = true
    try {
      await labelApi.deleteEntityType(id)
      // 从列表中移除
      entityTypes.value = entityTypes.value.filter(et => et.id !== id)
    } finally {
      loading.value = false
    }
  }

  const generateEntityDefinition = async (id: number) => {
    loading.value = true
    try {
      const response = await labelApi.generateEntityDefinition(id)
      // 刷新列表
      await fetchEntityTypes()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const reviewEntityType = async (id: number, data: {
    approved: boolean
    definition?: string
    examples?: string[]
    disambiguation?: string
  }) => {
    loading.value = true
    try {
      const response = await labelApi.reviewEntityType(id, data)
      // 更新列表中的数据
      const index = entityTypes.value.findIndex(et => et.id === id)
      if (index !== -1) {
        entityTypes.value[index] = response.data
      }
      return response.data
    } finally {
      loading.value = false
    }
  }

  const fetchRelationTypes = async (params?: {
    include_inactive?: boolean
    include_unreviewed?: boolean
  }) => {
    loading.value = true
    try {
      const response = await labelApi.listRelationTypes(params)
      relationTypes.value = response.data?.items || []
      return response
    } finally {
      loading.value = false
    }
  }

  const createRelationType = async (data: {
    type_name: string
    type_name_zh: string
    color: string
    description?: string
  }) => {
    loading.value = true
    try {
      const response = await labelApi.createRelationType(data)
      // 刷新列表
      await fetchRelationTypes()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const updateRelationType = async (id: number, data: {
    type_name?: string
    type_name_zh?: string
    color?: string
    description?: string
    is_active?: boolean
  }) => {
    loading.value = true
    try {
      const response = await labelApi.updateRelationType(id, data)
      // 更新列表中的数据
      const index = relationTypes.value.findIndex(rt => rt.id === id)
      if (index !== -1) {
        relationTypes.value[index] = response.data
      }
      return response.data
    } finally {
      loading.value = false
    }
  }

  const deleteRelationType = async (id: number) => {
    loading.value = true
    try {
      await labelApi.deleteRelationType(id)
      // 从列表中移除
      relationTypes.value = relationTypes.value.filter(rt => rt.id !== id)
    } finally {
      loading.value = false
    }
  }

  const generateRelationDefinition = async (id: number) => {
    loading.value = true
    try {
      const response = await labelApi.generateRelationDefinition(id)
      // 刷新列表
      await fetchRelationTypes()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const reviewRelationType = async (id: number, data: {
    approved: boolean
    definition?: string
    direction_rule?: string
    examples?: string[]
    disambiguation?: string
  }) => {
    loading.value = true
    try {
      const response = await labelApi.reviewRelationType(id, data)
      // 更新列表中的数据
      const index = relationTypes.value.findIndex(rt => rt.id === id)
      if (index !== -1) {
        relationTypes.value[index] = response.data
      }
      return response.data
    } finally {
      loading.value = false
    }
  }

  const importLabels = async (data: {
    entity_types: Partial<EntityType>[]
    relation_types: Partial<RelationType>[]
  }) => {
    loading.value = true
    try {
      const response = await labelApi.importLabels(data)
      // 刷新列表
      await fetchEntityTypes()
      await fetchRelationTypes()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const exportLabels = async () => {
    loading.value = true
    try {
      const response = await labelApi.exportLabels()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const previewPrompt = async (promptType?: 'entity' | 'relation' | 'image') => {
    loading.value = true
    try {
      const response = await labelApi.previewPrompt({ prompt_type: promptType })
      return response.data.prompt
    } finally {
      loading.value = false
    }
  }

  const fetchVersions = async () => {
    loading.value = true
    try {
      const response = await labelApi.listVersions()
      versions.value = response.data?.items || []
      // 找到当前激活的版本
      currentVersion.value = versions.value.find(v => v.is_active) || null
      return response
    } finally {
      loading.value = false
    }
  }

  const createSnapshot = async (data: {
    version_name: string
    description: string
    created_by: number
  }) => {
    loading.value = true
    try {
      const response = await labelApi.createSnapshot(data)
      // 刷新版本列表
      await fetchVersions()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const activateVersion = async (versionId: string) => {
    loading.value = true
    try {
      const response = await labelApi.activateVersion(versionId)
      // 刷新版本列表和标签列表
      await fetchVersions()
      await fetchEntityTypes()
      await fetchRelationTypes()
      return response.data
    } finally {
      loading.value = false
    }
  }

  const compareVersions = async (version1: string, version2: string) => {
    loading.value = true
    try {
      const response = await labelApi.compareVersions({ version1, version2 })
      return response.data
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    entityTypes.value = []
    relationTypes.value = []
    versions.value = []
    currentVersion.value = null
    loading.value = false
  }

  return {
    entityTypes,
    relationTypes,
    versions,
    currentVersion,
    loading,
    fetchEntityTypes,
    createEntityType,
    updateEntityType,
    deleteEntityType,
    generateEntityDefinition,
    reviewEntityType,
    fetchRelationTypes,
    createRelationType,
    updateRelationType,
    deleteRelationType,
    generateRelationDefinition,
    reviewRelationType,
    importLabels,
    exportLabels,
    previewPrompt,
    fetchVersions,
    createSnapshot,
    activateVersion,
    compareVersions,
    reset
  }
})
