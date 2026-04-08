<template>
  <el-dialog
    v-model="visible"
    title="批量自动标注"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-if="!jobStarted" class="dialog-content">
      <el-alert
        title="批量标注说明"
        type="info"
        :closable="false"
        show-icon
      >
        <p>将使用AI模型对数据集中的所有任务进行自动标注：</p>
        <ul>
          <li>自动识别文本中的实体</li>
          <li>自动抽取实体间的关系</li>
          <li>自动标注图片内容</li>
        </ul>
        <p style="margin-top: 10px; color: #e6a23c;">
          <el-icon><Warning /></el-icon>
          注意：批量标注可能需要较长时间，请耐心等待
        </p>
      </el-alert>

      <div class="dataset-info">
        <div class="info-item">
          <span class="label">数据集名称：</span>
          <span class="value">{{ dataset?.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">任务总数：</span>
          <span class="value">{{ dataset?.statistics?.total_tasks || 0 }}</span>
        </div>
        <div class="info-item">
          <span class="label">待标注任务：</span>
          <span class="value">{{ dataset?.statistics?.pending_tasks || 0 }}</span>
        </div>
      </div>
    </div>

    <div v-else class="progress-content">
      <div class="progress-header">
        <h3>正在执行批量标注...</h3>
        <el-tag :type="statusType">{{ statusText }}</el-tag>
      </div>

      <div class="progress-stats">
        <div class="stat-item">
          <div class="stat-label">总任务数</div>
          <div class="stat-value">{{ jobStats.total_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">已完成</div>
          <div class="stat-value success">{{ jobStats.completed_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">失败</div>
          <div class="stat-value danger">{{ jobStats.failed_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">进行中</div>
          <div class="stat-value warning">{{ jobStats.processing_tasks }}</div>
        </div>
      </div>

      <div class="progress-bar">
        <div class="progress-label">
          <span>完成进度</span>
          <span class="progress-percent">{{ progressPercent }}%</span>
        </div>
        <el-progress
          :percentage="progressPercent"
          :status="progressStatus"
        />
      </div>

      <div v-if="jobStats.failed_tasks > 0" class="error-section">
        <el-alert
          title="部分任务标注失败"
          type="warning"
          :closable="false"
          show-icon
        >
          <p>{{ jobStats.failed_tasks }} 个任务标注失败，请手动检查和标注</p>
        </el-alert>
      </div>

      <div class="time-info">
        <span>开始时间：{{ formatTime(jobStats.started_at) }}</span>
        <span v-if="jobStats.completed_at">
          完成时间：{{ formatTime(jobStats.completed_at) }}
        </span>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">
          {{ jobStarted && jobStats.status !== 'completed' ? '后台运行' : '关闭' }}
        </el-button>
        <el-button
          v-if="!jobStarted"
          type="primary"
          :loading="starting"
          @click="handleStart"
        >
          开始标注
        </el-button>
        <el-button
          v-else-if="jobStats.status === 'running'"
          type="danger"
          :loading="cancelling"
          @click="handleCancel"
        >
          取消任务
        </el-button>
        <el-button
          v-else-if="jobStats.status === 'completed'"
          type="primary"
          @click="handleViewResults"
        >
          查看结果
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Warning } from '@element-plus/icons-vue'
import { annotationApi } from '@/api/annotation'
import type { Dataset } from '@/types'
import { format } from 'date-fns'

interface Props {
  modelValue: boolean
  dataset: Dataset | null
}

interface JobStats {
  job_id: string
  dataset_id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  total_tasks: number
  completed_tasks: number
  failed_tasks: number
  processing_tasks: number
  started_at?: string
  completed_at?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

// 状态
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const jobStarted = ref(false)
const starting = ref(false)
const cancelling = ref(false)
const jobId = ref<string>('')
const jobStats = ref<JobStats>({
  job_id: '',
  dataset_id: '',
  status: 'pending',
  total_tasks: 0,
  completed_tasks: 0,
  failed_tasks: 0,
  processing_tasks: 0
})

let pollingTimer: number | null = null

// 计算属性
const progressPercent = computed(() => {
  if (jobStats.value.total_tasks === 0) return 0
  return Math.round(
    (jobStats.value.completed_tasks / jobStats.value.total_tasks) * 100
  )
})

const progressStatus = computed(() => {
  if (jobStats.value.status === 'completed') return 'success'
  if (jobStats.value.status === 'failed') return 'exception'
  if (jobStats.value.status === 'cancelled') return 'exception'
  return undefined
})

const statusType = computed(() => {
  const typeMap = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
    cancelled: 'info'
  }
  return typeMap[jobStats.value.status]
})

const statusText = computed(() => {
  const textMap = {
    pending: '等待中',
    running: '进行中',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消'
  }
  return textMap[jobStats.value.status]
})

// 方法
const handleStart = async () => {
  if (!props.dataset) return

  try {
    starting.value = true

    const response = await annotationApi.triggerBatchAnnotation({
      dataset_id: props.dataset.dataset_id
    })

    jobId.value = response.data.job_id
    jobStats.value = {
      job_id: response.data.job_id,
      dataset_id: response.data.dataset_id,
      status: response.data.status,
      total_tasks: response.data.total_tasks,
      completed_tasks: 0,
      failed_tasks: 0,
      processing_tasks: 0
    }

    jobStarted.value = true
    ElMessage.success('批量标注任务已启动')

    // 开始轮询任务状态
    startPolling()
  } catch (error: any) {
    ElMessage.error(error.message || '启动批量标注失败')
  } finally {
    starting.value = false
  }
}

const handleCancel = async () => {
  try {
    cancelling.value = true

    await annotationApi.cancelBatchJob(jobId.value)

    jobStats.value.status = 'cancelled'
    stopPolling()

    ElMessage.success('批量标注任务已取消')
  } catch (error: any) {
    ElMessage.error(error.message || '取消任务失败')
  } finally {
    cancelling.value = false
  }
}

const handleViewResults = () => {
  emit('success')
  handleClose()
}

const handleClose = () => {
  if (jobStats.value.status === 'running') {
    ElMessage.info('任务将在后台继续运行')
  }
  
  stopPolling()
  resetState()
  visible.value = false
}

const startPolling = () => {
  // 每2秒轮询一次任务状态
  pollingTimer = window.setInterval(async () => {
    await fetchJobStatus()
  }, 2000)
}

const stopPolling = () => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  }
}

const fetchJobStatus = async () => {
  try {
    const response = await annotationApi.getBatchJobStatus(jobId.value)
    jobStats.value = response.data

    // 如果任务完成或失败，停止轮询
    if (['completed', 'failed', 'cancelled'].includes(jobStats.value.status)) {
      stopPolling()
      
      if (jobStats.value.status === 'completed') {
        ElMessage.success('批量标注任务已完成')
        emit('success')
      } else if (jobStats.value.status === 'failed') {
        ElMessage.error('批量标注任务失败')
      }
    }
  } catch (error: any) {
    console.error('获取任务状态失败:', error)
  }
}

const formatTime = (timeString?: string) => {
  if (!timeString) return '-'
  try {
    return format(new Date(timeString), 'yyyy-MM-dd HH:mm:ss')
  } catch {
    return timeString
  }
}

const resetState = () => {
  jobStarted.value = false
  starting.value = false
  cancelling.value = false
  jobId.value = ''
  jobStats.value = {
    job_id: '',
    dataset_id: '',
    status: 'pending',
    total_tasks: 0,
    completed_tasks: 0,
    failed_tasks: 0,
    processing_tasks: 0
  }
}

// 监听对话框关闭
watch(visible, (newVal) => {
  if (!newVal) {
    stopPolling()
  }
})
</script>

<style scoped lang="scss">
.dialog-content {
  .dataset-info {
    margin-top: 20px;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 4px;

    .info-item {
      display: flex;
      align-items: center;
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }

      .label {
        font-size: 14px;
        color: #606266;
        min-width: 100px;
      }

      .value {
        font-size: 14px;
        color: #303133;
        font-weight: 600;
      }
    }
  }
}

.progress-content {
  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h3 {
      margin: 0;
      font-size: 16px;
      color: #303133;
    }
  }

  .progress-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;

    .stat-item {
      text-align: center;
      padding: 12px;
      background: #f5f7fa;
      border-radius: 4px;

      .stat-label {
        font-size: 12px;
        color: #909399;
        margin-bottom: 8px;
      }

      .stat-value {
        font-size: 24px;
        font-weight: 600;
        color: #303133;

        &.success {
          color: #67c23a;
        }

        &.danger {
          color: #f56c6c;
        }

        &.warning {
          color: #e6a23c;
        }
      }
    }
  }

  .progress-bar {
    margin-bottom: 20px;

    .progress-label {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      font-size: 14px;
      color: #606266;

      .progress-percent {
        font-weight: 600;
        color: #409eff;
      }
    }
  }

  .error-section {
    margin-bottom: 20px;
  }

  .time-info {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: #909399;
    padding-top: 16px;
    border-top: 1px solid #ebeef5;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
