<template>
  <svg
    class="relation-arrow-layer"
    :width="width"
    :height="height"
    preserveAspectRatio="xMinYMin meet"
    @click="handleLayerClick"
  >
    <!-- 箭头标记定义 -->
    <defs>
      <marker
        v-for="relation in relations"
        :key="`marker-${relation.id}`"
        :id="`arrow-${relation.id}`"
        markerWidth="10"
        markerHeight="10"
        refX="9"
        refY="3"
        orient="auto"
        markerUnits="strokeWidth"
      >
        <polygon
          points="0 0, 10 3, 0 6"
          :fill="getRelationColor(relation)"
        />
      </marker>
    </defs>

    <!-- 绘制关系箭头 -->
    <g v-for="relation in relations" :key="relation.id">
      <!-- 箭头路径 -->
      <path
        :d="getArrowPath(relation)"
        :stroke="getRelationColor(relation)"
        :stroke-width="isSelected(relation.id) ? 3 : 2"
        fill="none"
        stroke-linecap="round"
        stroke-linejoin="round"
        :marker-end="`url(#arrow-${relation.id})`"
        :class="{ 
          'relation-arrow': true, 
          'selected': isSelected(relation.id),
          'hovered': hoveredRelationId === relation.id
        }"
        @click.stop="handleArrowClick(relation)"
        @mouseenter="hoveredRelationId = relation.id"
        @mouseleave="hoveredRelationId = null"
      />

      <!-- 关系标签 -->
      <g v-if="showLabels">
        <rect
          :x="getLabelPosition(relation).x - 35"
          :y="getLabelPosition(relation).y - 14"
          width="70"
          height="28"
          rx="6"
          :fill="getRelationColor(relation)"
          opacity="0.95"
        />
        <text
          :x="getLabelPosition(relation).x"
          :y="getLabelPosition(relation).y"
          class="relation-label"
          text-anchor="middle"
          dominant-baseline="middle"
        >
          {{ relation.relation_type_name }}
        </text>
      </g>
    </g>

    <!-- 临时箭头（创建关系时） -->
    <path
      v-if="tempArrow"
      :d="tempArrow.path"
      stroke="#409eff"
      stroke-width="2"
      stroke-dasharray="5,5"
      fill="none"
      marker-end="url(#temp-arrow)"
    />
    <defs v-if="tempArrow">
      <marker
        id="temp-arrow"
        markerWidth="10"
        markerHeight="10"
        refX="9"
        refY="3"
        orient="auto"
        markerUnits="strokeWidth"
      >
        <path d="M0,0 L0,6 L9,3 z" fill="#409eff" />
      </marker>
    </defs>
  </svg>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

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
  source_entity_id: string  // 字符串格式的entity_id
  target_entity_id: string  // 字符串格式的entity_id
  relation_type_id: number
  relation_type_name: string
  color?: string
}

interface EntityPosition {
  x: number
  y: number
  width: number
  height: number
}

interface Props {
  relations: Relation[]
  entities: Entity[]
  entityPositions: Map<string, EntityPosition>  // 键改为字符串类型的entity_id
  selectedRelationId?: number | null
  showLabels?: boolean
  width?: number
  height?: number
}

interface Emits {
  (e: 'select', relationId: number): void
  (e: 'delete', relationId: number): void
}

const props = withDefaults(defineProps<Props>(), {
  selectedRelationId: null,
  showLabels: true,
  width: 0,
  height: 0
})

const emit = defineEmits<Emits>()

const hoveredRelationId = ref<number | null>(null)
const tempArrow = ref<{ path: string } | null>(null)

// 判断关系是否被选中
const isSelected = (relationId?: number) => {
  return relationId === props.selectedRelationId
}

// 获取关系颜色
const getRelationColor = (relation: Relation): string => {
  if (relation.color) return relation.color
  return '#409eff' // 默认蓝色
}

// 获取实体位置
const getEntityPosition = (entityId: string): EntityPosition | null => {
  return props.entityPositions.get(entityId) || null
}

/**
 * 计算箭头路径（优化方案：同行在上方，跨行从侧边）
 */
const getArrowPath = (relation: Relation): string => {
  const sourcePos = getEntityPosition(relation.source_entity_id)
  const targetPos = getEntityPosition(relation.target_entity_id)

  if (!sourcePos || !targetPos) {
    return ''
  }

  // 圆角半径
  const radius = 8

  // 计算中心点
  const sourceCenterX = sourcePos.x + sourcePos.width / 2
  const sourceCenterY = sourcePos.y + sourcePos.height / 2
  const targetCenterX = targetPos.x + targetPos.width / 2
  const targetCenterY = targetPos.y + targetPos.height / 2

  // 计算距离
  const dx = targetCenterX - sourceCenterX
  const dy = targetCenterY - sourceCenterY

  // 判断是否同行（垂直距离小于实体高度）
  const isSameLine = Math.abs(dy) < sourcePos.height

  let path = ''

  if (isSameLine) {
    // ========== 同一行：统一在上方绘制 ==========
    
    // 起点和终点：从实体上边缘中心出发
    const startX = sourceCenterX
    const startY = sourcePos.y
    const endX = targetCenterX
    const endY = targetPos.y

    // 计算箭头高度（根据关系ID分层，避免重叠）
    const layerIndex = (relation.id || 0) % 3
    const arcHeight = 40 + layerIndex * 30 // 40, 70, 100

    // 水平线的Y坐标（在实体上方）
    const horizontalY = Math.min(startY, endY) - arcHeight

    // 绘制路径
    path = `M ${startX} ${startY}`
    
    // 向上到水平线
    if (Math.abs(horizontalY - startY) > radius) {
      path += ` L ${startX} ${horizontalY + radius}`
      path += ` Q ${startX} ${horizontalY} ${startX + Math.sign(dx) * radius} ${horizontalY}`
    } else {
      path += ` L ${startX} ${horizontalY}`
    }

    // 水平线
    path += ` L ${endX - Math.sign(dx) * radius} ${horizontalY}`

    // 向下到终点
    path += ` Q ${endX} ${horizontalY} ${endX} ${horizontalY + radius}`
    path += ` L ${endX} ${endY}`

  } else {
    // ========== 跨行：从侧边连接 ==========
    
    let startX, startY, endX, endY

    // 判断方向
    const isDownward = dy > 0 // 从上到下
    const isRightward = dx > 0 // 从左到右

    if (isDownward) {
      // 从上到下
      if (isRightward) {
        // 右下方：从右边出发，到左边
        startX = sourcePos.x + sourcePos.width
        startY = sourceCenterY
        endX = targetPos.x
        endY = targetCenterY
      } else {
        // 左下方：从左边出发，到右边
        startX = sourcePos.x
        startY = sourceCenterY
        endX = targetPos.x + targetPos.width
        endY = targetCenterY
      }
    } else {
      // 从下到上
      if (isRightward) {
        // 右上方：从右边出发，到左边
        startX = sourcePos.x + sourcePos.width
        startY = sourceCenterY
        endX = targetPos.x
        endY = targetCenterY
      } else {
        // 左上方：从左边出发，到右边
        startX = sourcePos.x
        startY = sourceCenterY
        endX = targetPos.x + targetPos.width
        endY = targetCenterY
      }
    }

    // 计算中间转折点
    const midX = (startX + endX) / 2
    const midY = (startY + endY) / 2

    // 绘制Z字形路径
    path = `M ${startX} ${startY}`

    const horizontalLength = Math.abs(endX - startX)
    const verticalLength = Math.abs(endY - startY)

    if (horizontalLength > radius * 2 && verticalLength > radius * 2) {
      // 标准Z字形
      // 水平到中点
      path += ` L ${midX - Math.sign(dx) * radius} ${startY}`
      path += ` Q ${midX} ${startY} ${midX} ${startY + Math.sign(dy) * radius}`
      
      // 垂直到中点
      path += ` L ${midX} ${endY - Math.sign(dy) * radius}`
      path += ` Q ${midX} ${endY} ${midX + Math.sign(dx) * radius} ${endY}`
      
      // 水平到终点
      path += ` L ${endX} ${endY}`
    } else {
      // 距离太短，简化路径
      path += ` Q ${midX} ${startY} ${midX} ${midY}`
      path += ` Q ${midX} ${endY} ${endX} ${endY}`
    }
  }

  return path
}

// 获取标签位置（在箭头的水平段中点）
const getLabelPosition = (relation: Relation) => {
  const sourcePos = getEntityPosition(relation.source_entity_id)
  const targetPos = getEntityPosition(relation.target_entity_id)

  if (!sourcePos || !targetPos) {
    return { x: 0, y: 0 }
  }

  const sourceCenterX = sourcePos.x + sourcePos.width / 2
  const sourceCenterY = sourcePos.y + sourcePos.height / 2
  const targetCenterX = targetPos.x + targetPos.width / 2
  const targetCenterY = targetPos.y + targetPos.height / 2

  const dy = targetCenterY - sourceCenterY
  const isSameLine = Math.abs(dy) < sourcePos.height

  if (isSameLine) {
    // 同一行：标签在上方的水平线上
    const layerIndex = (relation.id || 0) % 3
    const arcHeight = 40 + layerIndex * 30
    const labelY = Math.min(sourcePos.y, targetPos.y) - arcHeight

    return {
      x: (sourceCenterX + targetCenterX) / 2,
      y: labelY
    }
  } else {
    // 跨行：标签在中间位置
    return {
      x: (sourceCenterX + targetCenterX) / 2,
      y: (sourceCenterY + targetCenterY) / 2
    }
  }
}

// 处理箭头点击
const handleArrowClick = (relation: Relation) => {
  if (relation.id) {
    emit('select', relation.id)
  }
}

// 处理图层点击（取消选择）
const handleLayerClick = () => {
  // 点击空白处取消选择
}

// 更新临时箭头（用于创建关系时的预览）
const updateTempArrow = (sourceEntityId: number, mouseX: number, mouseY: number) => {
  const sourcePos = getEntityPosition(sourceEntityId)
  if (!sourcePos) return

  const start = {
    x: sourcePos.x + sourcePos.width / 2,
    y: sourcePos.y + sourcePos.height / 2
  }

  tempArrow.value = {
    path: `M ${start.x} ${start.y} L ${mouseX} ${mouseY}`
  }
}

// 清除临时箭头
const clearTempArrow = () => {
  tempArrow.value = null
}

// 暴露方法给父组件
defineExpose({
  updateTempArrow,
  clearTempArrow
})
</script>

<style scoped>
.relation-arrow-layer {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 10;
  overflow: visible;  /* 确保箭头不被裁剪 */
}

.relation-arrow {
  cursor: pointer;
  transition: all 0.2s ease;
  pointer-events: all;
}

.relation-arrow:hover {
  stroke-width: 3 !important;
  filter: brightness(1.2);
}

.relation-arrow.selected {
  stroke-width: 4 !important;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.relation-label {
  fill: white;
  font-size: 12px;
  font-weight: 600;
  pointer-events: none;
  user-select: none;
}
</style>
