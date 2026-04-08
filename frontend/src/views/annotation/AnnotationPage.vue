<template>
  <div class="annotation-page">
    <!-- 加载状态 -->
    <el-loading v-if="loading" fullscreen text="加载任务数据中..." />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <el-divider direction="vertical" />
        <h2>标注任务 #{{ taskId }}</h2>
        <el-tag :type="getStatusType(taskStatus)" size="small">
          {{ getStatusText(taskStatus) }}
        </el-tag>
      </div>

      <div class="header-right">
        <el-button-group>
          <el-button 
            @click="handleSave" 
            :loading="saving"
            :disabled="taskStatus === 'under_review' || taskStatus === 'approved'"
          >
            <el-icon><DocumentCopy /></el-icon>
            保存
          </el-button>
          <el-button 
            v-if="taskStatus !== 'under_review' && taskStatus !== 'approved'"
            type="primary" 
            @click="handleSubmitReview"
          >
            <el-icon><Check /></el-icon>
            提交复核
          </el-button>
          <el-button 
            v-else
            type="success" 
            @click="goToReview"
          >
            <el-icon><View /></el-icon>
            查看复核
          </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="page-content">
      <div class="content-wrapper">
        <!-- 驳回提示 -->
        <el-alert
          v-if="taskStatus === 'rejected'"
          title="任务已被驳回"
          type="warning"
          description="该任务已被复核人员驳回，请根据驳回意见修改后重新保存并提交复核。"
          show-icon
          :closable="false"
          class="rejection-alert"
        />
        
        <!-- 只读提示 -->
        <el-alert
          v-if="isReadonly"
          title="只读模式"
          type="info"
          :description="getReadonlyMessage()"
          show-icon
          :closable="false"
          class="readonly-alert"
        />
        
        <!-- 左侧：标注编辑器 -->
        <div class="editor-section">
          <el-tabs v-model="activeTab" class="editor-tabs">
            <!-- 文本标注 -->
            <el-tab-pane label="文本标注" name="text">
              <TextAnnotationEditor
                v-if="corpusText"
                :text="corpusText"
                :entities="textEntities"
                :relations="relations"
                :entity-types="entityTypes"
                :relation-types="relationTypes"
                :readonly="isReadonly"
                @add-entity="handleAddTextEntity"
                @update-entity="handleUpdateTextEntity"
                @delete-entity="handleDeleteTextEntity"
                @add-relation="handleAddRelation"
                @delete-relation="handleDeleteRelation"
              />
              <el-empty v-else description="无文本内容" />
            </el-tab-pane>

            <!-- 图片标注 -->
            <el-tab-pane
              v-for="image in images"
              :key="image.id"
              :label="`图片 ${image.id}`"
              :name="`image-${image.id}`"
            >
              <ImageAnnotationEditor
                :image-url="image.url"
                :whole-image-entities="getImageEntities(image.id)"
                :bboxes="getImageBBoxes(image.id)"
                :entity-types="entityTypes"
                :readonly="isReadonly"
                @add-whole-image-entity="(entity) => handleAddWholeImageEntity(image.id, entity)"
                @delete-whole-image-entity="(id) => handleDeleteWholeImageEntity(image.id, id)"
                @add-bbox="(bbox) => handleAddBBox(image.id, bbox)"
                @update-bbox="(id, bbox) => handleUpdateBBox(image.id, id, bbox)"
                @delete-bbox="(id) => handleDeleteBBox(image.id, id)"
              />
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <!-- 右侧：信息面板 -->
      <div class="info-panel">
        <!-- 驳回历史 -->
        <el-card v-if="rejectionHistory.length > 0" class="info-card rejection-history-card">
          <template #header>
            <div class="card-header">
              <span>驳回历史</span>
              <el-tag type="warning" size="small">{{ rejectionHistory.length }} 次</el-tag>
            </div>
          </template>
          <el-scrollbar max-height="300px">
            <el-timeline>
              <el-timeline-item
                v-for="(rejection, index) in rejectionHistory"
                :key="index"
                :timestamp="formatDateTime(rejection.reviewed_at)"
                placement="top"
                type="warning"
              >
                <el-card>
                  <div class="rejection-item">
                    <div class="rejection-header">
                      <span class="rejection-round">第 {{ rejectionHistory.length - index }} 次驳回</span>
                      <span class="rejection-reviewer">复核人: {{ rejection.reviewer_id ? `用户${rejection.reviewer_id}` : '未知' }}</span>
                    </div>
                    <div class="rejection-comment">
                      {{ rejection.review_comment || '无驳回意见' }}
                    </div>
                  </div>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-scrollbar>
        </el-card>
        
        <!-- 任务信息 -->
        <el-card class="info-card">
          <template #header>
            <span>任务信息</span>
          </template>
          <div class="info-item">
            <span class="label">任务ID:</span>
            <span class="value">{{ taskId }}</span>
          </div>
          <div class="info-item">
            <span class="label">数据集ID:</span>
            <span class="value">{{ datasetId || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="label">语料ID:</span>
            <span class="value">{{ corpusId || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="label">状态:</span>
            <span class="value">{{ getStatusText(taskStatus) }}</span>
          </div>
          <div class="info-item">
            <span class="label">创建时间:</span>
            <span class="value">{{ formatDateTime(createdAt) }}</span>
          </div>
          <div class="info-item">
            <span class="label">更新时间:</span>
            <span class="value">{{ formatDateTime(updatedAt) }}</span>
          </div>
        </el-card>

        <!-- 统计信息 -->
        <el-card class="info-card">
          <template #header>
            <span>标注统计</span>
          </template>
          <div class="stat-item">
            <span class="stat-label">文本实体:</span>
            <span class="stat-value">{{ textEntities.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">关系:</span>
            <span class="stat-value">{{ relations.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">图片实体:</span>
            <span class="stat-value">{{ imageEntities.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">边界框:</span>
            <span class="stat-value">{{ bboxes.length }}</span>
          </div>
        </el-card>

        <!-- 版本历史 -->
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>版本历史</span>
              <el-button text size="small" @click="refreshVersions">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          <el-scrollbar max-height="300px">
            <div class="version-list">
              <div
                v-for="version in versions"
                :key="version.id"
                class="version-item"
                :class="{ current: version.is_current }"
              >
                <div class="version-info">
                  <span class="version-number">v{{ version.version_number }}</span>
                  <span class="version-time">{{ formatTime(version.created_at) }}</span>
                </div>
                <el-button
                  v-if="!version.is_current"
                  text
                  size="small"
                  @click="handleRollback(version.id)"
                >
                  回滚
                </el-button>
              </div>
            </div>
          </el-scrollbar>
        </el-card>

        <!-- 快捷键说明 -->
        <el-card class="info-card">
          <template #header>
            <span>快捷键</span>
          </template>
          <div class="shortcut-list">
            <div class="shortcut-item">
              <kbd>Ctrl + S</kbd>
              <span>保存</span>
            </div>
            <div class="shortcut-item">
              <kbd>Ctrl + Enter</kbd>
              <span>提交复核</span>
            </div>
            <div class="shortcut-item">
              <kbd>Esc</kbd>
              <span>取消操作</span>
            </div>
          </div>
          <el-divider />
          <div class="annotation-guide">
            <h4>标注操作</h4>
            <div class="guide-item">
              <strong>实体标注：</strong>
              <p>鼠标拖动选择文本，在弹出菜单中选择实体类型</p>
            </div>
            <div class="guide-item">
              <strong>关系标注：</strong>
              <p>按住 <kbd>Ctrl</kbd> 键，依次点击源实体和目标实体，然后选择关系类型</p>
            </div>
            <div class="guide-item">
              <strong>删除标注：</strong>
              <p>在右侧列表中点击删除按钮</p>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  DocumentCopy,
  Check,
  Refresh,
  View
} from '@element-plus/icons-vue'
import TextAnnotationEditor from '@/components/annotation/TextAnnotationEditor.vue'
import ImageAnnotationEditor from '@/components/annotation/ImageAnnotationEditor.vue'
import { useLabelStore } from '@/stores/label'
import type { EntityType, RelationType } from '@/api/label'
import { annotationApi } from '@/api/annotation'
import { reviewApi } from '@/api/review'

// 路由
const route = useRoute()
const router = useRouter()
const taskId = computed(() => route.params.taskId as string)

// Store
const labelStore = useLabelStore()

// 状态
const activeTab = ref('text')
const saving = ref(false)
const loading = ref(true)
const taskStatus = ref<'pending' | 'annotating' | 'reviewing' | 'approved' | 'rejected'>('pending')

// 只读模式：当任务处于复核中或已通过状态时，不允许编辑
// 注意：rejected（已驳回）状态应该允许编辑，以便标注员修改后重新提交
const isReadonly = computed(() => {
  return ['under_review', 'approved'].includes(taskStatus.value)
})

// 获取只读提示信息
const getReadonlyMessage = () => {
  const messages: Record<string, string> = {
    under_review: '该任务正在复核中，暂时无法编辑。如需修改，请等待复核结果。',
    approved: '该任务已通过复核，不可再编辑。'
  }
  return messages[taskStatus.value] || '该任务当前不可编辑。'
}

// 任务信息
const datasetName = ref('')
const datasetId = ref('')
const corpusId = ref('')
const annotatorName = ref('当前用户')
const createdAt = ref('')
const updatedAt = ref('')

// 语料文本
const corpusText = ref('')

// 图片列表
const images = ref<Array<{ id: number; url: string }>>([])

// 标注数据
const textEntities = ref<any[]>([])
const relations = ref<any[]>([])
const imageEntities = ref<Map<number, any[]>>(new Map())
const bboxes = ref<Map<number, any[]>>(new Map())

// 标签配置
const entityTypes = ref<EntityType[]>([])
const relationTypes = ref<RelationType[]>([])

// 版本历史
const versions = ref<any[]>([])

// 驳回历史
const rejectionHistory = ref<any[]>([])

// 加载任务数据
const loadTaskData = async () => {
  try {
    loading.value = true
    
    // 调用后端API获取任务详情（使用封装的API服务，包含认证头）
    const result = await annotationApi.getAnnotationTask(taskId.value)
    
    if (!result.success) {
      throw new Error(result.message || '获取任务详情失败')
    }
    
    const data = result.data
    
    // 设置任务信息
    datasetId.value = data.dataset_id || ''
    corpusId.value = data.corpus?.text_id || ''
    taskStatus.value = data.status || 'pending'
    createdAt.value = data.created_at || ''
    updatedAt.value = data.updated_at || ''
    
    // 设置语料文本
    corpusText.value = data.corpus?.text || ''
    
    // 设置实体数据 - 需要从 entityTypes 中匹配颜色和类型名称
    textEntities.value = data.entities?.map((e: any) => {
      // 尝试匹配中文名或英文名
      const entityType = entityTypes.value.find(et => 
        et.type_name === e.label || et.type_name_zh === e.label
      )
      return {
        id: e.id,
        entity_id: e.entity_id,
        text: e.token,
        entity_type_name: e.label,
        entity_type_id: entityType?.id,
        start_offset: e.start_offset,
        end_offset: e.end_offset,
        confidence: e.confidence,
        color: entityType?.color || '#cccccc' // 默认颜色
      }
    }) || []
    
    // 设置关系数据 - 需要从 relationTypes 中匹配类型名称
    relations.value = data.relations?.map((r: any) => {
      // 尝试匹配中文名或英文名
      const relationType = relationTypes.value.find(rt => 
        rt.type_name === r.relation_type || rt.type_name_zh === r.relation_type
      )
      return {
        id: r.id,
        relation_id: r.relation_id,
        source_entity_id: r.from_entity_id,
        target_entity_id: r.to_entity_id,
        relation_type_name: r.relation_type,
        relation_type_id: relationType?.id
      }
    }) || []
    
    // TODO: 加载图片数据
    // 目前图片数据为空，后续需要实现
    images.value = []
    
    // 加载驳回历史
    await loadRejectionHistory()
    
    console.log('任务数据加载成功:', {
      taskId: taskId.value,
      taskStatus: taskStatus.value,
      isReadonly: isReadonly.value,
      corpusText: corpusText.value,
      entities: textEntities.value.length,
      relations: relations.value.length,
      entityTypes: entityTypes.value.length,
      relationTypes: relationTypes.value.length,
      rejections: rejectionHistory.value.length
    })
  } catch (error: any) {
    console.error('加载任务数据失败:', error)
    ElMessage.error(error.message || '加载任务数据失败')
  } finally {
    loading.value = false
  }
}

// 加载驳回历史
const loadRejectionHistory = async () => {
  try {
    // 查询该任务的所有复核记录
    const response = await reviewApi.list({ 
      skip: 0, 
      limit: 100 
    })
    
    const reviews = Array.isArray(response) ? response : (response.data || [])
    
    // 筛选出该任务的所有驳回记录，按时间倒序排列
    rejectionHistory.value = reviews
      .filter((r: any) => r.task_id === taskId.value && r.status === 'rejected')
      .sort((a: any, b: any) => {
        const timeA = new Date(a.reviewed_at || a.created_at).getTime()
        const timeB = new Date(b.reviewed_at || b.created_at).getTime()
        return timeB - timeA // 最新的在前
      })
    
    console.log('[AnnotationPage] 驳回历史加载完成:', rejectionHistory.value.length, '条记录')
  } catch (error) {
    console.error('加载驳回历史失败:', error)
    // 不显示错误提示，因为这不是关键功能
  }
}

// 加载数据
onMounted(async () => {
  try {
    // 加载标签配置
    await labelStore.fetchEntityTypes({ include_inactive: false })
    await labelStore.fetchRelationTypes({ include_inactive: false })
    entityTypes.value = labelStore.entityTypes
    relationTypes.value = labelStore.relationTypes
    
    console.log('[AnnotationPage] Loaded entityTypes:', entityTypes.value)
    console.log('[AnnotationPage] Loaded relationTypes:', relationTypes.value)

    // 加载任务数据
    await loadTaskData()

    // 初始化图片实体和边界框
    images.value.forEach(image => {
      imageEntities.value.set(image.id, [])
      bboxes.value.set(image.id, [])
    })

    // 注册快捷键
    document.addEventListener('keydown', handleKeyDown)
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})

// 快捷键处理
const handleKeyDown = (e: KeyboardEvent) => {
  // Ctrl + S: 保存
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault()
    handleSave()
  }
  // Ctrl + Enter: 提交复核
  if (e.ctrlKey && e.key === 'Enter') {
    e.preventDefault()
    handleSubmitReview()
  }
  // Esc: 取消操作
  if (e.key === 'Escape') {
    // TODO: 取消当前操作
  }
}

// 文本实体操作
const handleAddTextEntity = async (entity: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API添加实体
    const response = await annotationApi.addTextEntity(taskId.value, {
      token: entity.text,
      label: entity.entity_type_name,
      start_offset: entity.start_offset,
      end_offset: entity.end_offset
    })
    
    // 添加到本地数组，使用后端返回的ID
    textEntities.value.push({
      ...entity,
      id: response.data.id,
      entity_id: response.data.entity_id
    })
  } catch (error) {
    console.error('添加实体失败:', error)
    ElMessage.error('添加实体失败')
  }
}

const handleUpdateTextEntity = async (id: number, updates: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API更新实体
    await annotationApi.updateTextEntity(taskId.value, id, {
      token: updates.text,
      label: updates.entity_type_name,
      start_offset: updates.start_offset,
      end_offset: updates.end_offset
    })
    
    // 更新本地数组
    const index = textEntities.value.findIndex(e => e.id === id)
    if (index !== -1) {
      textEntities.value[index] = { ...textEntities.value[index], ...updates }
    }
  } catch (error) {
    console.error('更新实体失败:', error)
    ElMessage.error('更新实体失败')
  }
}

const handleDeleteTextEntity = async (id: number) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API删除实体（后端会自动删除相关关系）
    await annotationApi.deleteTextEntity(taskId.value, id)
    
    // 删除本地相关关系
    relations.value = relations.value.filter(
      r => r.source_entity_id !== id && r.target_entity_id !== id
    )
    // 删除本地实体
    textEntities.value = textEntities.value.filter(e => e.id !== id)
    
    console.log('[AnnotationPage] Entity deleted, remaining entities:', textEntities.value.length)
  } catch (error) {
    console.error('删除实体失败:', error)
    ElMessage.error('删除实体失败')
  }
}

// 关系操作
const handleAddRelation = async (relation: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API添加关系
    const response = await annotationApi.addRelation(taskId.value, {
      from_entity_id: relation.source_entity_id,
      to_entity_id: relation.target_entity_id,
      relation_type: relation.relation_type_name
    })
    
    // 添加到本地数组，使用后端返回的ID
    relations.value.push({
      ...relation,
      id: response.data.id,
      relation_id: response.data.relation_id
    })
  } catch (error) {
    console.error('添加关系失败:', error)
    ElMessage.error('添加关系失败')
  }
}

const handleDeleteRelation = async (id: number) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  try {
    // 调用后端API删除关系
    await annotationApi.deleteRelation(taskId.value, id)
    
    // 删除本地关系
    relations.value = relations.value.filter(r => r.id !== id)
  } catch (error) {
    console.error('删除关系失败:', error)
    ElMessage.error('删除关系失败')
  }
}

// 图片实体操作
const getImageEntities = (imageId: number) => {
  return imageEntities.value.get(imageId) || []
}

const handleAddWholeImageEntity = (imageId: number, entity: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const entities = imageEntities.value.get(imageId) || []
  entities.push({ ...entity, id: Date.now() })
  imageEntities.value.set(imageId, entities)
}

const handleDeleteWholeImageEntity = (imageId: number, entityId: number) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const entities = imageEntities.value.get(imageId) || []
  imageEntities.value.set(imageId, entities.filter(e => e.id !== entityId))
}

// 边界框操作
const getImageBBoxes = (imageId: number) => {
  return bboxes.value.get(imageId) || []
}

const handleAddBBox = (imageId: number, bbox: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const boxes = bboxes.value.get(imageId) || []
  boxes.push({ ...bbox, id: Date.now() })
  bboxes.value.set(imageId, boxes)
}

const handleUpdateBBox = (imageId: number, bboxId: number, updates: any) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const boxes = bboxes.value.get(imageId) || []
  const index = boxes.findIndex(b => b.id === bboxId)
  if (index !== -1) {
    boxes[index] = { ...boxes[index], ...updates }
    bboxes.value.set(imageId, boxes)
  }
}

const handleDeleteBBox = (imageId: number, bboxId: number) => {
  if (isReadonly.value) {
    ElMessage.warning('当前任务不可编辑')
    return
  }
  
  const boxes = bboxes.value.get(imageId) || []
  bboxes.value.set(imageId, boxes.filter(b => b.id !== bboxId))
}

// 保存
const handleSave = async () => {
  if (!taskId.value) return
  
  saving.value = true
  try {
    // 标注数据已经通过增删改操作实时保存到后端
    // 这里更新任务状态为"已完成"，以便后续提交复核
    await annotationApi.updateAnnotationTask(
      taskId.value, 
      { status: 'completed' }
    )
    
    taskStatus.value = 'completed'
    ElMessage.success('保存成功')
    updatedAt.value = new Date().toISOString()
    
    // 重新加载任务数据以获取最新版本号
    await loadTaskData()
  } catch (error: any) {
    console.error('保存失败:', error)
    ElMessage.error(error.message || '保存失败')
  } finally {
    saving.value = false
  }
}

// 提交复核
const handleSubmitReview = async () => {
  if (!taskId.value) return
  
  try {
    // 检查任务状态，如果不是completed，提示用户先保存
    if (taskStatus.value !== 'completed') {
      await ElMessageBox.confirm(
        '请先保存标注结果，然后再提交复核。',
        '提示',
        { 
          type: 'warning',
          confirmButtonText: '保存并提交',
          cancelButtonText: '取消'
        }
      )
      
      // 先保存
      await handleSave()
    }
    
    // 确认提交
    await ElMessageBox.confirm(
      '确定要提交复核吗？提交后将无法继续编辑。',
      '提示',
      { type: 'warning' }
    )

    // 调用API提交复核
    console.log('[AnnotationPage] 开始提交复核, taskId:', taskId.value)
    const response = await reviewApi.submit(taskId.value)
    
    console.log('[AnnotationPage] 提交复核响应:', response)
    
    if (response.data || response.review_id) {
      taskStatus.value = 'under_review'
      ElMessage.success('提交复核成功')
      
      // 重新加载任务数据
      await loadTaskData()
      
      // 可选：跳转到复核列表
      // router.push({ name: 'review' })
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('提交复核失败:', error)
      console.error('错误详情:', error.response?.data)
      ElMessage.error(error.response?.data?.detail || error.message || '提交复核失败')
    }
  }
}

// 版本回滚
const handleRollback = async (versionId: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要回滚到此版本吗？当前未保存的修改将丢失。',
      '警告',
      { type: 'warning' }
    )

    // TODO: 调用API回滚版本
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('回滚成功')
    // 重新加载数据
  } catch (error) {
    // 用户取消
  }
}

// 刷新版本列表
const refreshVersions = () => {
  // TODO: 调用API刷新版本列表
  ElMessage.success('刷新成功')
}

// 返回
const goBack = () => {
  router.back()
}

// 跳转到复核页面
const goToReview = async () => {
  try {
    console.log('[AnnotationPage] 查找复核任务, taskId:', taskId.value)
    
    // 查询该任务的复核记录
    const response = await reviewApi.list({ 
      skip: 0, 
      limit: 100 
    })
    
    console.log('[AnnotationPage] 复核列表API响应:', response)
    
    // 后端直接返回数组，不是 { data: [...] } 格式
    const reviews = Array.isArray(response) ? response : (response.data || [])
    console.log('[AnnotationPage] 复核任务列表:', reviews)
    console.log('[AnnotationPage] 当前taskId:', taskId.value)
    
    const review = reviews.find((r: any) => {
      console.log('[AnnotationPage] 比较:', r.task_id, '===', taskId.value, '?', r.task_id === taskId.value)
      return r.task_id === taskId.value
    })
    
    if (review) {
      console.log('[AnnotationPage] 找到复核任务:', review)
      router.push({ name: 'review-detail', params: { reviewId: review.review_id } })
    } else {
      console.warn('[AnnotationPage] 未找到对应的复核任务')
      ElMessage.warning('未找到对应的复核任务')
      router.push({ name: 'review' })
    }
  } catch (error) {
    console.error('跳转失败:', error)
    router.push({ name: 'review' })
  }
}

// 状态相关
const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: 'info',
    in_progress: 'warning',
    annotating: 'warning',
    reviewing: 'primary',
    approved: 'success',
    rejected: 'danger',
    completed: 'success'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待标注',
    in_progress: '标注中',
    annotating: '标注中',
    under_review: '复核中',
    reviewing: '复核中',
    approved: '已通过',
    rejected: '已驳回',
    completed: '已完成'
  }
  return textMap[status] || '未知'
}

const formatTime = (time: string) => {
  return time.split(' ')[1] // 只显示时间部分
}

const formatDateTime = (dateTime: string) => {
  if (!dateTime) return '-'
  try {
    const date = new Date(dateTime)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch {
    return dateTime
  }
}
</script>

<style scoped>
.annotation-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #dcdfe6;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.page-content {
  flex: 1;
  display: flex;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
}

.readonly-alert {
  flex-shrink: 0;
}

.editor-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-tabs {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.editor-tabs :deep(.el-tabs__content) {
  flex: 1;
  overflow: hidden;
}

.editor-tabs :deep(.el-tab-pane) {
  height: 100%;
}

.info-panel {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.info-card {
  flex-shrink: 0;
}

.rejection-history-card {
  border-color: #e6a23c;
}

.rejection-item {
  padding: 8px 0;
}

.rejection-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.rejection-round {
  font-weight: 600;
  color: #e6a23c;
}

.rejection-reviewer {
  color: #909399;
}

.rejection-comment {
  padding: 12px;
  background: #fdf6ec;
  border-left: 3px solid #e6a23c;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  white-space: pre-wrap;
  word-break: break-word;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-item,
.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child,
.stat-item:last-child {
  border-bottom: none;
}

.label,
.stat-label {
  color: #909399;
  font-size: 14px;
}

.value,
.stat-value {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

.version-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.version-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  transition: all 0.2s;
}

.version-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.version-item.current {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.version-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.version-number {
  font-weight: 500;
  color: #303133;
}

.version-time {
  font-size: 12px;
  color: #909399;
}

.shortcut-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.shortcut-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.shortcut-item kbd {
  padding: 4px 8px;
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
}

.annotation-guide {
  margin-top: 8px;
}

.annotation-guide h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.guide-item {
  margin-bottom: 16px;
}

.guide-item:last-child {
  margin-bottom: 0;
}

.guide-item strong {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
  color: #606266;
}

.guide-item p {
  margin: 0;
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}

.guide-item kbd {
  padding: 2px 6px;
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  font-size: 11px;
  font-family: monospace;
}
</style>
