<template>
  <div class="dataset-management">
    <div class="page-header">
      <div class="header-left">
        <h2>数据集管理</h2>
        <p class="page-desc">
          {{ authStore.user?.role === 'viewer' ? '查看和导出数据集' : '从语料中选择记录创建数据集，用于标注任务' }}
        </p>
      </div>
      <div class="header-right">
        <el-select
          v-model="statusFilter"
          placeholder="筛选状态"
          clearable
          style="width: 150px; margin-right: 12px"
          @change="handleFilterChange"
        >
          <el-option label="全部" value="" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已完成" value="completed" />
        </el-select>
        <el-button
          v-if="authStore.user?.role !== 'viewer'"
          type="primary"
          :icon="Plus"
          @click="handleCreate"
        >
          创建数据集
        </el-button>
      </div>
    </div>

    <!-- 数据集列表 -->
    <div v-loading="loading" class="dataset-list">
      <el-empty
        v-if="!loading && datasetList.length === 0"
        :description="authStore.user?.role === 'viewer' ? '暂无数据集' : '暂无数据集'"
      >
        <el-button 
          v-if="authStore.user?.role !== 'viewer'" 
          type="primary" 
          @click="handleCreate"
        >
          创建第一个数据集
        </el-button>
      </el-empty>

      <div v-else class="dataset-grid">
        <DatasetCard
          v-for="dataset in datasetList"
          :key="dataset.id"
          :dataset="dataset"
          :is-viewer="authStore.user?.role === 'viewer'"
          :is-admin="authStore.user?.role === 'admin'"
          @view="handleView"
          @batch-annotate="handleBatchAnnotate"
          @assign="handleAssign"
          @edit="handleEdit"
          @delete="handleDelete"
          @export="handleExport"
        />
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[12, 24, 48]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 创建数据集对话框 -->
    <DatasetCreateDialog
      v-model="createDialogVisible"
      @success="handleCreateSuccess"
    />

    <!-- 编辑数据集对话框 -->
    <DatasetEditDialog
      v-model="editDialogVisible"
      :dataset="selectedDataset"
      @success="handleEditSuccess"
    />

    <!-- 批量标注对话框 -->
    <BatchAnnotationDialog
      v-model="batchAnnotationDialogVisible"
      :dataset="selectedDataset"
      @success="handleBatchAnnotationSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ref, computed, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useDatasetStore, useAuthStore } from '@/stores'
import DatasetCard from '@/components/dataset/DatasetCard.vue'
import DatasetCreateDialog from '@/components/dataset/DatasetCreateDialog.vue'
import DatasetEditDialog from '@/components/dataset/DatasetEditDialog.vue'
import BatchAnnotationDialog from '@/components/dataset/BatchAnnotationDialog.vue'
import type { Dataset, DatasetStatus } from '@/types'
import { buildApiUrl } from '@/utils/backendUrl'

const router = useRouter()
const datasetStore = useDatasetStore()
const authStore = useAuthStore()

// 状态
const createDialogVisible = ref(false)
const editDialogVisible = ref(false)
const batchAnnotationDialogVisible = ref(false)
const selectedDataset = ref<Dataset | null>(null)
const currentPage = ref(1)
const pageSize = ref(12)
const statusFilter = ref<DatasetStatus | ''>('')

// 检查用户角色，标注员和复核员应该使用"我的数据集"页面
const checkUserRole = () => {
  const userRole = authStore.user?.role
  if (userRole === 'annotator' || userRole === 'reviewer') {
    ElMessage.info('标注员和复核员请使用"我的数据集"查看分配给您的任务')
    router.replace({ name: 'my-datasets' })
  }
}

// 计算属性
const loading = computed(() => datasetStore.loading)
const allDatasets = computed(() => datasetStore.datasetList)
const total = computed(() => datasetStore.total)

// 根据状态筛选数据集
const datasetList = computed(() => {
  if (!statusFilter.value) {
    return allDatasets.value
  }
  
  return allDatasets.value.filter(dataset => {
    const stats = dataset.statistics
    if (!stats) return false
    
    const total = stats.total_tasks
    const completed = stats.completed_tasks
    
    if (statusFilter.value === 'in_progress') {
      return total > 0 && completed < total
    } else if (statusFilter.value === 'completed') {
      return total > 0 && completed === total
    }
    
    return true
  })
})

// 方法
const fetchList = async () => {
  // 浏览员应该看到所有数据集，不按创建人过滤
  const params: any = {
    page: currentPage.value,
    page_size: pageSize.value
  }
  
  // 只有非浏览员才按创建人过滤（可选）
  // 实际上，所有角色都应该能看到所有数据集
  // if (authStore.user?.role !== 'viewer') {
  //   params.created_by = authStore.user?.id
  // }
  
  await datasetStore.fetchList(params)
}

const handlePageChange = () => {
  fetchList()
}

const handleFilterChange = () => {
  // 筛选是前端实现,不需要重新请求
  // 如果需要后端筛选,可以在这里调用 fetchList()
}

const handleCreate = () => {
  createDialogVisible.value = true
}

const handleCreateSuccess = () => {
  ElMessage.success('数据集创建成功')
  fetchList()
}

const handleView = (dataset: Dataset) => {
  router.push({ name: 'dataset-detail', params: { id: dataset.dataset_id } })
}

const handleAssign = (dataset: Dataset) => {
  router.push({ name: 'dataset-assignment', params: { id: dataset.dataset_id } })
}

const handleBatchAnnotate = (dataset: Dataset) => {
  selectedDataset.value = dataset
  batchAnnotationDialogVisible.value = true
}

const handleBatchAnnotationSuccess = () => {
  ElMessage.success('批量标注完成')
  fetchList()
}

const handleEdit = (dataset: Dataset) => {
  selectedDataset.value = dataset
  editDialogVisible.value = true
}

const handleEditSuccess = () => {
  ElMessage.success('数据集更新成功')
  fetchList()
}

const handleDelete = async (dataset: Dataset) => {
  try {
    const confirmMessageVNode = h('div', [
      h('div', `确定要删除数据集 "${dataset.name}" 吗？`),
      h('div', { style: 'margin-top: 8px; color: #f56c6c;' }, '此操作将同时删除所有关联的标注任务，且不可恢复。')
    ])
    await ElMessageBox.confirm(
      confirmMessageVNode,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await datasetStore.deleteDataset(dataset.dataset_id)
    ElMessage.success('删除成功')
    
    // 如果当前页没有数据了，返回上一页
    if (datasetList.value.length === 0 && currentPage.value > 1) {
      currentPage.value--
    }
    
    fetchList()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const handleExport = async (dataset: Dataset) => {
  try {
    const fallbackFilename = `${dataset.dataset_id}_${Date.now()}.jsonl`
    const requestedOutputPath = `data/exports/${fallbackFilename}`

    // 直接POST导出接口，获取blob
    const url = buildApiUrl(`/datasets/${dataset.dataset_id}/export`)

    const token = localStorage.getItem('token') || sessionStorage.getItem('token')
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const response = await axios.post(
      url,
      {
        output_path: requestedOutputPath,
        status_filter: ["completed", "reviewed"]
      },
      {
        headers,
        responseType: 'blob',
        validateStatus: status => status === 200
      }
    )

    // 尝试从响应头获取文件名
    let filename = fallbackFilename
    const disposition = response.headers['content-disposition']
    if (disposition) {
      const match = disposition.match(/filename="?([^";]+)"?/)
      if (match) filename = decodeURIComponent(match[1])
    }

    // 创建下载链接
    const blob = response.data
    const blobUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = blobUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(blobUrl)

    ElMessage.success('导出成功，已开始下载')
  } catch (error: any) {
    ElMessage.error(error?.message || '导出失败')
  }
}

// 生命周期
onMounted(() => {
  // 检查用户角色
  checkUserRole()
  
  // 如果不是标注员/复核员，加载数据集列表
  const userRole = authStore.user?.role
  if (userRole !== 'annotator' && userRole !== 'reviewer') {
    fetchList()
  }
})
</script>

<style scoped lang="scss">
.dataset-management {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;

    .header-left {
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

    .header-right {
      display: flex;
      align-items: center;
    }
  }

  .dataset-list {
    min-height: 400px;

    .dataset-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;
    }
  }

  .pagination {
    margin-top: 24px;
    display: flex;
    justify-content: center;
  }
}
</style>
