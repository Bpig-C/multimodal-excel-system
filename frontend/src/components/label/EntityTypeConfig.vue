<template>
  <div class="entity-type-config">
    <div class="toolbar">
      <el-button type="primary" @click="handleCreate">新建实体类型</el-button>
      <el-space>
        <el-checkbox v-model="showInactive">显示已停用</el-checkbox>
        <el-checkbox v-model="showUnreviewed">显示未审核</el-checkbox>
      </el-space>
    </div>

    <el-table :data="filteredEntityTypes" v-loading="labelStore.loading">
      <el-table-column prop="type_name" label="类型名称" width="150" />
      <el-table-column prop="type_name_zh" label="中文名称" width="150" />
      <el-table-column label="颜色" width="100">
        <template #default="{ row }">
          <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
            {{ row.type_name_zh }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="支持边界框" width="100">
        <template #default="{ row }">
          <el-tag :type="row.supports_bbox ? 'success' : 'info'" size="small">
            {{ row.supports_bbox ? '是' : '否' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="审核状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_reviewed ? 'success' : 'warning'" size="small">
            {{ row.is_reviewed ? '已审核' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '启用' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" @click="handleGenerateDefinition(row)">生成定义</el-button>
          <el-button size="small" @click="handleReview(row)" v-if="!row.is_reviewed">审核</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑实体类型' : '新建实体类型'"
      width="600px"
    >
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="类型名称" prop="type_name">
          <el-input v-model="formData.type_name" placeholder="英文名称，如 Product" />
        </el-form-item>
        <el-form-item label="中文名称" prop="type_name_zh">
          <el-input v-model="formData.type_name_zh" placeholder="中文名称，如 产品" />
        </el-form-item>
        <el-form-item label="颜色" prop="color">
          <el-color-picker v-model="formData.color" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="支持边界框">
          <el-switch v-model="formData.supports_bbox" />
        </el-form-item>
        <el-form-item label="启用状态" v-if="isEdit">
          <el-switch v-model="formData.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 审核对话框 -->
    <DefinitionReview
      v-model:visible="reviewDialogVisible"
      :entity-type="currentEntityType"
      @success="handleReviewSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { EntityType } from '@/api/label'
import DefinitionReview from './DefinitionReview.vue'

const labelStore = useLabelStore()
const showInactive = ref(false)
const showUnreviewed = ref(true)  // 默认显示未审核的标签（包括默认配置）
const dialogVisible = ref(false)
const reviewDialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const currentEntityType = ref<EntityType | null>(null)

const formData = ref({
  type_name: '',
  type_name_zh: '',
  color: '#409EFF',
  description: '',
  supports_bbox: false,
  is_active: true
})

const rules: FormRules = {
  type_name: [{ required: true, message: '请输入类型名称', trigger: 'blur' }],
  type_name_zh: [{ required: true, message: '请输入中文名称', trigger: 'blur' }],
  color: [{ required: true, message: '请选择颜色', trigger: 'change' }]
}

const filteredEntityTypes = computed(() => {
  return labelStore.entityTypes.filter(et => {
    if (!showInactive.value && !et.is_active) return false
    if (!showUnreviewed.value && !et.is_reviewed) return false
    return true
  })
})

const handleCreate = () => {
  isEdit.value = false
  formData.value = {
    type_name: '',
    type_name_zh: '',
    color: '#409EFF',
    description: '',
    supports_bbox: false,
    is_active: true
  }
  dialogVisible.value = true
}

const handleEdit = (row: EntityType) => {
  isEdit.value = true
  formData.value = {
    type_name: row.type_name,
    type_name_zh: row.type_name_zh,
    color: row.color,
    description: row.description || '',
    supports_bbox: row.supports_bbox,
    is_active: row.is_active
  }
  currentEntityType.value = row
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      if (isEdit.value && currentEntityType.value) {
        await labelStore.updateEntityType(currentEntityType.value.id, formData.value)
        ElMessage.success('更新成功')
      } else {
        await labelStore.createEntityType(formData.value)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    }
  })
}

const handleGenerateDefinition = async (row: EntityType) => {
  try {
    await ElMessageBox.confirm('确定要使用LLM生成该实体类型的定义吗？', '提示', {
      type: 'warning'
    })
    await labelStore.generateEntityDefinition(row.id)
    ElMessage.success('定义生成成功，请审核')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('生成失败')
    }
  }
}

const handleReview = (row: EntityType) => {
  currentEntityType.value = row
  reviewDialogVisible.value = true
}

const handleReviewSuccess = () => {
  ElMessage.success('审核成功')
  labelStore.fetchEntityTypes()
}

const handleDelete = async (row: EntityType) => {
  try {
    await ElMessageBox.confirm('确定要删除该实体类型吗？', '警告', {
      type: 'warning'
    })
    await labelStore.deleteEntityType(row.id)
    ElMessage.success('删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  labelStore.fetchEntityTypes({ include_inactive: true, include_unreviewed: true })
})
</script>

<style scoped>
.entity-type-config {
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
