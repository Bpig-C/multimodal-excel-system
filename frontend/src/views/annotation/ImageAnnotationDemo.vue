<template>
  <div class="image-annotation-demo">
    <div class="page-header">
      <h2>图片标注编辑器</h2>
      <div class="actions">
        <el-button @click="handleSave">保存</el-button>
        <el-button type="primary" @click="handleSubmit">提交复核</el-button>
      </div>
    </div>

    <div class="editor-container">
      <ImageAnnotationEditor
        :image-url="sampleImageUrl"
        :whole-image-entities="wholeImageEntities"
        :bboxes="bboxes"
        :entity-types="entityTypes"
        @add-whole-image-entity="handleAddWholeImageEntity"
        @delete-whole-image-entity="handleDeleteWholeImageEntity"
        @add-bbox="handleAddBBox"
        @update-bbox="handleUpdateBBox"
        @delete-bbox="handleDeleteBBox"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import ImageAnnotationEditor from '@/components/annotation/ImageAnnotationEditor.vue'
import { useLabelStore } from '@/stores/label'
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

const labelStore = useLabelStore()

// 示例图片URL（可以替换为实际图片）
const sampleImageUrl = ref('https://via.placeholder.com/800x600/e3f2fd/2196f3?text=Sample+Image')

const wholeImageEntities = ref<ImageEntity[]>([])
const bboxes = ref<BoundingBox[]>([])
const entityTypes = ref<EntityType[]>([])
let nextWholeImageEntityId = 1
let nextBBoxId = 1

// 加载标签配置
onMounted(async () => {
  try {
    await labelStore.fetchEntityTypes({ include_inactive: false })
    entityTypes.value = labelStore.entityTypes
  } catch (error) {
    ElMessage.error('加载标签配置失败')
  }
})

const handleAddWholeImageEntity = (entity: Omit<ImageEntity, 'id'>) => {
  const newEntity: ImageEntity = {
    ...entity,
    id: nextWholeImageEntityId++
  }
  wholeImageEntities.value.push(newEntity)
}

const handleDeleteWholeImageEntity = (id: number) => {
  wholeImageEntities.value = wholeImageEntities.value.filter(e => e.id !== id)
}

const handleAddBBox = (bbox: Omit<BoundingBox, 'id'>) => {
  const newBBox: BoundingBox = {
    ...bbox,
    id: nextBBoxId++
  }
  bboxes.value.push(newBBox)
}

const handleUpdateBBox = (id: number, updates: Partial<BoundingBox>) => {
  const index = bboxes.value.findIndex(b => b.id === id)
  if (index !== -1) {
    bboxes.value[index] = { ...bboxes.value[index], ...updates }
  }
}

const handleDeleteBBox = (id: number) => {
  bboxes.value = bboxes.value.filter(b => b.id !== id)
}

const handleSave = () => {
  ElMessage.success('保存成功')
  console.log('Whole Image Entities:', wholeImageEntities.value)
  console.log('Bounding Boxes:', bboxes.value)
}

const handleSubmit = () => {
  ElMessage.success('提交复核成功')
}
</script>

<style scoped>
.image-annotation-demo {
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
}
</style>
