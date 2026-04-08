<template>
  <el-dialog
    v-model="dialogVisible"
    :title="mode === 'import' ? '导入标签配置' : '导出标签配置'"
    width="600px"
  >
    <div v-if="mode === 'import'">
      <el-upload
        drag
        :auto-upload="false"
        :on-change="handleFileChange"
        :limit="1"
        accept=".json"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            只能上传JSON格式的配置文件
          </div>
        </template>
      </el-upload>

      <el-alert
        v-if="previewData"
        title="预览"
        type="info"
        :closable="false"
        style="margin-top: 20px;"
      >
        <div>实体类型: {{ previewData.entity_types?.length || 0 }} 个</div>
        <div>关系类型: {{ previewData.relation_types?.length || 0 }} 个</div>
      </el-alert>
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button
        v-if="mode === 'import'"
        type="primary"
        @click="handleImport"
        :disabled="!previewData"
        :loading="loading"
      >
        导入
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { useLabelStore } from '@/stores/label'
import type { UploadFile } from 'element-plus'

interface Props {
  visible: boolean
  mode: 'import' | 'export'
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
  'success': []
}>()

const labelStore = useLabelStore()
const loading = ref(false)
const previewData = ref<any>(null)

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const handleFileChange = (file: UploadFile) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const content = e.target?.result as string
      previewData.value = JSON.parse(content)
    } catch (error) {
      ElMessage.error('文件格式错误')
      previewData.value = null
    }
  }
  reader.readAsText(file.raw!)
}

const handleImport = async () => {
  if (!previewData.value) return
  
  loading.value = true
  try {
    await labelStore.importLabels(previewData.value)
    emit('success')
    dialogVisible.value = false
    previewData.value = null
  } catch (error) {
    ElMessage.error('导入失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.el-icon--upload {
  font-size: 67px;
  color: #8c939d;
  margin: 40px 0 16px;
  line-height: 50px;
}
</style>
