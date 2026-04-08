<template>
  <div class="my-datasets-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="title">我的数据集</span>
          <el-radio-group v-model="roleFilter" size="small" @change="loadMyDatasets">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="annotator">标注任务</el-radio-button>
            <el-radio-button label="reviewer">复核任务</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="datasets"
        style="width: 100%"
      >
        <el-table-column prop="name" label="数据集名称" min-width="200">
          <template #default="{ row }">
            <el-link type="primary" @click="goToDetail(row.dataset_id)">
              {{ row.name }}
            </el-link>
          </template>
        </el-table-column>

        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />

        <el-table-column prop="my_role" label="我的角色" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.my_role === 'annotator'" type="success">标注员</el-tag>
            <el-tag v-else-if="row.my_role === 'reviewer'" type="warning">复核员</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="my_task_range" label="任务范围" width="120" />

        <el-table-column label="进度" width="200">
          <template #default="{ row }">
            <div class="progress-info">
              <el-progress
                :percentage="getProgress(row)"
                :color="getProgressColor(row)"
              />
              <span class="progress-text">
                {{ row.my_completed_count }} / {{ row.my_task_count }}
              </span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="total_tasks" label="总任务数" width="100" />

        <el-table-column prop="assigned_at" label="分配时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.assigned_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.my_role === 'annotator'"
              type="primary"
              size="small"
              @click="goToAnnotation(row.dataset_id)"
            >
              开始标注
            </el-button>
            <el-button
              v-else-if="row.my_role === 'reviewer'"
              type="warning"
              size="small"
              @click="goToReview(row.dataset_id)"
            >
              开始复核
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadMyDatasets"
          @current-change="loadMyDatasets"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { datasetApi } from '@/api/dataset'
import type { MyDatasetInfo } from '@/types/assignment'

const router = useRouter()

// 状态
const loading = ref(false)
const datasets = ref<MyDatasetInfo[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const roleFilter = ref('')

// 加载我的数据集
const loadMyDatasets = async () => {
  loading.value = true
  try {
    console.log('开始加载我的数据集...')
    const response = await datasetApi.getMyDatasets({
      role: roleFilter.value || undefined,
      page: currentPage.value,
      page_size: pageSize.value
    })

    console.log('API响应:', response)
    console.log('response.success:', response.success)
    console.log('response.data:', response.data)
    console.log('response.data.items:', response.data?.items)

    if (response.success) {
      datasets.value = response.data.items
      total.value = response.data.total
      console.log('✓ 设置datasets:', datasets.value)
      console.log('✓ 设置total:', total.value)
    } else {
      console.error('API返回success=false')
    }
  } catch (error: any) {
    console.error('加载失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载数据集失败')
  } finally {
    loading.value = false
  }
}

// 计算进度百分比
const getProgress = (row: MyDatasetInfo) => {
  if (row.my_task_count === 0) return 0
  return Math.round((row.my_completed_count / row.my_task_count) * 100)
}

// 获取进度条颜色
const getProgressColor = (row: MyDatasetInfo) => {
  const progress = getProgress(row)
  if (progress === 100) return '#67c23a'
  if (progress >= 50) return '#409eff'
  return '#e6a23c'
}

// 格式化日期
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 跳转到数据集详情
const goToDetail = (datasetId: string) => {
  router.push({ name: 'dataset-detail', params: { id: datasetId } })
}

// 跳转到标注页面
const goToAnnotation = (datasetId: string) => {
  router.push({ name: 'annotations', query: { dataset_id: datasetId } })
}

// 跳转到复核页面
const goToReview = (datasetId: string) => {
  router.push({ name: 'review', query: { dataset_id: datasetId } })
}

onMounted(() => {
  loadMyDatasets()
})
</script>

<style scoped lang="scss">
.my-datasets-container {
  padding: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .title {
      font-size: 18px;
      font-weight: 600;
    }
  }

  .progress-info {
    display: flex;
    flex-direction: column;
    gap: 4px;

    .progress-text {
      font-size: 12px;
      color: #606266;
      text-align: center;
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
