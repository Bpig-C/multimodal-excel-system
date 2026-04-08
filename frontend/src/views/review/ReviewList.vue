<template>
  <div class="review-list-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="title">复核任务列表</span>
        </div>
      </template>

      <!-- 筛选区域 -->
      <div class="filter-section">
        <el-form :inline="true" :model="filters">
          <el-form-item label="状态">
            <el-select
              v-model="filters.status"
              placeholder="全部状态"
              clearable
              style="width: 150px"
              @change="handleFilterChange"
            >
              <el-option label="待复核" value="pending" />
              <el-option label="已通过" value="approved" />
              <el-option label="已驳回" value="rejected" />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="loadReviewTasks">查询</el-button>
            <el-button @click="clearFilters">清除筛选</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 任务列表表格 -->
      <el-table
        v-loading="loading"
        :data="reviewTasks"
        style="width: 100%"
        @row-click="handleReview"
      >
        <el-table-column prop="review_id" label="复核ID" width="180" />
        <el-table-column prop="task_id" label="标注任务ID" width="180" />
        
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="复核人" width="120">
          <template #default="{ row }">
            {{ row.reviewer_id ? `用户${row.reviewer_id}` : '未分配' }}
          </template>
        </el-table-column>
        
        <el-table-column prop="review_comment" label="复核意见" show-overflow-tooltip />
        
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="复核时间" width="180">
          <template #default="{ row }">
            {{ row.reviewed_at ? formatDateTime(row.reviewed_at) : '-' }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click.stop="handleReview(row)"
            >
              {{ row.status === 'pending' ? '开始复核' : '查看详情' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态 -->
      <el-empty
        v-if="!loading && reviewTasks.length === 0"
        description="暂无复核任务"
      />

      <!-- 分页 -->
      <div v-if="reviewTasks.length > 0" class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { reviewApi } from '@/api/review'
import { formatDateTime } from '@/utils/datetime'

interface ReviewTask {
  review_id: string
  task_id: string
  status: 'pending' | 'approved' | 'rejected'
  reviewer_id?: number
  review_comment?: string
  reviewed_at?: string
  created_at: string
}

const router = useRouter()

// 状态
const loading = ref(false)
const reviewTasks = ref<ReviewTask[]>([])

// 筛选条件
const filters = ref({
  status: '',
  reviewer_id: undefined as number | undefined
})

// 分页
const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

// 加载复核任务列表
const loadReviewTasks = async () => {
  try {
    loading.value = true
    
    const response = await reviewApi.list({
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
      status: filters.value.status || undefined,
      reviewer_id: filters.value.reviewer_id
    })
    
    // 处理响应数据
    if (Array.isArray(response)) {
      // 如果返回的是数组
      reviewTasks.value = response
      pagination.value.total = response.length
    } else if (response.data) {
      // 如果返回的是包含data的对象
      reviewTasks.value = response.data.items || response.data
      pagination.value.total = response.data.total || reviewTasks.value.length
    }
  } catch (error: any) {
    console.error('加载复核任务失败:', error)
    ElMessage.error(error.message || '加载复核任务失败')
  } finally {
    loading.value = false
  }
}

// 筛选变化
const handleFilterChange = () => {
  pagination.value.page = 1
  loadReviewTasks()
}

// 清除筛选
const clearFilters = () => {
  filters.value.status = ''
  filters.value.reviewer_id = undefined
  pagination.value.page = 1
  loadReviewTasks()
}

// 分页变化
const handlePageChange = (page: number) => {
  pagination.value.page = page
  loadReviewTasks()
}

const handlePageSizeChange = (pageSize: number) => {
  pagination.value.pageSize = pageSize
  pagination.value.page = 1
  loadReviewTasks()
}

// 开始复核
const handleReview = (task: ReviewTask) => {
  router.push({
    name: 'review-detail',
    params: { reviewId: task.review_id }
  })
}

// 状态相关
const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待复核',
    approved: '已通过',
    rejected: '已驳回'
  }
  return textMap[status] || '未知'
}

// formatDateTime 已从 @/utils/datetime 导入

// 初始化
onMounted(() => {
  loadReviewTasks()
})
</script>

<style scoped lang="scss">
.review-list-container {
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

  .filter-section {
    margin-bottom: 20px;
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
