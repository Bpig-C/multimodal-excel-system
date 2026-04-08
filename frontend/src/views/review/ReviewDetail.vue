<template>
  <div class="review-detail-page">
    <!-- 加载状态 -->
    <el-loading v-if="loading" fullscreen text="加载复核任务数据中..." />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <el-divider direction="vertical" />
        <h2>复核任务 #{{ reviewId }}</h2>
        <el-tag :type="getStatusType(reviewStatus)" size="small">
          {{ getStatusText(reviewStatus) }}
        </el-tag>
      </div>

      <div class="header-right">
        <el-button-group v-if="reviewStatus === 'pending'">
          <el-button type="danger" @click="handleReject" :loading="submitting">
            <el-icon><Close /></el-icon>
            驳回
          </el-button>
          <el-button type="success" @click="handleApprove" :loading="submitting">
            <el-icon><Check /></el-icon>
            批准
          </el-button>
        </el-button-group>
        <el-tag v-else :type="getStatusType(reviewStatus)" size="large">
          {{ getStatusText(reviewStatus) }}
        </el-tag>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="page-content">
      <!-- 左侧：标注查看器 -->
      <div class="viewer-section">
        <el-tabs v-model="activeTab" class="viewer-tabs">
          <!-- 文本标注 -->
          <el-tab-pane label="文本标注" name="text">
            <TextAnnotationEditor
              v-if="corpusText"
              :text="corpusText"
              :entities="textEntities"
              :relations="relations"
              :entity-types="entityTypes"
              :relation-types="relationTypes"
              :readonly="reviewStatus !== 'pending'"
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
              :readonly="reviewStatus !== 'pending'"
              @add-whole-image-entity="(entity) => handleAddWholeImageEntity(image.id, entity)"
              @delete-whole-image-entity="(id) => handleDeleteWholeImageEntity(image.id, id)"
              @add-bbox="(bbox) => handleAddBBox(image.id, bbox)"
              @update-bbox="(id, bbox) => handleUpdateBBox(image.id, id, bbox)"
              @delete-bbox="(id) => handleDeleteBBox(image.id, id)"
            />
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 右侧：复核信息面板 -->
      <div class="info-panel">
        <!-- 复核信息 -->
        <el-card class="info-card">
          <template #header>
            <span>复核信息</span>
          </template>
          <div class="info-item">
            <span class="label">复核ID:</span>
            <span class="value">{{ reviewId }}</span>
          </div>
          <div class="info-item">
            <span class="label">标注任务ID:</span>
            <span class="value">{{ taskId || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="label">状态:</span>
            <span class="value">{{ getStatusText(reviewStatus) }}</span>
          </div>
          <div class="info-item">
            <span class="label">复核人:</span>
            <span class="value">{{ reviewerId ? `用户${reviewerId}` : '未分配' }}</span>
          </div>
          <div class="info-item">
            <span class="label">创建时间:</span>
            <span class="value">{{ formatDateTime(createdAt) }}</span>
          </div>
          <div class="info-item">
            <span class="label">复核时间:</span>
            <span class="value">{{ formatDateTime(reviewedAt) }}</span>
          </div>
        </el-card>

        <!-- 复核意见 -->
        <el-card class="info-card">
          <template #header>
            <span>复核意见</span>
          </template>
          <el-input
            v-if="reviewStatus === 'pending'"
            v-model="reviewComment"
            type="textarea"
            :rows="6"
            placeholder="请输入复核意见（驳回时必填）"
          />
          <div v-else class="review-comment-display">
            {{ reviewComment || '无' }}
          </div>
        </el-card>

        <!-- 标注统计 -->
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
            <span class="stat-value">{{ imageEntities.size }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">边界框:</span>
            <span class="stat-value">{{ bboxes.size }}</span>
          </div>
        </el-card>

        <!-- 操作提示 -->
        <el-card v-if="reviewStatus === 'pending'" class="info-card">
          <template #header>
            <span>操作说明</span>
          </template>
          <div class="guide-item">
            <strong>复核流程：</strong>
            <p>1. 仔细检查文本和图片标注</p>
            <p>2. 如需修改，可直接编辑标注</p>
            <p>3. 填写复核意见（驳回时必填）</p>
            <p>4. 点击"批准"或"驳回"按钮</p>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 驳回确认对话框 -->
    <el-dialog
      v-model="showRejectDialog"
      title="驳回确认"
      width="500px"
    >
      <el-form :model="rejectForm" label-width="100px">
        <el-form-item label="驳回原因" required>
          <el-input
            v-model="rejectForm.comment"
            type="textarea"
            :rows="4"
            placeholder="请输入驳回原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRejectDialog = false">取消</el-button>
        <el-button
          type="danger"
          @click="confirmReject"
          :disabled="!rejectForm.comment"
          :loading="submitting"
        >
          确认驳回
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  Check,
  Close
} from '@element-plus/icons-vue'
import TextAnnotationEditor from '@/components/annotation/TextAnnotationEditor.vue'
import ImageAnnotationEditor from '@/components/annotation/ImageAnnotationEditor.vue'
import { useLabelStore } from '@/stores/label'
import type { EntityType, RelationType } from '@/api/label'
import { reviewApi } from '@/api/review'
import { annotationApi } from '@/api/annotation'
import { formatDateTime } from '@/utils/datetime'

// 路由
const route = useRoute()
const router = useRouter()
const reviewId = computed(() => route.params.reviewId as string)

// Store
const labelStore = useLabelStore()

// 状态
const activeTab = ref('text')
const loading = ref(true)
const submitting = ref(false)
const reviewStatus = ref<'pending' | 'approved' | 'rejected'>('pending')
const showRejectDialog = ref(false)

// 复核信息
const taskId = ref('')
const reviewerId = ref<number>()
const reviewComment = ref('')
const createdAt = ref('')
const reviewedAt = ref('')

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

// 驳回表单
const rejectForm = ref({
  comment: ''
})

// 加载复核任务数据
const loadReviewData = async () => {
  try {
    loading.value = true
    
    console.log('[ReviewDetail] 开始加载复核数据, reviewId:', reviewId.value)
    
    // 获取复核任务详情
    const reviewResponse = await reviewApi.get(reviewId.value)
    
    console.log('[ReviewDetail] 复核API响应:', reviewResponse)
    
    // 后端可能直接返回对象，也可能是 { data: {...} } 格式
    const review = reviewResponse.data || reviewResponse
    
    console.log('[ReviewDetail] 解析后的复核数据:', review)
    
    // 设置复核信息
    if (review && review.task) {
      taskId.value = review.task_id || review.task?.task_id || ''
      reviewStatus.value = review.status || 'pending'
      reviewerId.value = review.reviewer_id
      reviewComment.value = review.review_comment || ''
      createdAt.value = review.created_at || ''
      reviewedAt.value = review.reviewed_at || ''
      
      console.log('[ReviewDetail] 复核信息已设置:', {
        taskId: taskId.value,
        reviewStatus: reviewStatus.value,
        reviewerId: reviewerId.value
      })
      
      // 如果有task_id，加载标注数据
      if (taskId.value) {
        await loadAnnotationData(taskId.value)
      } else {
        console.warn('[ReviewDetail] 没有task_id，无法加载标注数据')
      }
    } else {
      console.warn('[ReviewDetail] review 数据为空或格式不正确:', review)
    }
  } catch (error: any) {
    console.error('加载复核任务失败:', error)
    ElMessage.error(error.message || '加载复核任务失败')
  } finally {
    loading.value = false
  }
}

// 加载标注数据
const loadAnnotationData = async (taskIdValue: string) => {
  try {
    console.log('[ReviewDetail] 开始加载标注数据, taskId:', taskIdValue)
    
    // 调用后端API获取任务详情（使用封装的API服务，包含认证头）
    const result = await annotationApi.getAnnotationTask(taskIdValue)
    
    console.log('[ReviewDetail] 标注API响应:', result)
    
    if (!result.success) {
      throw new Error(result.message || '获取标注数据失败')
    }
    
    const data = result.data
    
    // 设置语料文本
    corpusText.value = data.corpus?.text || ''
    
    console.log('[ReviewDetail] 语料文本长度:', corpusText.value.length)
    
    // 设置实体数据
    textEntities.value = data.entities?.map((e: any) => {
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
        color: entityType?.color || '#cccccc'
      }
    }) || []
    
    // 设置关系数据
    relations.value = data.relations?.map((r: any) => {
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
    
    console.log('[ReviewDetail] 标注数据加载完成:', {
      corpusText: corpusText.value.substring(0, 50) + '...',
      entities: textEntities.value.length,
      relations: relations.value.length
    })
    
    // TODO: 加载图片数据
    images.value = []
  } catch (error: any) {
    console.error('加载标注数据失败:', error)
    ElMessage.error(error.message || '加载标注数据失败')
  }
}

// 批准复核
const handleApprove = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要批准此标注任务吗？',
      '确认批准',
      { type: 'success' }
    )

    submitting.value = true
    
    await reviewApi.approve(reviewId.value, {
      comment: reviewComment.value
    })
    
    ElMessage.success('批准成功')
    reviewStatus.value = 'approved'
    reviewedAt.value = new Date().toISOString()
    
    // 延迟返回列表
    setTimeout(() => {
      router.push({ name: 'review' })
    }, 1500)
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('批准失败:', error)
      ElMessage.error(error.message || '批准失败')
    }
  } finally {
    submitting.value = false
  }
}

// 驳回复核
const handleReject = () => {
  rejectForm.value.comment = reviewComment.value
  showRejectDialog.value = true
}

const confirmReject = async () => {
  if (!rejectForm.value.comment) {
    ElMessage.warning('请填写驳回原因')
    return
  }

  try {
    submitting.value = true
    
    await reviewApi.reject(reviewId.value, {
      comment: rejectForm.value.comment
    })
    
    ElMessage.success('驳回成功')
    reviewStatus.value = 'rejected'
    reviewComment.value = rejectForm.value.comment
    reviewedAt.value = new Date().toISOString()
    showRejectDialog.value = false
    
    // 延迟返回列表
    setTimeout(() => {
      router.push({ name: 'review' })
    }, 1500)
  } catch (error: any) {
    console.error('驳回失败:', error)
    ElMessage.error(error.message || '驳回失败')
  } finally {
    submitting.value = false
  }
}

// 标注编辑操作（仅在pending状态下可用）
const handleAddTextEntity = async (entity: any) => {
  if (reviewStatus.value !== 'pending') return
  
  try {
    const response = await annotationApi.addTextEntity(taskId.value, {
      token: entity.text,
      label: entity.entity_type_name,
      start_offset: entity.start_offset,
      end_offset: entity.end_offset
    })
    
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
  if (reviewStatus.value !== 'pending') return
  
  try {
    await annotationApi.updateTextEntity(taskId.value, id, {
      token: updates.text,
      label: updates.entity_type_name,
      start_offset: updates.start_offset,
      end_offset: updates.end_offset
    })
    
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
  if (reviewStatus.value !== 'pending') return
  
  try {
    await annotationApi.deleteTextEntity(taskId.value, id)
    
    relations.value = relations.value.filter(
      r => r.source_entity_id !== id && r.target_entity_id !== id
    )
    textEntities.value = textEntities.value.filter(e => e.id !== id)
  } catch (error) {
    console.error('删除实体失败:', error)
    ElMessage.error('删除实体失败')
  }
}

const handleAddRelation = async (relation: any) => {
  if (reviewStatus.value !== 'pending') return
  
  try {
    const response = await annotationApi.addRelation(taskId.value, {
      from_entity_id: relation.source_entity_id,
      to_entity_id: relation.target_entity_id,
      relation_type: relation.relation_type_name
    })
    
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
  if (reviewStatus.value !== 'pending') return
  
  try {
    await annotationApi.deleteRelation(taskId.value, id)
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
  if (reviewStatus.value !== 'pending') return
  const entities = imageEntities.value.get(imageId) || []
  entities.push({ ...entity, id: Date.now() })
  imageEntities.value.set(imageId, entities)
}

const handleDeleteWholeImageEntity = (imageId: number, entityId: number) => {
  if (reviewStatus.value !== 'pending') return
  const entities = imageEntities.value.get(imageId) || []
  imageEntities.value.set(imageId, entities.filter(e => e.id !== entityId))
}

const getImageBBoxes = (imageId: number) => {
  return bboxes.value.get(imageId) || []
}

const handleAddBBox = (imageId: number, bbox: any) => {
  if (reviewStatus.value !== 'pending') return
  const boxes = bboxes.value.get(imageId) || []
  boxes.push({ ...bbox, id: Date.now() })
  bboxes.value.set(imageId, boxes)
}

const handleUpdateBBox = (imageId: number, bboxId: number, updates: any) => {
  if (reviewStatus.value !== 'pending') return
  const boxes = bboxes.value.get(imageId) || []
  const index = boxes.findIndex(b => b.id === bboxId)
  if (index !== -1) {
    boxes[index] = { ...boxes[index], ...updates }
    bboxes.value.set(imageId, boxes)
  }
}

const handleDeleteBBox = (imageId: number, bboxId: number) => {
  if (reviewStatus.value !== 'pending') return
  const boxes = bboxes.value.get(imageId) || []
  bboxes.value.set(imageId, boxes.filter(b => b.id !== bboxId))
}

// 返回
const goBack = () => {
  router.push({ name: 'review' })
}

// 状态相关
const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待复核',
    approved: '已通过',
    rejected: '已驳回'
  }
  return textMap[status] || '未知'
}

// formatDateTime 已从 @/utils/datetime 导入

// 初始化
onMounted(async () => {
  try {
    // 加载标签配置
    await labelStore.fetchEntityTypes({ include_inactive: false })
    await labelStore.fetchRelationTypes({ include_inactive: false })
    entityTypes.value = labelStore.entityTypes
    relationTypes.value = labelStore.relationTypes

    // 加载复核数据
    await loadReviewData()
  } catch (error) {
    ElMessage.error('初始化失败')
  }
})
</script>

<style scoped>
.review-detail-page {
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

.viewer-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.viewer-tabs {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.viewer-tabs :deep(.el-tabs__content) {
  flex: 1;
  overflow: hidden;
}

.viewer-tabs :deep(.el-tab-pane) {
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

.review-comment-display {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100px;
  white-space: pre-wrap;
}

.guide-item {
  margin-bottom: 16px;
}

.guide-item:last-child {
  margin-bottom: 0;
}

.guide-item strong {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  color: #606266;
}

.guide-item p {
  margin: 4px 0;
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}
</style>
