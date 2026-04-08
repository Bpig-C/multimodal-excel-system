<template>
  <div class="relation-list">
    <div class="list-header">
      <h3>关系列表 ({{ relations.length }})</h3>
    </div>

    <el-scrollbar>
      <div class="relation-items">
        <div
          v-for="relation in relations"
          :key="relation.id"
          class="relation-item"
          :class="{ selected: selectedRelationId === relation.id }"
          @click="handleSelect(relation.id!)"
        >
          <div class="relation-header">
            <el-tag type="info" size="small">
              {{ relation.relation_type_name }}
            </el-tag>
            <el-button
              type="danger"
              size="small"
              text
              @click.stop="handleDelete(relation.id!)"
            >
              删除
            </el-button>
          </div>

          <div class="relation-content">
            <div class="entity-box source">
              <span class="entity-label">源实体</span>
              <div class="entity-text">
                {{ getEntityText(relation.source_entity_id) }}
              </div>
            </div>

            <div class="arrow">
              <el-icon><Right /></el-icon>
            </div>

            <div class="entity-box target">
              <span class="entity-label">目标实体</span>
              <div class="entity-text">
                {{ getEntityText(relation.target_entity_id) }}
              </div>
            </div>
          </div>
        </div>

        <el-empty
          v-if="relations.length === 0"
          description="暂无关系"
          :image-size="80"
        />
      </div>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Right } from '@element-plus/icons-vue'

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
  source_entity_id: number
  target_entity_id: number
  relation_type_id: number
  relation_type_name: string
}

interface Props {
  relations: Relation[]
  entities: Entity[]
}

interface Emits {
  (e: 'select', relationId: number): void
  (e: 'delete', relationId: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const selectedRelationId = ref<number | null>(null)

const getEntityText = (entityId: number): string => {
  const entity = props.entities.find(e => e.id === entityId)
  return entity ? entity.text : '未知实体'
}

const handleSelect = (relationId: number) => {
  selectedRelationId.value = relationId
  emit('select', relationId)
}

const handleDelete = (relationId: number) => {
  emit('delete', relationId)
  if (selectedRelationId.value === relationId) {
    selectedRelationId.value = null
  }
}
</script>

<style scoped>
.relation-list {
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

.relation-items {
  padding: 8px;
}

.relation-item {
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.relation-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.relation-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.relation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.relation-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.entity-box {
  flex: 1;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.entity-label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.entity-text {
  font-size: 13px;
  color: #303133;
  word-break: break-word;
  line-height: 1.4;
}

.arrow {
  font-size: 18px;
  color: #409eff;
}
</style>
