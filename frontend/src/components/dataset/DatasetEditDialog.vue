<template>
  <el-dialog
    v-model="dialogVisible"
    title="编辑数据集"
    width="500px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="数据集名称" prop="name">
        <el-input
          v-model="formData.name"
          placeholder="请输入数据集名称"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="数据集描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入数据集描述（可选）"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleSubmit"
        >
          保存
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useDatasetStore } from '@/stores'
import type { Dataset } from '@/api/dataset'

interface Props {
  modelValue: boolean
  dataset?: Dataset
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const datasetStore = useDatasetStore()

// 状态
const formRef = ref<FormInstance>()
const loading = ref(false)

const formData = ref({
  name: '',
  description: ''
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入数据集名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ]
}

// 计算属性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 监听对话框打开，填充数据
watch(dialogVisible, (newVal) => {
  if (newVal && props.dataset) {
    formData.value = {
      name: props.dataset.name || '',
      description: props.dataset.description || ''
    }
  }
})

// 方法
const handleClose = () => {
  formRef.value?.resetFields()
  dialogVisible.value = false
}

const handleSubmit = async () => {
  try {
    // 验证表单
    await formRef.value?.validate()

    if (!props.dataset) {
      ElMessage.error('数据集信息缺失')
      return
    }

    loading.value = true

    // 调用API更新数据集
    await datasetStore.update(props.dataset.dataset_id, {
      name: formData.value.name,
      description: formData.value.description
    })

    ElMessage.success('数据集更新成功')
    emit('success')
    handleClose()
  } catch (error: any) {
    console.error('更新数据集失败:', error)
    ElMessage.error(error.message || '更新失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
