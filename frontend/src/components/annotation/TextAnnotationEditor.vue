<template>
  <div class="text-annotation-editor">
    <!-- 工具栏 -->
    <div class="toolbar">
      <el-alert
        v-if="relationCreation.state.value.isActive"
        :title="relationCreation.getHintMessage()"
        type="info"
        :closable="false"
      />
      <el-button
        v-if="relationCreation.state.value.isActive"
        size="small"
        @click="cancelRelationCreation"
      >
        取消关系创建
      </el-button>
      <span v-if="!relationCreation.state.value.isActive && !props.readonly" class="toolbar-hint">
        提示：选择文本创建实体，点击实体选中（Delete键删除），Ctrl+点击实体创建关系
      </span>
      <span v-if="props.readonly" class="toolbar-hint readonly-hint">
        <el-icon><View /></el-icon>
        只读模式：仅可查看标注，不可编辑
      </span>
    </div>

    <!-- 文本显示区域 -->
    <div class="text-display-area">
      <div
        ref="textContainerRef"
        class="text-container"
        v-html="renderedText"
      >
      </div>

      <!-- SVG箭头层 -->
      <RelationArrowLayer
        ref="arrowLayerRef"
        :relations="relations"
        :entities="entities"
        :entity-positions="entityPositions"
        :selected-relation-id="selectedRelationId"
        :width="containerWidth"
        :height="containerHeight"
        @select="handleRelationSelect"
      />

      <!-- 标签选择菜单 -->
      <LabelSelector
        v-if="showLabelSelector"
        :position="labelSelectorPosition"
        :entity-types="entityTypes"
        @select="handleLabelSelect"
        @close="closeLabelSelector"
      />
    </div>

    <!-- 侧边面板 -->
    <div class="side-panel">
      <!-- 实体列表 -->
      <EntityList
        :entities="entities"
        :text="text"
        @select="handleEntitySelect"
        @delete="handleEntityDelete"
        @update="handleEntityUpdate"
      />

      <!-- 关系列表 -->
      <RelationList
        :relations="relations"
        :entities="entities"
        @select="handleRelationSelect"
        @delete="handleRelationDelete"
      />
    </div>

    <!-- 关系类型选择对话框 -->
    <RelationTypeSelector
      v-model="showRelationTypeSelector"
      :source-entity="selectedSourceEntity"
      :target-entity="selectedTargetEntity"
      :relation-types="relationTypes"
      @select="handleRelationTypeSelect"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { View } from '@element-plus/icons-vue'
import LabelSelector from './LabelSelector.vue'
import EntityList from './EntityList.vue'
import RelationList from './RelationList.vue'
import RelationArrowLayer from './RelationArrowLayer.vue'
import RelationTypeSelector from './RelationTypeSelector.vue'
import { useTextSelection } from '@/composables/useTextSelection'
import { useRelationCreation } from '@/composables/useRelationCreation'
import type { EntityType, RelationType } from '@/api/label'

interface Entity {
  id?: number
  text: string
  start_offset: number
  end_offset: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Relation {
  id?: number
  source_entity_id: string  // 使用字符串格式的entity_id
  target_entity_id: string  // 使用字符串格式的entity_id
  relation_type_id: number
  relation_type_name: string
}

interface Props {
  text: string
  entities: Entity[]
  relations: Relation[]
  entityTypes: EntityType[]
  relationTypes: RelationType[]
  readonly?: boolean  // 添加只读模式支持
}

interface Emits {
  (e: 'add-entity', entity: Omit<Entity, 'id'>): void
  (e: 'update-entity', id: number, entity: Partial<Entity>): void
  (e: 'delete-entity', id: number): void
  (e: 'add-relation', relation: Omit<Relation, 'id'>): void
  (e: 'delete-relation', id: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const textContainerRef = ref<HTMLElement>()
const arrowLayerRef = ref<InstanceType<typeof RelationArrowLayer>>()
const showLabelSelector = ref(false)
const labelSelectorPosition = ref({ x: 0, y: 0 })
const selectedRange = ref<{ start: number; end: number } | null>(null)
const selectedEntityId = ref<number | null>(null)
const selectedRelationId = ref<number | null>(null)
const showRelationTypeSelector = ref(false)
const selectedSourceEntity = ref<Entity | null>(null)
const selectedTargetEntity = ref<Entity | null>(null)
const containerWidth = ref(0)
const containerHeight = ref(0)
const entityPositions = ref<Map<string, any>>(new Map())  // 键改为字符串类型

// 使用composables
const { getSelection, validateOffset } = useTextSelection()
const relationCreation = useRelationCreation()

// 计算文字颜色以确保对比度
const getContrastColor = (hexColor: string): string => {
  // 如果颜色未定义，返回黑色
  if (!hexColor) return '#000000'
  
  // 移除 # 号
  const hex = hexColor.replace('#', '')
  
  // 转换为 RGB
  const r = parseInt(hex.substr(0, 2), 16)
  const g = parseInt(hex.substr(2, 2), 16)
  const b = parseInt(hex.substr(4, 2), 16)
  
  // 计算亮度 (使用 YIQ 公式)
  const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000
  
  // 根据亮度返回黑色或白色
  return yiq >= 128 ? '#000000' : '#ffffff'
}

// 渲染带实体高亮的文本（使用v-html）
const renderedText = computed(() => {
  if (!props.text) return ''
  
  // 如果没有实体，直接返回转义后的纯文本
  if (props.entities.length === 0) {
    return escapeHtml(props.text)
  }
  
  // 按偏移量排序实体
  const sortedEntities = [...props.entities].sort((a, b) => a.start_offset - b.start_offset)
  
  let html = ''
  let lastOffset = 0
  
  sortedEntities.forEach(entity => {
    // 添加实体前的文本
    if (entity.start_offset > lastOffset) {
      html += escapeHtml(props.text.substring(lastOffset, entity.start_offset))
    }
    
    // 添加实体（带高亮）
    const entityText = props.text.substring(entity.start_offset, entity.end_offset)
    const textColor = getContrastColor(entity.color)
    const isSelected = selectedEntityId.value === entity.id
    const bgColor = isSelected ? '#ffeb3b' : entity.color
    const finalTextColor = isSelected ? '#000000' : textColor
    
    html += `<span class="entity-highlight" data-entity-id="${entity.id}" style="background-color: ${bgColor}; color: ${finalTextColor}; padding: 2px 4px; border-radius: 3px;">${escapeHtml(entityText)}</span>`
    
    lastOffset = entity.end_offset
  })
  
  // 添加最后的文本
  if (lastOffset < props.text.length) {
    html += escapeHtml(props.text.substring(lastOffset))
  }
  
  return html
})

// HTML转义函数
const escapeHtml = (text: string): string => {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

// 更新容器尺寸
const updateContainerSize = () => {
  if (textContainerRef.value) {
    containerWidth.value = textContainerRef.value.offsetWidth
    // 增加额外高度以容纳上方的箭头（120px padding + 100px 额外空间）
    containerHeight.value = textContainerRef.value.offsetHeight + 220
  }
}

// 更新实体位置
const updateEntityPositions = () => {
  if (!textContainerRef.value) return

  const positions = new Map()
  props.entities.forEach(entity => {
    if (!entity.entity_id) return

    // 查找实体的span元素（使用数字id作为data属性）
    const entitySpan = textContainerRef.value?.querySelector(
      `span[data-entity-id="${entity.id}"]`
    )

    if (entitySpan) {
      const rect = entitySpan.getBoundingClientRect()
      const containerRect = textContainerRef.value!.getBoundingClientRect()

      // 使用entity_id（字符串）作为键
      positions.set(entity.entity_id, {
        x: rect.left - containerRect.left,
        y: rect.top - containerRect.top, // 不加偏移，使用实际位置
        width: rect.width,
        height: rect.height
      })
    }
  })

  entityPositions.value = positions
}

// 处理鼠标松开事件（文本选择完成）
const handleMouseUp = () => {
  // 只读模式下不允许选择
  if (props.readonly) return
  
  // 延迟一小段时间，确保选择已完成
  setTimeout(() => {
    if (!textContainerRef.value) return
    
    const selection = getSelection(textContainerRef.value)
    
    // 只有当有有效选择且选择了文本时才显示标签选择器
    if (selection && selection.text && selection.text.trim().length > 0) {
      selectedRange.value = selection
      
      // 显示标签选择菜单
      const range = window.getSelection()?.getRangeAt(0)
      if (range) {
        const rect = range.getBoundingClientRect()
        labelSelectorPosition.value = {
          x: rect.left + rect.width / 2,
          y: rect.bottom + 10
        }
        showLabelSelector.value = true
      }
    }
  }, 10)
}

// 处理实体点击（使用事件委托）
const handleContainerClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  
  // 检查是否点击了实体
  if (target.classList.contains('entity-highlight')) {
    const entityId = parseInt(target.getAttribute('data-entity-id') || '0', 10)
    const entity = props.entities.find(e => e.id === entityId)
    
    if (entity && entity.id) {
      // Ctrl+点击实体：创建关系（只读模式下不允许）
      if (event.ctrlKey && !props.readonly) {
        event.preventDefault()
        event.stopPropagation()
        
        // 如果还没开始创建关系，自动开始
        if (!relationCreation.state.value.isActive) {
          relationCreation.startCreation()
        }
        
        const completed = relationCreation.selectEntity(entity.id)
        if (completed) {
          // 选择完成，显示关系类型选择对话框
          const { sourceEntityId, targetEntityId } = relationCreation.getSelectedEntities()
          selectedSourceEntity.value = props.entities.find(e => e.id === sourceEntityId) || null
          selectedTargetEntity.value = props.entities.find(e => e.id === targetEntityId) || null
          showRelationTypeSelector.value = true
        }
      } else {
        // 普通点击：选择/取消选择实体
        if (selectedEntityId.value === entity.id) {
          // 再次点击同一个实体，取消选择
          selectedEntityId.value = null
        } else {
          // 选择新实体
          selectedEntityId.value = entity.id
        }
      }
    }
  } else {
    // 点击空白处，取消所有选择
    selectedEntityId.value = null
    selectedRelationId.value = null
  }
}

// 处理标签选择
const handleLabelSelect = (entityType: EntityType) => {
  if (!selectedRange.value) return
  
  const { start, end } = selectedRange.value
  
  // 验证偏移量
  if (!validateOffset(props.text, start, end)) {
    ElMessage.error('选择的文本偏移量无效')
    return
  }
  
  // 检查是否与现有实体重叠
  const hasOverlap = props.entities.some(
    e => !(end <= e.start_offset || start >= e.end_offset)
  )
  
  if (hasOverlap) {
    ElMessage.warning('选择的文本与现有实体重叠')
    return
  }
  
  // 创建新实体
  const newEntity: Omit<Entity, 'id'> = {
    text: props.text.substring(start, end),
    start_offset: start,
    end_offset: end,
    entity_type_id: entityType.id,
    entity_type_name: entityType.type_name_zh,
    color: entityType.color
  }
  
  emit('add-entity', newEntity)
  closeLabelSelector()

  // 更新实体位置
  nextTick(() => {
    updateEntityPositions()
  })
}

// 关闭标签选择菜单
const closeLabelSelector = () => {
  showLabelSelector.value = false
  selectedRange.value = null
  window.getSelection()?.removeAllRanges()
}



// 取消创建关系
const cancelRelationCreation = () => {
  relationCreation.cancelCreation()
}

// 处理关系类型选择
const handleRelationTypeSelect = (relationType: RelationType) => {
  const { sourceEntityId, targetEntityId } = relationCreation.getSelectedEntities()
  
  if (!sourceEntityId || !targetEntityId) return

  // 查找实体对象以获取entity_id
  const sourceEntity = props.entities.find(e => e.id === sourceEntityId)
  const targetEntity = props.entities.find(e => e.id === targetEntityId)
  
  if (!sourceEntity || !targetEntity) {
    ElMessage.error('无法找到选中的实体')
    return
  }

  const newRelation: Omit<Relation, 'id'> = {
    source_entity_id: sourceEntity.entity_id,
    target_entity_id: targetEntity.entity_id,
    relation_type_id: relationType.id,
    relation_type_name: relationType.type_name_zh
  }

  emit('add-relation', newRelation)
  relationCreation.reset()
  ElMessage.success('关系创建成功')
}

// 处理实体选择
const handleEntitySelect = (entityId: number) => {
  selectedEntityId.value = entityId
}

// 处理实体删除
const handleEntityDelete = (entityId: number) => {
  emit('delete-entity', entityId)
  if (selectedEntityId.value === entityId) {
    selectedEntityId.value = null
  }

  // 清除选择，强制重新渲染
  window.getSelection()?.removeAllRanges()

  // 更新实体位置
  nextTick(() => {
    updateEntityPositions()
  })
}

// 处理键盘事件
const handleKeyDown = (event: KeyboardEvent) => {
  // 只读模式下不允许删除
  if (props.readonly) return
  
  // Delete 或 Backspace 键删除选中的实体
  if ((event.key === 'Delete' || event.key === 'Backspace') && selectedEntityId.value) {
    event.preventDefault()
    handleEntityDelete(selectedEntityId.value)
  }
  
  // Escape 键取消选择
  if (event.key === 'Escape') {
    selectedEntityId.value = null
    selectedRelationId.value = null
    if (relationCreation.state.value.isActive) {
      relationCreation.cancelCreation()
    }
  }
}

// 处理实体更新
const handleEntityUpdate = (entityId: number, updates: Partial<Entity>) => {
  emit('update-entity', entityId, updates)

  // 更新实体位置
  nextTick(() => {
    updateEntityPositions()
  })
}

// 处理关系选择
const handleRelationSelect = (relationId: number) => {
  // 如果点击的是已选中的关系，取消选择
  if (selectedRelationId.value === relationId) {
    selectedRelationId.value = null
  } else {
    selectedRelationId.value = relationId
  }
}

// 处理关系删除
const handleRelationDelete = (relationId: number) => {
  emit('delete-relation', relationId)
  if (selectedRelationId.value === relationId) {
    selectedRelationId.value = null
  }
}

// 初始化
onMounted(() => {
  console.log('[TextAnnotationEditor] Mounted with props:', {
    text: props.text?.substring(0, 50) + '...',
    entitiesCount: props.entities.length,
    relationsCount: props.relations.length,
    entityTypesCount: props.entityTypes.length,
    relationTypesCount: props.relationTypes.length,
    entityTypes: props.entityTypes
  })
  
  updateContainerSize()
  updateEntityPositions()

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    updateContainerSize()
    updateEntityPositions()
  })
  
  // 监听键盘事件
  document.addEventListener('keydown', handleKeyDown)
  
  // 监听鼠标松开事件（文本选择完成后显示标签选择器）
  if (textContainerRef.value) {
    textContainerRef.value.addEventListener('mouseup', handleMouseUp)
  }
  
  // 监听容器点击（用于实体点击）
  if (textContainerRef.value) {
    textContainerRef.value.addEventListener('click', handleContainerClick)
  }
})

// 清理
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
  if (textContainerRef.value) {
    textContainerRef.value.removeEventListener('mouseup', handleMouseUp)
    textContainerRef.value.removeEventListener('click', handleContainerClick)
  }
})
</script>

<style scoped>
.text-annotation-editor {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.toolbar-hint {
  color: #909399;
  font-size: 14px;
}

.readonly-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e6a23c;
  font-weight: 500;
}

.text-display-area {
  flex: 1;
  position: relative;
  overflow: visible;  /* 改为 visible，让箭头可以超出容器 */
  display: flex;
  gap: 20px;
}

.text-container {
  flex: 1;
  padding: 20px;
  padding-top: 120px;  /* 增加顶部内边距，为上方的箭头留出空间 */
  line-height: 3;  /* 增加行间距到3倍，为跨行箭头留出空间 */
  font-size: 16px;
  white-space: pre-wrap;
  word-break: break-word;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: text;
  user-select: text;
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
  overflow-y: auto;  /* 添加垂直滚动 */
  max-height: calc(100vh - 400px);  /* 限制最大高度 */
}

/* 实体高亮样式 */
.text-container :deep(.entity-highlight) {
  cursor: text;
  user-select: text;
}

/* Ctrl 键按下时，实体显示为可点击 */
.text-container :deep(.entity-highlight:hover) {
  opacity: 0.9;
}

.side-panel {
  width: 350px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow: auto;
}
</style>
