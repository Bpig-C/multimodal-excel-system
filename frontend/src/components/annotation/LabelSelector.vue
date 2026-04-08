<template>
  <teleport to="body">
    <div
      v-if="visible"
      class="label-selector"
      :style="{ left: `${position.x}px`, top: `${position.y}px` }"
      @click.stop
    >
      <div class="label-selector-header">
        <span>选择实体类型</span>
        <el-icon class="close-icon" @click="handleClose">
          <Close />
        </el-icon>
      </div>
      
      <el-scrollbar max-height="300px">
        <div class="label-list">
          <div
            v-for="entityType in entityTypes"
            :key="entityType.id"
            class="label-item"
            @click="handleSelect(entityType)"
          >
            <el-tag
              :color="entityType.color"
              :style="{ backgroundColor: entityType.color, color: '#fff', border: 'none' }"
            >
              {{ entityType.type_name_zh }}
            </el-tag>
            <span class="label-description">{{ entityType.description }}</span>
          </div>
        </div>
      </el-scrollbar>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { Close } from '@element-plus/icons-vue'
import type { EntityType } from '@/api/label'

interface Props {
  position: { x: number; y: number }
  entityTypes: EntityType[]
}

interface Emits {
  (e: 'select', entityType: EntityType): void
  (e: 'close'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const visible = ref(true)

console.log('[LabelSelector] Created with props:', {
  position: props.position,
  entityTypesCount: props.entityTypes.length,
  entityTypes: props.entityTypes
})

const handleSelect = (entityType: EntityType) => {
  emit('select', entityType)
}

const handleClose = () => {
  visible.value = false
  emit('close')
}

// 点击外部关闭
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.label-selector')) {
    handleClose()
  }
}

onMounted(() => {
  // 延迟添加点击外部监听器，避免与触发选择的 mouseup 事件冲突
  setTimeout(() => {
    document.addEventListener('click', handleClickOutside)
  }, 100)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.label-selector {
  position: fixed;
  z-index: 9999;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  min-width: 250px;
  max-width: 400px;
  transform: translateX(-50%);
}

.label-selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
  font-weight: 500;
}

.close-icon {
  cursor: pointer;
  font-size: 16px;
}

.close-icon:hover {
  color: #409eff;
}

.label-list {
  padding: 8px 0;
}

.label-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.label-item:hover {
  background-color: #f5f7fa;
}

.label-description {
  flex: 1;
  font-size: 13px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
