<template>
  <el-dialog
    v-model="visible"
    title="选择关系类型"
    width="500px"
    @close="handleClose"
  >
    <div class="relation-info">
      <div class="entity-box">
        <span class="label">源实体</span>
        <div class="entity-text">{{ sourceEntity?.text }}</div>
      </div>
      <el-icon class="arrow-icon"><Right /></el-icon>
      <div class="entity-box">
        <span class="label">目标实体</span>
        <div class="entity-text">{{ targetEntity?.text }}</div>
      </div>
    </div>

    <el-divider />

    <div class="relation-types">
      <div
        v-for="relationType in relationTypes"
        :key="relationType.id"
        class="relation-type-item"
        @click="handleSelect(relationType)"
      >
        <el-tag
          :color="relationType.color"
          :style="{ backgroundColor: relationType.color, color: '#fff', border: 'none' }"
        >
          {{ relationType.type_name_zh }}
        </el-tag>
        <span class="description">{{ relationType.description }}</span>
      </div>
    </div>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Right } from '@element-plus/icons-vue'
import type { RelationType } from '@/api/label'

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
  modelValue: boolean
  sourceEntity: Entity | null
  targetEntity: Entity | null
  relationTypes: RelationType[]
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'select', relationType: RelationType): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleSelect = (relationType: RelationType) => {
  emit('select', relationType)
  visible.value = false
}

const handleClose = () => {
  visible.value = false
}
</script>

<style scoped>
.relation-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.entity-box {
  flex: 1;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.entity-box .label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
}

.entity-box .entity-text {
  font-size: 14px;
  color: #303133;
  word-break: break-word;
  line-height: 1.5;
}

.arrow-icon {
  font-size: 24px;
  color: #409eff;
}

.relation-types {
  max-height: 400px;
  overflow-y: auto;
}

.relation-type-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.relation-type-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.description {
  flex: 1;
  font-size: 13px;
  color: #606266;
}
</style>
