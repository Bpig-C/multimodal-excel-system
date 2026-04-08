<template>
  <el-card class="dataset-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="dataset-name">
          <el-icon class="dataset-icon"><Folder /></el-icon>
          <span class="name-text">{{ dataset.name }}</span>
          <el-tag :type="statusTagType" size="small" class="status-tag">
            {{ statusText }}
          </el-tag>
        </div>
        <el-dropdown trigger="click" @command="handleCommand">
          <el-icon class="more-icon"><MoreFilled /></el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="view" :icon="View">
                查看详情
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="batchAnnotate" 
                :icon="MagicStick"
              >
                批量标注
              </el-dropdown-item>
              <!-- Task 47: 分配管理（仅管理员可见） -->
              <el-dropdown-item 
                v-if="isAdmin" 
                command="assign" 
                :icon="Setting"
              >
                分配管理
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="edit" 
                :icon="Edit"
              >
                编辑
              </el-dropdown-item>
              <el-dropdown-item 
                command="export" 
                :icon="Download"
                :disabled="datasetStatus === 'empty'"
              >
                导出
              </el-dropdown-item>
              <el-dropdown-item 
                v-if="!isViewer" 
                command="delete" 
                :icon="Delete" 
                divided
              >
                删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </template>

    <div class="card-content">
      <!-- 描述 -->
      <div v-if="dataset.description" class="description">
        {{ dataset.description }}
      </div>
      <div v-else class="description empty">
        暂无描述
      </div>

      <!-- 统计信息 -->
      <div class="statistics">
        <div class="stat-item">
          <div class="stat-label">总任务数</div>
          <div class="stat-value">{{ statistics.total_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">已标注</div>
          <div class="stat-value completed">{{ statistics.completed_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">已复核</div>
          <div class="stat-value reviewed">{{ statistics.reviewed_tasks }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">待处理</div>
          <div class="stat-value pending">{{ statistics.pending_tasks }}</div>
        </div>
      </div>

      <!-- 进度条 -->
      <div class="progress-section">
        <div class="progress-label">
          <span>完成进度</span>
          <span class="progress-percent">{{ completionRate }}%</span>
        </div>
        <el-progress
          :percentage="completionRate"
          :color="progressColor"
          :show-text="false"
        />
      </div>

      <!-- 元信息 -->
      <div class="meta-info">
        <span class="meta-item">
          <el-icon><Clock /></el-icon>
          {{ formatDate(dataset.created_at) }}
        </span>
      </div>
    </div>

    <template #footer>
      <div class="card-footer">
        <el-button size="small" @click="handleView">
          查看详情
        </el-button>
        <el-button 
          v-if="!isViewer" 
          size="small" 
          type="primary" 
          @click="handleStartAnnotation"
        >
          开始标注
        </el-button>
        <el-tooltip
          v-else
          :disabled="datasetStatus !== 'empty'"
          content="数据集为空,无法导出"
          placement="top"
        >
          <span>
            <el-button 
              size="small" 
              type="primary" 
              :disabled="datasetStatus === 'empty'"
              @click="handleCommand('export')"
            >
              导出数据
            </el-button>
          </span>
        </el-tooltip>
      </div>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  Folder,
  MoreFilled,
  View,
  Edit,
  Download,
  Delete,
  Clock,
  MagicStick,
  Setting
} from '@element-plus/icons-vue'
import type { Dataset, DatasetStatistics, DatasetStatus } from '@/types'
import { formatDateRelative } from '@/utils/datetime'

interface Props {
  dataset: Dataset
  isViewer?: boolean
  isAdmin?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isViewer: false,
  isAdmin: false
})

const emit = defineEmits<{
  view: [dataset: Dataset]
  edit: [dataset: Dataset]
  delete: [dataset: Dataset]
  export: [dataset: Dataset]
  batchAnnotate: [dataset: Dataset]
  assign: [dataset: Dataset]
}>()

// 计算属性
const statistics = computed<DatasetStatistics>(() => {
  return props.dataset.statistics || {
    total_tasks: 0,
    completed_tasks: 0,
    reviewed_tasks: 0,
    pending_tasks: 0
  }
})

const completionRate = computed(() => {
  const total = statistics.value.total_tasks
  if (total === 0) return 0
  return Math.round((statistics.value.completed_tasks / total) * 100)
})

const progressColor = computed(() => {
  const rate = completionRate.value
  if (rate === 100) return '#67c23a'
  if (rate >= 50) return '#409eff'
  return '#e6a23c'
})

const datasetStatus = computed<DatasetStatus>(() => {
  const total = statistics.value.total_tasks
  const completed = statistics.value.completed_tasks
  
  if (total === 0) return 'empty'
  if (completed < total) return 'in_progress'
  return 'completed'
})

const statusText = computed(() => {
  switch (datasetStatus.value) {
    case 'empty':
      return '空'
    case 'in_progress':
      return '进行中'
    case 'completed':
      return '已完成'
    default:
      return ''
  }
})

const statusTagType = computed(() => {
  switch (datasetStatus.value) {
    case 'empty':
      return 'info'
    case 'in_progress':
      return 'warning'
    case 'completed':
      return 'success'
    default:
      return 'info'
  }
})

// 方法
const formatDate = (dateString: string) => formatDateRelative(dateString)

const handleCommand = (command: string) => {
  switch (command) {
    case 'view':
      emit('view', props.dataset)
      break
    case 'batchAnnotate':
      emit('batchAnnotate', props.dataset)
      break
    case 'assign':
      emit('assign', props.dataset)
      break
    case 'edit':
      emit('edit', props.dataset)
      break
    case 'export':
      emit('export', props.dataset)
      break
    case 'delete':
      emit('delete', props.dataset)
      break
  }
}

const handleView = () => {
  emit('view', props.dataset)
}

const handleStartAnnotation = () => {
  // 跳转到数据集详情页面，查看任务列表
  emit('view', props.dataset)
}
</script>

<style scoped lang="scss">
.dataset-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .dataset-name {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;
      min-width: 0;

      .dataset-icon {
        font-size: 20px;
        color: #409eff;
        flex-shrink: 0;
      }

      .name-text {
        font-size: 16px;
        font-weight: 600;
        color: #303133;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .status-tag {
        flex-shrink: 0;
        margin-left: auto;
      }
    }

    .more-icon {
      font-size: 20px;
      color: #909399;
      cursor: pointer;
      flex-shrink: 0;

      &:hover {
        color: #409eff;
      }
    }
  }

  .card-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 16px;

    .description {
      font-size: 14px;
      line-height: 1.6;
      color: #606266;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;

      &.empty {
        color: #c0c4cc;
        font-style: italic;
      }
    }

    .statistics {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;

      .stat-item {
        text-align: center;

        .stat-label {
          font-size: 12px;
          color: #909399;
          margin-bottom: 4px;
        }

        .stat-value {
          font-size: 20px;
          font-weight: 600;
          color: #303133;

          &.completed {
            color: #67c23a;
          }

          &.reviewed {
            color: #409eff;
          }

          &.pending {
            color: #e6a23c;
          }
        }
      }
    }

    .progress-section {
      .progress-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-size: 13px;
        color: #606266;

        .progress-percent {
          font-weight: 600;
          color: #409eff;
        }
      }
    }

    .meta-info {
      display: flex;
      gap: 16px;
      font-size: 13px;
      color: #909399;

      .meta-item {
        display: flex;
        align-items: center;
        gap: 4px;

        .el-icon {
          font-size: 14px;
        }
      }
    }
  }

  .card-footer {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
  }
}
</style>
