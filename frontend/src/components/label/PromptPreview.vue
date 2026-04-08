<template>
  <el-dialog
    v-model="dialogVisible"
    title="Agent Prompt 预览"
    width="900px"
  >
    <div class="prompt-preview">
      <el-radio-group v-model="promptType" @change="handleTypeChange">
        <el-radio-button value="entity">实体抽取</el-radio-button>
        <el-radio-button value="relation">关系抽取</el-radio-button>
        <el-radio-button value="image">图片标注</el-radio-button>
      </el-radio-group>

      <div class="prompt-content" v-loading="loading">
        <pre v-if="promptContent">{{ promptContent }}</pre>
        <el-empty v-else description="暂无内容" />
      </div>

      <div class="prompt-actions">
        <el-button @click="handleCopy">复制</el-button>
        <el-button type="primary" @click="handleRefresh">刷新</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '@/stores/label'

interface Props {
  visible: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const labelStore = useLabelStore()
const promptType = ref<'entity' | 'relation' | 'image'>('entity')
const promptContent = ref('')
const loading = ref(false)

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const loadPrompt = async () => {
  loading.value = true
  try {
    promptContent.value = await labelStore.previewPrompt(promptType.value)
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleTypeChange = () => {
  loadPrompt()
}

const handleRefresh = () => {
  loadPrompt()
}

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(promptContent.value)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

watch(() => props.visible, (visible) => {
  if (visible) {
    loadPrompt()
  }
})
</script>

<style scoped>
.prompt-preview {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.prompt-content {
  min-height: 400px;
  max-height: 600px;
  overflow-y: auto;
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 16px;
}

.prompt-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.prompt-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
