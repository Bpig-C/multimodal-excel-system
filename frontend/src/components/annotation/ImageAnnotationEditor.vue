<template>
  <div class="image-annotation-editor">
    <!-- 工具栏 -->
    <div class="toolbar">
      <el-radio-group v-model="annotationMode" size="small" :disabled="props.readonly">
        <el-radio-button value="whole">整图标注</el-radio-button>
        <el-radio-button value="region">区域标注</el-radio-button>
      </el-radio-group>

      <el-divider direction="vertical" />

      <el-button-group size="small">
        <el-button @click="zoomIn">
          <el-icon><ZoomIn /></el-icon>
        </el-button>
        <el-button @click="zoomOut">
          <el-icon><ZoomOut /></el-icon>
        </el-button>
        <el-button @click="resetZoom">
          <el-icon><RefreshRight /></el-icon>
        </el-button>
      </el-button-group>

      <span class="zoom-info">{{ Math.round(scale * 100) }}%</span>

      <el-divider direction="vertical" />

      <el-button
        v-if="selectedBBox && !props.readonly"
        type="danger"
        size="small"
        @click="deleteSelectedBBox"
      >
        删除选中区域
      </el-button>
      
      <span v-if="props.readonly" class="toolbar-hint readonly-hint">
        <el-icon><View /></el-icon>
        只读模式：仅可查看标注，不可编辑
      </span>
    </div>

    <!-- 图片显示区域 -->
    <div class="image-display-area">
      <div
        ref="containerRef"
        class="image-container"
        :class="{ 'region-mode': annotationMode === 'region' }"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @wheel="handleWheel"
      >
        <img
          ref="imageRef"
          :src="imageUrl"
          :style="imageStyle"
          @load="handleImageLoad"
          @click="handleImageClick"
        />

        <!-- 边界框层 -->
        <svg
          v-if="annotationMode === 'region'"
          class="bbox-layer"
          :style="imageStyle"
        >
          <!-- 已标注的边界框 -->
          <g
            v-for="bbox in bboxes"
            :key="bbox.id"
            @click.stop="selectBBox(bbox.id!)"
          >
            <rect
              :x="bbox.x * scale"
              :y="bbox.y * scale"
              :width="bbox.width * scale"
              :height="bbox.height * scale"
              :stroke="bbox.color"
              :stroke-width="selectedBBox === bbox.id ? 3 : 2"
              fill="none"
              :class="{ 'bbox-rect': true, 'selected': selectedBBox === bbox.id }"
            />
            <text
              :x="bbox.x * scale + 5"
              :y="bbox.y * scale + 20"
              class="bbox-label"
              :fill="bbox.color"
            >
              {{ bbox.entity_type_name }}
            </text>
          </g>

          <!-- 正在绘制的边界框 -->
          <rect
            v-if="drawingBBox"
            :x="drawingBBox.x"
            :y="drawingBBox.y"
            :width="drawingBBox.width"
            :height="drawingBBox.height"
            stroke="#409eff"
            stroke-width="2"
            stroke-dasharray="5,5"
            fill="rgba(64, 158, 255, 0.1)"
          />
        </svg>
      </div>

      <!-- 整图标注标签选择 -->
      <LabelSelector
        v-if="showLabelSelector && annotationMode === 'whole'"
        :position="labelSelectorPosition"
        :entity-types="entityTypes"
        @select="handleWholeImageLabel"
        @close="closeLabelSelector"
      />

      <!-- 区域标注标签选择 -->
      <LabelSelector
        v-if="showBBoxLabelSelector"
        :position="bboxLabelSelectorPosition"
        :entity-types="bboxEntityTypes"
        @select="handleBBoxLabel"
        @close="closeBBoxLabelSelector"
      />
    </div>

    <!-- 侧边面板 -->
    <div class="side-panel">
      <!-- 整图标注列表 -->
      <div v-if="annotationMode === 'whole'" class="annotation-list">
        <div class="list-header">
          <h3>整图标注 ({{ wholeImageEntities.length }})</h3>
        </div>
        <el-scrollbar>
          <div class="entity-items">
            <div
              v-for="entity in wholeImageEntities"
              :key="entity.id"
              class="entity-item"
            >
              <el-tag
                :color="entity.color"
                :style="{ backgroundColor: entity.color, color: '#fff', border: 'none' }"
                size="small"
              >
                {{ entity.entity_type_name }}
              </el-tag>
              <el-button
                v-if="!props.readonly"
                type="danger"
                size="small"
                text
                @click="deleteWholeImageEntity(entity.id!)"
              >
                删除
              </el-button>
            </div>
          </div>
        </el-scrollbar>
      </div>

      <!-- 区域标注列表 -->
      <div v-if="annotationMode === 'region'" class="annotation-list">
        <div class="list-header">
          <h3>区域标注 ({{ bboxes.length }})</h3>
        </div>
        <el-scrollbar>
          <div class="bbox-items">
            <div
              v-for="bbox in bboxes"
              :key="bbox.id"
              class="bbox-item"
              :class="{ selected: selectedBBox === bbox.id }"
              @click="selectBBox(bbox.id!)"
            >
              <el-tag
                :color="bbox.color"
                :style="{ backgroundColor: bbox.color, color: '#fff', border: 'none' }"
                size="small"
              >
                {{ bbox.entity_type_name }}
              </el-tag>
              <div class="bbox-coords">
                {{ Math.round(bbox.x) }}, {{ Math.round(bbox.y) }}, 
                {{ Math.round(bbox.width) }}, {{ Math.round(bbox.height) }}
              </div>
              <el-button
                v-if="!props.readonly"
                type="danger"
                size="small"
                text
                @click.stop="deleteBBox(bbox.id!)"
              >
                删除
              </el-button>
            </div>
          </div>
        </el-scrollbar>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ZoomIn, ZoomOut, RefreshRight, View } from '@element-plus/icons-vue'
import LabelSelector from './LabelSelector.vue'
import type { EntityType } from '@/api/label'

interface ImageEntity {
  id?: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface BoundingBox {
  id?: number
  x: number
  y: number
  width: number
  height: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Props {
  imageUrl: string
  wholeImageEntities: ImageEntity[]
  bboxes: BoundingBox[]
  entityTypes: EntityType[]
  readonly?: boolean  // 添加只读模式支持
}

interface Emits {
  (e: 'add-whole-image-entity', entity: Omit<ImageEntity, 'id'>): void
  (e: 'delete-whole-image-entity', id: number): void
  (e: 'add-bbox', bbox: Omit<BoundingBox, 'id'>): void
  (e: 'update-bbox', id: number, bbox: Partial<BoundingBox>): void
  (e: 'delete-bbox', id: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const containerRef = ref<HTMLElement>()
const imageRef = ref<HTMLImageElement>()
const annotationMode = ref<'whole' | 'region'>('whole')
const scale = ref(1)
const translateX = ref(0)
const translateY = ref(0)
const imageNaturalWidth = ref(0)
const imageNaturalHeight = ref(0)

// 整图标注
const showLabelSelector = ref(false)
const labelSelectorPosition = ref({ x: 0, y: 0 })

// 区域标注
const showBBoxLabelSelector = ref(false)
const bboxLabelSelectorPosition = ref({ x: 0, y: 0 })
const drawingBBox = ref<{ x: number; y: number; width: number; height: number } | null>(null)
const isDrawing = ref(false)
const drawStartX = ref(0)
const drawStartY = ref(0)
const selectedBBox = ref<number | null>(null)
const pendingBBox = ref<{ x: number; y: number; width: number; height: number } | null>(null)

// 拖拽平移
const isPanning = ref(false)
const panStartX = ref(0)
const panStartY = ref(0)

// 只支持边界框的实体类型
const bboxEntityTypes = computed(() => {
  return props.entityTypes.filter(et => et.supports_bbox)
})

// 图片样式
const imageStyle = computed(() => {
  return {
    transform: `translate(${translateX.value}px, ${translateY.value}px) scale(${scale.value})`,
    transformOrigin: '0 0'
  }
})

// 处理图片加载
const handleImageLoad = () => {
  if (imageRef.value) {
    imageNaturalWidth.value = imageRef.value.naturalWidth
    imageNaturalHeight.value = imageRef.value.naturalHeight
  }
}

// 缩放
const zoomIn = () => {
  scale.value = Math.min(scale.value * 1.2, 5)
}

const zoomOut = () => {
  scale.value = Math.max(scale.value / 1.2, 0.1)
}

const resetZoom = () => {
  scale.value = 1
  translateX.value = 0
  translateY.value = 0
}

// 鼠标滚轮缩放
const handleWheel = (e: WheelEvent) => {
  e.preventDefault()
  if (e.deltaY < 0) {
    zoomIn()
  } else {
    zoomOut()
  }
}

// 整图标注：点击图片
const handleImageClick = (e: MouseEvent) => {
  if (props.readonly) return  // 只读模式下不允许标注
  if (annotationMode.value !== 'whole') return
  if (isDrawing.value) return

  // 显示标签选择菜单
  labelSelectorPosition.value = {
    x: e.clientX,
    y: e.clientY
  }
  showLabelSelector.value = true
}

// 整图标注：选择标签
const handleWholeImageLabel = (entityType: EntityType) => {
  const newEntity: Omit<ImageEntity, 'id'> = {
    entity_type_id: entityType.id,
    entity_type_name: entityType.type_name_zh,
    color: entityType.color
  }
  emit('add-whole-image-entity', newEntity)
  closeLabelSelector()
  ElMessage.success('整图标注添加成功')
}

// 关闭整图标签选择
const closeLabelSelector = () => {
  showLabelSelector.value = false
}

// 删除整图标注
const deleteWholeImageEntity = (id: number) => {
  emit('delete-whole-image-entity', id)
}

// 区域标注：鼠标按下
const handleMouseDown = (e: MouseEvent) => {
  if (props.readonly) return  // 只读模式下不允许绘制
  if (annotationMode.value !== 'region') return
  if (!imageRef.value) return

  const rect = imageRef.value.getBoundingClientRect()
  const x = (e.clientX - rect.left) / scale.value
  const y = (e.clientY - rect.top) / scale.value

  // 检查是否在图片范围内
  if (x < 0 || y < 0 || x > imageNaturalWidth.value || y > imageNaturalHeight.value) {
    return
  }

  isDrawing.value = true
  drawStartX.value = x
  drawStartY.value = y
  drawingBBox.value = {
    x: x * scale.value,
    y: y * scale.value,
    width: 0,
    height: 0
  }
}

// 区域标注：鼠标移动
const handleMouseMove = (e: MouseEvent) => {
  if (!isDrawing.value || !imageRef.value) return

  const rect = imageRef.value.getBoundingClientRect()
  const x = (e.clientX - rect.left) / scale.value
  const y = (e.clientY - rect.top) / scale.value

  const width = x - drawStartX.value
  const height = y - drawStartY.value

  drawingBBox.value = {
    x: Math.min(drawStartX.value, x) * scale.value,
    y: Math.min(drawStartY.value, y) * scale.value,
    width: Math.abs(width) * scale.value,
    height: Math.abs(height) * scale.value
  }
}

// 区域标注：鼠标释放
const handleMouseUp = (e: MouseEvent) => {
  if (!isDrawing.value || !drawingBBox.value) return

  isDrawing.value = false

  // 检查边界框大小
  if (drawingBBox.value.width < 10 || drawingBBox.value.height < 10) {
    drawingBBox.value = null
    ElMessage.warning('边界框太小，请重新绘制')
    return
  }

  // 保存待标注的边界框（原始坐标）
  pendingBBox.value = {
    x: drawingBBox.value.x / scale.value,
    y: drawingBBox.value.y / scale.value,
    width: drawingBBox.value.width / scale.value,
    height: drawingBBox.value.height / scale.value
  }

  // 显示标签选择菜单
  bboxLabelSelectorPosition.value = {
    x: e.clientX,
    y: e.clientY
  }
  showBBoxLabelSelector.value = true
  drawingBBox.value = null
}

// 区域标注：选择标签
const handleBBoxLabel = (entityType: EntityType) => {
  if (!pendingBBox.value) return

  const newBBox: Omit<BoundingBox, 'id'> = {
    ...pendingBBox.value,
    entity_type_id: entityType.id,
    entity_type_name: entityType.type_name_zh,
    color: entityType.color
  }

  emit('add-bbox', newBBox)
  closeBBoxLabelSelector()
  pendingBBox.value = null
  ElMessage.success('区域标注添加成功')
}

// 关闭区域标签选择
const closeBBoxLabelSelector = () => {
  showBBoxLabelSelector.value = false
  drawingBBox.value = null
  pendingBBox.value = null
}

// 选择边界框
const selectBBox = (id: number) => {
  selectedBBox.value = id
}

// 删除边界框
const deleteBBox = (id: number) => {
  emit('delete-bbox', id)
  if (selectedBBox.value === id) {
    selectedBBox.value = null
  }
}

// 删除选中的边界框
const deleteSelectedBBox = () => {
  if (selectedBBox.value) {
    deleteBBox(selectedBBox.value)
  }
}
</script>

<style scoped>
.image-annotation-editor {
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
  font-size: 13px;
  color: #909399;
  margin-left: auto;
}

.readonly-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #409eff;
  font-weight: 500;
}

.zoom-info {
  font-size: 14px;
  color: #606266;
  min-width: 50px;
}

.image-display-area {
  flex: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  gap: 20px;
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.image-container {
  flex: 1;
  position: relative;
  overflow: auto;
  cursor: grab;
}

.image-container.region-mode {
  cursor: crosshair;
}

.image-container img {
  display: block;
  max-width: none;
  user-select: none;
}

.bbox-layer {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: all;
}

.bbox-rect {
  cursor: pointer;
  transition: stroke-width 0.2s;
}

.bbox-rect:hover {
  stroke-width: 3 !important;
}

.bbox-rect.selected {
  stroke-width: 4 !important;
}

.bbox-label {
  font-size: 14px;
  font-weight: 500;
  pointer-events: none;
  text-shadow: 0 0 3px white, 0 0 3px white;
}

.side-panel {
  width: 300px;
  display: flex;
  flex-direction: column;
}

.annotation-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.list-header {
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
}

.list-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
}

.entity-items,
.bbox-items {
  padding: 8px;
}

.entity-item,
.bbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  margin-bottom: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.entity-item:hover,
.bbox-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.bbox-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.bbox-coords {
  flex: 1;
  font-size: 12px;
  color: #909399;
}
</style>
