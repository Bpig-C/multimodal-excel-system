<template>
  <div class="annotation-list-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="title-section">
            <span class="title">标注任务列表</span>
            <span v-if="currentDatasetName" class="dataset-badge">
              <el-tag type="primary" size="large">{{ currentDatasetName }}</el-tag>
            </span>
          </div>
          <el-breadcrumb v-if="currentDatasetName" separator="/">
            <el-breadcrumb-item :to="{ name: 'my-datasets' }">我的数据集</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentDatasetName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
      </template>

      <!-- 筛选区域 -->
      <div class="filter-section">
        <el-form :inline="true" :model="filters">
          <el-form-item label="数据集">
            <el-select
              v-model="filters.dataset_id"
              placeholder="全部数据集"
              clearable
              style="width: 200px"
              @change="handleFilterChange"
            >
              <el-option
                v-for="dataset in datasets"
                :key="dataset.dataset_id"
                :label="dataset.name"
                :value="dataset.dataset_id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="状态">
            <el-select
              v-model="filters.status"
              placeholder="全部状态"
              clearable
              style="width: 150px"
              @change="handleFilterChange"
            >
              <el-option
                v-for="option in STATUS_OPTIONS"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="loadTasks">查询</el-button>
            <el-button @click="clearFilters">清除筛选</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 任务列表表格 -->
      <el-table
        v-loading="loading"
        :data="tasks"
        style="width: 100%"
        @row-click="handleRowClick"
      >
        <el-table-column prop="task_id" label="任务ID" width="180" />

        <el-table-column prop="dataset_name" label="数据集" width="150" show-overflow-tooltip />

        <el-table-column prop="corpus_text" label="语料预览" min-width="300" show-overflow-tooltip />

        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="标注信息" width="120">
          <template #default="{ row }">
            <div class="annotation-info">
              <span>实体: {{ row.entity_count }}</span>
              <span>关系: {{ row.relation_count }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click.stop="goToAnnotation(row.task_id)"
            >
              编辑
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态 -->
      <el-empty
        v-if="!loading && tasks.length === 0"
        description="暂无分配的任务"
      />

      <!-- 分页 -->
      <div v-if="tasks.length > 0" class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handlePageSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { annotationApi } from '@/api/annotation'
import { datasetApi } from '@/api/dataset'
import type { TaskListItem, Dataset } from '@/types'
import { getStatusText, getStatusType, STATUS_OPTIONS } from '@/constants/taskStatus'

const router = useRouter()
const route = useRoute()

// 状态
const loading = ref(false)
const tasks = ref<TaskListItem[]>([])
const datasets = ref<Dataset[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const currentDatasetName = ref('')

// 筛选条件
const filters = ref({
  dataset_id: '',
  status: ''
})

// 加载数据集列表（用于筛选）
const loadDatasets = async () => {
  // 从任务列表中提取唯一的数据集
  // 这样可以避免额外的API调用和权限问题
  const uniqueDatasets = new Map<string, string>()
  
  tasks.value.forEach(task => {
    if (task.dataset_id && task.dataset_name) {
      uniqueDatasets.set(task.dataset_id, task.dataset_name)
    }
  })
  
  datasets.value = Array.from(uniqueDatasets.entries()).map(([dataset_id, name]) => ({
    dataset_id,
    name
  }))
}

// 加载任务列表
const loadTasks = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (filters.value.dataset_id) {
      params.dataset_id = filters.value.dataset_id
    }
    if (filters.value.status) {
      params.status = filters.value.status
    }

    const response = await annotationApi.getTaskList(params)

    if (response.success) {
      tasks.value = response.data.items
      total.value = response.data.total
      
      // 从任务列表中提取数据集信息用于筛选
      loadDatasets()
    }
  } catch (error: any) {
    console.error('加载任务列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载任务列表失败')
  } finally {
    loading.value = false
  }
}

// 筛选变化处理
const handleFilterChange = () => {
  currentPage.value = 1
  loadTasks()
}

// 清除筛选
const clearFilters = () => {
  filters.value.dataset_id = ''
  filters.value.status = ''
  currentDatasetName.value = ''
  currentPage.value = 1
  
  // 清除URL参数
  router.replace({ query: {} })
  
  loadTasks()
}

// 分页变化处理
const handlePageChange = (page: number) => {
  currentPage.value = page
  loadTasks()
}

const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadTasks()
}

// 行点击处理
const handleRowClick = (row: TaskListItem) => {
  goToAnnotation(row.task_id)
}

// 跳转到标注编辑器
const goToAnnotation = (taskId: string) => {
  router.push({ name: 'annotation-editor', params: { taskId } })
}

// 格式化日期
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 更新当前数据集名称
const updateCurrentDatasetName = () => {
  if (filters.value.dataset_id) {
    const dataset = datasets.value.find(d => d.dataset_id === filters.value.dataset_id)
    currentDatasetName.value = dataset?.name || ''
  } else {
    currentDatasetName.value = ''
  }
}

// 监听路由参数变化（从"我的数据集"跳转过来时）
watch(
  () => route.query.dataset_id,
  (datasetId) => {
    if (datasetId) {
      filters.value.dataset_id = datasetId as string
      loadTasks()
    }
  },
  { immediate: true }
)

// 监听数据集列表变化，更新当前数据集名称
watch(
  () => datasets.value,
  () => {
    updateCurrentDatasetName()
  },
  { deep: true }
)

onMounted(() => {
  // 只加载任务，数据集列表会从任务中提取
  if (!route.query.dataset_id) {
    loadTasks()
  }
})
</script>

<style scoped lang="scss">
.annotation-list-container {
  padding: 20px;

  .card-header {
    display: flex;
    flex-direction: column;
    gap: 12px;

    .title-section {
      display: flex;
      align-items: center;
      gap: 12px;

      .title {
        font-size: 18px;
        font-weight: 600;
      }

      .dataset-badge {
        display: flex;
        align-items: center;
      }
    }
  }

  .filter-section {
    margin-bottom: 20px;
  }

  .annotation-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 12px;
    color: #606266;
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  :deep(.el-table__row) {
    cursor: pointer;

    &:hover {
      background-color: #f5f7fa;
    }
  }
}
</style>
