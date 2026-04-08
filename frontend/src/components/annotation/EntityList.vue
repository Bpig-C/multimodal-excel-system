<template>
  <div class="entity-list">
    <div class="list-header">
      <h3>实体列表 ({{ entities.length }})</h3>
    </div>

    <el-scrollbar>
      <div class="entity-items">
        <div
          v-for="entity in sortedEntities"
          :key="entity.id"
          class="entity-item"
          :class="{ selected: selectedEntityId === entity.id }"
          @click="handleSelect(entity.id!)"
        >
          <div class="entity-header">
            <el-tag
              :color="entity.color"
              :style="{ backgroundColor: entity.color, color: '#fff', border: 'none' }"
              size="small"
            >
              {{ entity.entity_type_name }}
            </el-tag>
            <el-button
              type="danger"
              size="small"
              text
              @click.stop="handleDelete(entity.id!)"
            >
              删除
            </el-button>
          </div>

          <div class="entity-text">
            "{{ entity.text }}"
          </div>

          <div class="entity-meta">
            <span class="offset-info">
              偏移量: {{ entity.start_offset }} - {{ entity.end_offset }}
            </span>
          </div>
        </div>

        <el-empty
          v-if="entities.length === 0"
          description="暂无实体"
          :image-size="80"
        />
      </div>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Entity {
  id?: number
  text: string
  start_offset: number
  end_offset: number
  entity_type_id: number
  entity_type_name: string
  color: string
}

interface Props {
  entities: Entity[]
  text: string
}

interface Emits {
  (e: 'select', entityId: number): void
  (e: 'delete', entityId: number): void
  (e: 'update', entityId: number, updates: Partial<Entity>): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const selectedEntityId = ref<number | null>(null)

// 按偏移量排序实体
const sortedEntities = computed(() => {
  return [...props.entities].sort((a, b) => a.start_offset - b.start_offset)
})

const handleSelect = (entityId: number) => {
  selectedEntityId.value = entityId
  emit('select', entityId)
}

const handleDelete = (entityId: number) => {
  emit('delete', entityId)
  if (selectedEntityId.value === entityId) {
    selectedEntityId.value = null
  }
}
</script>

<style scoped>
.entity-list {
  display: flex;
  flex-direction: column;
  height: 50%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
}

.list-header {
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
}

.list-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.entity-items {
  padding: 8px;
}

.entity-item {
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.entity-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.entity-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.entity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.entity-text {
  font-size: 14px;
  color: #303133;
  margin-bottom: 8px;
  word-break: break-word;
  line-height: 1.5;
}

.entity-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.offset-info {
  font-size: 12px;
  color: #909399;
}
</style>
