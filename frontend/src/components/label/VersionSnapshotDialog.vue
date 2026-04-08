<template>
  <el-dialog
    v-model="dialogVisible"
    title="创建版本快照"
    width="600px"
  >
    <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
      <el-form-item label="版本名称" prop="version_name">
        <el-input v-model="formData.version_name" placeholder="如: v1.0.0" />
      </el-form-item>
      <el-form-item label="版本描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请描述此版本的主要变更"
        />
      </el-form-item>
      <el-alert
        title="提示"
        type="info"
        :closable="false"
        style="margin-bottom: 20px;"
      >
        创建快照将保存当前所有实体类型和关系类型的配置，包括定义、示例等信息。
      </el-alert>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="loading">创建</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import { useUserStore } from '@/stores/user'

interface Props {
  visible: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
  'success': []
}>()

const labelStore = useLabelStore()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const formData = ref({
  version_name: '',
  description: ''
})

const rules: FormRules = {
  version_name: [{ required: true, message: '请输入版本名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入版本描述', trigger: 'blur' }]
}

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      await labelStore.createSnapshot({
        version_name: formData.value.version_name,
        description: formData.value.description,
        created_by: userStore.currentUser?.id || 1
      })
      emit('success')
      dialogVisible.value = false
      formData.value = {
        version_name: '',
        description: ''
      }
    } catch (error) {
      ElMessage.error('创建失败')
    } finally {
      loading.value = false
    }
  })
}
</script>
