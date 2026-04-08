/**
 * 标签管理API
 */
import { request } from './request'

// 实体类型接口
export interface EntityType {
  id: number
  type_name: string
  type_name_zh: string
  color: string
  description?: string
  definition?: string
  examples?: string[]
  disambiguation?: string
  supports_bbox: boolean
  is_active: boolean
  is_reviewed: boolean
  reviewed_by?: number
  reviewed_at?: string
  created_at: string
  updated_at?: string
}

// 关系类型接口
export interface RelationType {
  id: number
  type_name: string
  type_name_zh: string
  color: string
  description?: string
  definition?: string
  direction_rule?: string
  examples?: string[]
  disambiguation?: string
  is_active: boolean
  is_reviewed: boolean
  reviewed_by?: number
  reviewed_at?: string
  created_at: string
  updated_at?: string
}

// 标签体系版本接口
export interface LabelSchemaVersion {
  id: number
  version_id: string
  version_name: string
  description: string
  is_active: boolean
  entity_types: EntityType[]
  relation_types: RelationType[]
  created_by: number
  created_at: string
}

export const labelApi = {
  // ============================================================================
  // 实体类型管理
  // ============================================================================

  /**
   * 获取实体类型列表
   */
  listEntityTypes(params?: {
    include_inactive?: boolean
    include_unreviewed?: boolean
  }) {
    return request.get<{
      success: boolean
      message: string
      data: {
        items: EntityType[]
        total: number
      }
    }>('/labels/entities', { params })
  },

  /**
   * 创建实体类型
   */
  createEntityType(data: {
    type_name: string
    type_name_zh: string
    color: string
    description?: string
    supports_bbox?: boolean
  }) {
    return request.post<{
      success: boolean
      message: string
      data: EntityType
    }>('/labels/entities', data)
  },

  /**
   * 更新实体类型
   */
  updateEntityType(id: number, data: {
    type_name?: string
    type_name_zh?: string
    color?: string
    description?: string
    supports_bbox?: boolean
    is_active?: boolean
  }) {
    return request.put<{
      success: boolean
      message: string
      data: EntityType
    }>(`/labels/entities/${id}`, data)
  },

  /**
   * 删除实体类型
   */
  deleteEntityType(id: number) {
    return request.delete<{
      success: boolean
      message: string
    }>(`/labels/entities/${id}`)
  },

  /**
   * 生成实体类型定义
   */
  generateEntityDefinition(id: number) {
    return request.post<{
      success: boolean
      message: string
      data: {
        definition: string
        examples: string[]
        disambiguation: string
      }
    }>(`/labels/entities/${id}/generate-definition`)
  },

  /**
   * 审核实体类型定义
   */
  reviewEntityType(id: number, data: {
    approved: boolean
    definition?: string
    examples?: string[]
    disambiguation?: string
  }) {
    return request.post<{
      success: boolean
      message: string
      data: EntityType
    }>(`/labels/entities/${id}/review`, data)
  },

  // ============================================================================
  // 关系类型管理
  // ============================================================================

  /**
   * 获取关系类型列表
   */
  listRelationTypes(params?: {
    include_inactive?: boolean
    include_unreviewed?: boolean
  }) {
    return request.get<{
      success: boolean
      message: string
      data: {
        items: RelationType[]
        total: number
      }
    }>('/labels/relations', { params })
  },

  /**
   * 创建关系类型
   */
  createRelationType(data: {
    type_name: string
    type_name_zh: string
    color: string
    description?: string
  }) {
    return request.post<{
      success: boolean
      message: string
      data: RelationType
    }>('/labels/relations', data)
  },

  /**
   * 更新关系类型
   */
  updateRelationType(id: number, data: {
    type_name?: string
    type_name_zh?: string
    color?: string
    description?: string
    is_active?: boolean
  }) {
    return request.put<{
      success: boolean
      message: string
      data: RelationType
    }>(`/labels/relations/${id}`, data)
  },

  /**
   * 删除关系类型
   */
  deleteRelationType(id: number) {
    return request.delete<{
      success: boolean
      message: string
    }>(`/labels/relations/${id}`)
  },

  /**
   * 生成关系类型定义
   */
  generateRelationDefinition(id: number) {
    return request.post<{
      success: boolean
      message: string
      data: {
        definition: string
        direction_rule: string
        examples: string[]
        disambiguation: string
      }
    }>(`/labels/relations/${id}/generate-definition`)
  },

  /**
   * 审核关系类型定义
   */
  reviewRelationType(id: number, data: {
    approved: boolean
    definition?: string
    direction_rule?: string
    examples?: string[]
    disambiguation?: string
  }) {
    return request.post<{
      success: boolean
      message: string
      data: RelationType
    }>(`/labels/relations/${id}/review`, data)
  },

  // ============================================================================
  // 导入导出
  // ============================================================================

  /**
   * 导入标签配置
   */
  importLabels(data: {
    entity_types: Partial<EntityType>[]
    relation_types: Partial<RelationType>[]
  }) {
    return request.post<{
      success: boolean
      message: string
      data: {
        imported_entities: number
        imported_relations: number
      }
    }>('/labels/import', data)
  },

  /**
   * 导出标签配置
   */
  exportLabels() {
    return request.get<{
      success: boolean
      message: string
      data: {
        entity_types: EntityType[]
        relation_types: RelationType[]
      }
    }>('/labels/export')
  },

  // ============================================================================
  // Prompt预览
  // ============================================================================

  /**
   * 预览Agent Prompt
   */
  previewPrompt(params?: {
    prompt_type?: 'entity' | 'relation' | 'image'
  }) {
    return request.get<{
      success: boolean
      message: string
      data: {
        prompt: string
      }
    }>('/labels/prompt-preview', { params })
  },

  // ============================================================================
  // 版本管理
  // ============================================================================

  /**
   * 获取版本列表
   */
  listVersions() {
    return request.get<{
      success: boolean
      message: string
      data: {
        items: LabelSchemaVersion[]
        total: number
      }
    }>('/labels/versions')
  },

  /**
   * 创建版本快照
   */
  createSnapshot(data: {
    version_name: string
    description: string
    created_by: number
  }) {
    return request.post<{
      success: boolean
      message: string
      data: LabelSchemaVersion
    }>('/labels/versions/snapshot', data)
  },

  /**
   * 获取版本详情
   */
  getVersion(versionId: string) {
    return request.get<{
      success: boolean
      message: string
      data: LabelSchemaVersion
    }>(`/labels/versions/${versionId}`)
  },

  /**
   * 激活版本
   */
  activateVersion(versionId: string) {
    return request.post<{
      success: boolean
      message: string
      data: LabelSchemaVersion
    }>(`/labels/versions/${versionId}/activate`)
  },

  /**
   * 比较版本差异
   */
  compareVersions(params: {
    version1: string
    version2: string
  }) {
    return request.get<{
      success: boolean
      message: string
      data: {
        added_entities: EntityType[]
        removed_entities: EntityType[]
        modified_entities: Array<{
          old: EntityType
          new: EntityType
        }>
        added_relations: RelationType[]
        removed_relations: RelationType[]
        modified_relations: Array<{
          old: RelationType
          new: RelationType
        }>
      }
    }>('/labels/versions/compare', { params })
  }
}
