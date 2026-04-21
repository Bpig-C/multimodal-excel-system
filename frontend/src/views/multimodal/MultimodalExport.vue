<template>
  <div class="multimodal-export">
    <div class="page-header">
      <h2>多模态格式转换</h2>
      <p class="page-desc">独立导出 KF、QMS、品质失效案例数据，支持实体文本、CLIP 对齐、QA 对齐三种格式。</p>
    </div>

    <el-card class="processor-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>选择数据类型</span>
        </div>
      </template>

      <el-radio-group v-model="currentProcessor" @change="handleProcessorChange">
        <el-radio-button
          v-for="processor in processorTabs"
          :key="processor.name"
          :value="processor.name"
        >
          {{ processor.display_name }}
        </el-radio-button>
      </el-radio-group>
    </el-card>

    <el-card class="sources-card">
      <template #header>
        <div class="card-header">
          <span>选择导出数据源</span>
          <el-space>
            <el-button @click="selectAllSources">全选</el-button>
            <el-button @click="clearSources">清空</el-button>
            <el-button type="primary" :icon="Refresh" @click="refreshSources">刷新</el-button>
          </el-space>
        </div>
      </template>

      <el-checkbox-group v-model="selectedDataSources" class="sources-group">
        <el-checkbox
          v-for="file in store.processedFiles"
          :key="file.data_source"
          :label="file.data_source"
          class="source-item"
        >
          <div class="source-title">{{ file.filename }}</div>
          <div class="source-meta">数据源：{{ file.data_source }} | 记录数：{{ file.table_count }}</div>
        </el-checkbox>
      </el-checkbox-group>

      <el-empty
        v-if="!store.loading && store.processedFiles.length === 0"
        description="当前处理器暂无可导出的已处理文件"
      />
    </el-card>

    <el-card class="formats-card">
      <template #header>
        <div class="card-header">
          <span>导出格式配置</span>
        </div>
      </template>

      <el-form label-width="110px">
        <el-form-item label="导出格式">
          <el-checkbox-group v-model="exportFormats">
            <el-checkbox label="entity_text">实体文本</el-checkbox>
            <el-checkbox label="clip_alignment">CLIP 对齐</el-checkbox>
            <el-checkbox label="qa_alignment">QA 对齐</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="包含图片">
          <el-switch v-model="includeImages" />
        </el-form-item>
      </el-form>

      <el-alert
        type="info"
        :closable="false"
        description="系统会按当前数据类型与所选数据源批量导出，并打包为 ZIP 下载。当前进度优先显示真实传输字节；服务器打包阶段会单独提示。"
      />

      <el-button
        type="primary"
        class="export-btn"
        :loading="store.isExporting"
        :disabled="exportFormats.length === 0 || selectedDataSources.length === 0"
        @click="handleBatchExport"
      >
        开始导出
      </el-button>

      <div v-if="exportProgressVisible" class="transfer-progress">
        <el-progress
          :percentage="store.exportProgress.percentage"
          :status="exportProgressStatus"
          :stroke-width="8"
          :show-text="false"
        />
        <p class="progress-text">{{ exportProgressText }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { useDocumentStore } from '@/stores/document'
import type { ExportFormat } from '@/types'

const store = useDocumentStore()

const defaultProcessors = [
  { name: 'kf', display_name: 'KF快反' },
  { name: 'qms', display_name: 'QMS质量' },
  { name: 'failure_case', display_name: '品质案例' }
]

const processorTabs = computed(() => {
  return store.processors.length > 0 ? store.processors : defaultProcessors
})

const currentProcessor = computed({
  get: () => store.currentProcessor,
  set: (value: string) => store.setCurrentProcessor(value)
})

const selectedDataSources = ref<string[]>([])
const exportFormats = ref<ExportFormat[]>(['entity_text'])
const includeImages = ref(false)

const formatBytes = (bytes?: number | null) => {
  if (!bytes || bytes <= 0) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB']
  let value = bytes
  let unitIndex = 0

  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024
    unitIndex += 1
  }

  return `${value.toFixed(value >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`
}

const formatEta = (seconds: number): string => {
  if (!isFinite(seconds) || seconds <= 0) return ''
  if (seconds < 60) return `约 ${Math.ceil(seconds)} 秒`
  if (seconds < 3600) return `约 ${Math.ceil(seconds / 60)} 分钟`
  return `约 ${(seconds / 3600).toFixed(1)} 小时`
}

// Download speed tracking
const downloadStartTime = ref(0)
const downloadSpeed = ref(0) // bytes/sec

watch(
  () => store.exportProgress.phase,
  (phase) => {
    if (phase !== 'downloading') {
      downloadStartTime.value = 0
      downloadSpeed.value = 0
    }
  }
)

watch(
  () => store.exportProgress.loaded,
  (loaded) => {
    if (store.exportProgress.phase !== 'downloading' || loaded <= 0) return
    if (downloadStartTime.value === 0) {
      downloadStartTime.value = Date.now()
      return
    }
    const elapsed = (Date.now() - downloadStartTime.value) / 1000
    if (elapsed > 0.5) {
      downloadSpeed.value = loaded / elapsed
    }
  }
)

const resolveProgressStatus = (phase: string): 'success' | 'exception' | undefined => {
  if (phase === 'success') return 'success'
  if (phase === 'exception') return 'exception'
  return undefined
}

const exportProgressVisible = computed(() => store.exportProgress.phase !== 'idle')
const exportProgressStatus = computed(() => resolveProgressStatus(store.exportProgress.phase))
const exportProgressText = computed(() => {
  const state = store.exportProgress

  if (state.phase === 'processing') {
    return state.message || '正在打包导出文件...'
  }

  if (state.phase === 'downloading') {
    const speedStr = downloadSpeed.value > 1024
      ? `${formatBytes(downloadSpeed.value)}/s`
      : ''

    if (state.total && state.total > 0) {
      const eta = downloadSpeed.value > 0
        ? formatEta((state.total - state.loaded) / downloadSpeed.value)
        : ''
      const etaPart = eta ? `  ${eta}` : ''
      const speedPart = speedStr ? `  ${speedStr}` : ''
      return `已下载 ${formatBytes(state.loaded)} / ${formatBytes(state.total)} (${state.percentage}%)${speedPart}${etaPart}`
    }

    const speedPart = speedStr ? `  ${speedStr}` : ''
    return `正在接收导出文件，已下载 ${formatBytes(state.loaded)}${speedPart}`
  }

  return state.message
})

const resetSelectedSources = () => {
  selectedDataSources.value = store.processedFiles.map(file => file.data_source)
}

const handleProcessorChange = async (value: string) => {
  await store.setCurrentProcessor(value)
  store.resetExportProgress()
  resetSelectedSources()
}

const refreshSources = async () => {
  await store.fetchProcessedFiles()
  resetSelectedSources()
}

const selectAllSources = () => {
  resetSelectedSources()
}

const clearSources = () => {
  selectedDataSources.value = []
}

const downloadBlob = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

const handleBatchExport = async () => {
  try {
    const blob = await store.batchExport({
      formats: exportFormats.value,
      data_sources: selectedDataSources.value,
      include_images: includeImages.value
    })

    downloadBlob(blob, `${store.currentProcessor}_corpus_${Date.now()}.zip`)
    ElMessage.success('导出成功')
  } catch (error: any) {
    ElMessage.error(error?.message || '导出失败')
  }
}

onMounted(async () => {
  await store.fetchProcessors()
  await store.fetchProcessedFiles()
  store.resetExportProgress()
  resetSelectedSources()
})
</script>

<style scoped lang="scss">
.multimodal-export {
  padding: 20px;

  .page-header {
    margin-bottom: 20px;

    h2 {
      margin: 0 0 8px;
      font-size: 24px;
      color: #303133;
    }

    .page-desc {
      margin: 0;
      font-size: 14px;
      color: #909399;
    }
  }

  .processor-card,
  .sources-card,
  .formats-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
  }

  .sources-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 8px;

    .source-item {
      margin-right: 0;
      padding: 8px 10px;
      border: 1px solid #ebeef5;
      border-radius: 6px;
      background: #fafafa;
    }

    .source-title {
      font-weight: 600;
      color: #303133;
    }

    .source-meta {
      margin-top: 4px;
      font-size: 12px;
      color: #909399;
    }
  }

  .export-btn {
    margin-top: 16px;
    width: 100%;
  }

  .transfer-progress {
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 8px;
    background: #f5f7fa;

    .progress-text {
      margin: 10px 0 0;
      color: #606266;
      font-size: 13px;
      line-height: 1.5;
    }
  }
}
</style>
