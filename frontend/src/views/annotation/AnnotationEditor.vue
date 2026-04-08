<template>
  <div class="annotation-editor-page">
    <div class="page-header">
      <h2>文本标注编辑器</h2>
      <div class="actions">
        <el-button @click="handleSave">保存</el-button>
        <el-button type="primary" @click="handleSubmit">提交复核</el-button>
      </div>
    </div>

    <div class="editor-container">
      <TextAnnotationEditor
        :text="sampleText"
        :entities="entities"
        :relations="relations"
        :entity-types="entityTypes"
        :relation-types="relationTypes"
        @add-entity="handleAddEntity"
        @update-entity="handleUpdateEntity"
        @delete-entity="handleDeleteEntity"
        @add-relation="handleAddRelation"
        @delete-relation="handleDeleteRelation"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import TextAnnotationEditor from '@/components/annotation/TextAnnotationEditor.vue'
import { useLabelStore } from '@/stores/label'
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
  source_entity_id: number
  target_entity_id: number
  relation_type_id: number
  relation_type_name: string
}

const labelStore = useLabelStore()

// 示例文本
const sampleText = ref(`某客户反馈产品型号ABC-123在使用过程中出现了屏幕闪烁的问题。经检查发现，该批次产品在2024年1月15日生产，使用的是供应商XYZ提供的显示屏。

初步分析认为，问题可能是由于焊接工艺参数设置不当导致的。具体表现为焊接温度过高（实际温度350℃，标准温度应为320℃），导致显示屏排线接触不良。

处置措施：
1. 立即停止使用该批次产品
2. 对所有同批次产品进行全面检查
3. 调整焊接设备温度参数
4. 对操作人员进行再培训

改进措施：
1. 建立更严格的工艺参数监控机制
2. 增加产品出厂前的质量检测项目
3. 与供应商XYZ协商改进显示屏质量`)

const entities = ref<Entity[]>([])
const relations = ref<Relation[]>([])
const entityTypes = ref<EntityType[]>([])
const relationTypes = ref<RelationType[]>([])
let nextEntityId = 1
let nextRelationId = 1

// 加载标签配置
onMounted(async () => {
  try {
    await labelStore.fetchEntityTypes({ include_inactive: false })
    await labelStore.fetchRelationTypes({ include_inactive: false })
    entityTypes.value = labelStore.entityTypes
    relationTypes.value = labelStore.relationTypes
  } catch (error) {
    ElMessage.error('加载标签配置失败')
  }
})

const handleAddEntity = (entity: Omit<Entity, 'id'>) => {
  const newEntity: Entity = {
    ...entity,
    id: nextEntityId++
  }
  entities.value.push(newEntity)
  ElMessage.success('实体添加成功')
}

const handleUpdateEntity = (id: number, updates: Partial<Entity>) => {
  const index = entities.value.findIndex(e => e.id === id)
  if (index !== -1) {
    entities.value[index] = { ...entities.value[index], ...updates }
    ElMessage.success('实体更新成功')
  }
}

const handleDeleteEntity = (id: number) => {
  entities.value = entities.value.filter(e => e.id !== id)
  // 同时删除相关的关系
  relations.value = relations.value.filter(
    r => r.source_entity_id !== id && r.target_entity_id !== id
  )
  ElMessage.success('实体删除成功')
}

const handleAddRelation = (relation: Omit<Relation, 'id'>) => {
  const newRelation: Relation = {
    ...relation,
    id: nextRelationId++
  }
  relations.value.push(newRelation)
  ElMessage.success('关系添加成功')
}

const handleDeleteRelation = (id: number) => {
  relations.value = relations.value.filter(r => r.id !== id)
  ElMessage.success('关系删除成功')
}

const handleSave = () => {
  ElMessage.success('保存成功')
  console.log('Entities:', entities.value)
  console.log('Relations:', relations.value)
}

const handleSubmit = () => {
  ElMessage.success('提交复核成功')
}
</script>

<style scoped>
.annotation-editor-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 10px;
}

.editor-container {
  flex: 1;
  overflow: hidden;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
}
</style>
