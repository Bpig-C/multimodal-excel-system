<template>
  <el-dialog
    v-model="dialogVisible"
    title="创建数据集"
    width="90%"
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

      <el-form-item label="选择语料" required>
        <div class="corpus-selector-wrapper">
          <CorpusSelector ref="corpusSelectorRef" />
        </div>
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
          创建数据集
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, h } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useDatasetStore, useAuthStore } from '@/stores'
import CorpusSelector from './CorpusSelector.vue'

interface Props {
  modelValue: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const datasetStore = useDatasetStore()
const authStore = useAuthStore()

// 状态
const formRef = ref<FormInstance>()
const corpusSelectorRef = ref<InstanceType<typeof CorpusSelector>>()
const loading = ref(false)

const formData = ref({
  name: '',
  description: ''
  // 移除 corpus_ids，因为它不是表单字段，而是从 CorpusSelector 获取的
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

// 方法
const handleClose = () => {
  formRef.value?.resetFields()
  corpusSelectorRef.value?.clearSelection()
  dialogVisible.value = false
}

const handleSubmit = async () => {
  try {
    // 验证表单
    await formRef.value?.validate()

    // 获取选中的语料完整信息
    const selectedCorpus = corpusSelectorRef.value?.getSelectedCorpus() || []
    
    if (selectedCorpus.length === 0) {
      ElMessage.warning('请至少选择一条语料')
      return
    }

    // 提取数据库ID
    const corpusIds = selectedCorpus
      .map(corpus => corpus.id)
      .filter((id): id is number => id !== undefined)

    if (corpusIds.length === 0) {
      ElMessage.error('无法获取语料ID，请重试')
      return
    }

    if (corpusIds.length !== selectedCorpus.length) {
      ElMessage.warning(`部分语料缺少ID信息，将创建 ${corpusIds.length} 个任务`)
    }

    // 确认创建（VNode格式，支持换行）
    const confirmMessageVNode = h('div', [
      h('div', '即将创建数据集：'),
      h('div', [
        h('div', [`- 名称：${formData.value.name}`]),
        h('div', [`- 选中语料：${corpusIds.length} 条`]),
        h('div', [`- 将创建 ${corpusIds.length} 个标注任务`]),
      ]),
      h('div', { style: 'margin-top: 8px;' }, '确认创建吗？')
    ])
    await ElMessageBox.confirm(confirmMessageVNode, '确认创建', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })

    loading.value = true

    // 调用API创建数据集
    await datasetStore.create({
      name: formData.value.name,
      description: formData.value.description,
      corpus_ids: corpusIds,  // 使用数据库ID
      created_by: authStore.user?.id || 1
    })

    ElMessage.success('数据集创建成功')
    emit('success')
    handleClose()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('创建数据集失败:', error)
      ElMessage.error(error.message || '创建失败')
    }
  } finally {
    loading.value = false
  }
}

// 监听对话框打开，重置表单
watch(dialogVisible, (newVal) => {
  if (newVal) {
    formData.value = {
      name: '',
      description: ''
    }
  }
})
</script>

<style scoped lang="scss">
.corpus-selector-wrapper {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 16px;
  background: #fafafa;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
