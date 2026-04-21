<template>
  <div class="dataset-detail">
    <div v-loading="loading" class="detail-container">
      <el-page-header @back="handleBack">
        <template #content>
          <div class="page-header-content">
            <span class="page-title">{{ dataset?.name || '数据集详情' }}</span>
            <!-- Task 47: 添加分配管理按钮（仅管理员可见） -->
            <el-button
              v-if="authStore.user?.role === 'admin'"
              type="primary"
              @click="goToAssignment"
            >
              <el-icon><Setting /></el-icon>
              分配管理
            </el-button>
          </div>
        </template>
      </el-page-header>

      <div v-if="dataset" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="数据集名称">
            {{ dataset.name }}
          </el-descriptions-item>
          <el-descriptions-item label="数据集ID">
            {{ dataset.dataset_id }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ dataset.description || '暂无描述' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ dataset.created_at }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">
            {{ dataset.updated_at }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="statistics-section">
          <h3>统计信息</h3>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-statistic title="总任务数" :value="dataset.statistics?.total_tasks || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="已完成" :value="dataset.statistics?.completed_tasks || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="已复核" :value="dataset.statistics?.reviewed_tasks || 0" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="待处理" :value="dataset.statistics?.pending_tasks || 0" />
            </el-col>
          </el-row>
        </div>

        <!-- 标注任务列表 -->
        <div class="tasks-section">
          <div class="section-header">
            <h3>标注任务列表</h3>
            <div class="header-actions">
              <el-button
                v-if="authStore.user?.role !== 'viewer' && selectedTasks.length > 0"
                type="success"
                size="small"
                @click="handleBatchAnnotateSelected"
              >
                批量标注选中 ({{ selectedTasks.length }})
              </el-button>
              <el-button
                v-if="authStore.user?.role !== 'viewer'"
                type="primary"
                size="small"
                @click="handleBatchAnnotateAll"
              >
                批量标注全部
              </el-button>
              <!-- 添加语料按钮（仅管理员） -->
              <el-button
                v-if="authStore.user?.role === 'admin'"
                type="success"
                size="small"
                :icon="Plus"
                @click="openAddCorpusDialog"
              >
                添加语料
              </el-button>
            </div>
          </div>

          <el-table
            v-loading="tasksLoading"
            :data="taskList"
            stripe
            style="width: 100%"
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              v-if="authStore.user?.role !== 'viewer'"
              type="selection"
              width="55"
              :selectable="isTaskSelectable"
            />
            <el-table-column prop="task_id" label="任务ID" width="180" />
            <el-table-column label="语料文本" min-width="300">
              <template #default="{ row }">
                <div class="text-preview">
                  {{ row.corpus_text || '暂无文本' }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="标注类型" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.annotation_type === 'automatic'" type="info">
                  自动
                </el-tag>
                <el-tag v-else-if="row.annotation_type === 'manual'" type="success">
                  手动
                </el-tag>
                <el-tag v-else type="warning">待标注</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="实体数" width="80">
              <template #default="{ row }">
                {{ row.entity_count || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="关系数" width="80">
              <template #default="{ row }">
                {{ row.relation_count || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="更新时间" width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.updated_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-if="authStore.user?.role !== 'viewer'"
                  type="primary"
                  size="small"
                  @click="handleAnnotate(row)"
                >
                  {{ row.status === 'pending' ? '开始标注' : '继续标注' }}
                </el-button>
                <el-button
                  v-else
                  type="info"
                  size="small"
                  @click="handleAnnotate(row)"
                >
                  查看
                </el-button>
                <!-- 删除任务按钮（仅管理员） -->
                <el-button
                  v-if="authStore.user?.role === 'admin'"
                  type="danger"
                  size="small"
                  :icon="Delete"
                  @click="handleDeleteTask(row)"
                />
              </template>
            </el-table-column>
          </el-table>

          <div v-if="taskTotal > 0" class="pagination">
            <el-pagination
              v-model:current-page="taskPage"
              v-model:page-size="taskPageSize"
              :total="taskTotal"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="fetchTasks"
              @current-change="fetchTasks"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 添加语料对话框 -->
    <el-dialog
      v-model="addCorpusDialogVisible"
      title="添加语料到数据集"
      width="80%"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <CorpusSelector ref="corpusSelectorRef" />
      <template #footer>
        <el-button @click="addCorpusDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="addTasksLoading" @click="confirmAddCorpus">
          确认添加
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Setting, Plus, Delete } from '@element-plus/icons-vue'
import { useDatasetStore, useAuthStore } from '@/stores'
import CorpusSelector from '@/components/dataset/CorpusSelector.vue'
import type { Dataset } from '@/types'
import { formatDateTime } from '@/utils/datetime'
import { getStatusText, getStatusType } from '@/constants/taskStatus'
import { annotationApi } from '@/api/annotation'

interface AnnotationTask {
  id: number
  task_id: string
  corpus_text: string
  status: string
  annotation_type: string
  entity_count: number
  relation_count: number
  updated_at: string
}

const route = useRoute()
const router = useRouter()
const datasetStore = useDatasetStore()
const authStore = useAuthStore()

const loading = ref(false)
const tasksLoading = ref(false)
const dataset = ref<Dataset | null>(null)
const taskList = ref<AnnotationTask[]>([])
const taskPage = ref(1)
const taskPageSize = ref(20)
const taskTotal = ref(0)

// 添加语料对话框
const addCorpusDialogVisible = ref(false)
const addTasksLoading = ref(false)
const corpusSelectorRef = ref<InstanceType<typeof CorpusSelector> | null>(null)

const handleBack = () => {
  router.push({ name: 'datasets' })
}

// Task 47: 跳转到分配管理页面
const goToAssignment = () => {
  if (dataset.value) {
    router.push({
      name: 'dataset-assignment',
      params: { id: dataset.value.dataset_id }
    })
  }
}

const fetchDetail = async () => {
  const id = route.params.id as string
  if (!id) {
    handleBack()
    return
  }

  loading.value = true
  try {
    dataset.value = await datasetStore.fetchDetail(id)
    // 获取任务列表
    await fetchTasks()
  } catch (error: any) {
    console.error('获取数据集详情失败:', error)
    
    // 如果是404错误，说明后端API还未实现，使用模拟数据
    if (error.response?.status === 404) {
      ElMessage.warning('后端API未实现，使用模拟数据')
      // 使用模拟数据
      dataset.value = {
        id: 1,
        dataset_id: id,
        name: `数据集 ${id}`,
        description: '这是一个测试数据集（模拟数据）',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        statistics: {
          total_tasks: 0,
          completed_tasks: 0,
          reviewed_tasks: 0,
          pending_tasks: 0
        }
      } as any
    } else {
      ElMessage.error('获取数据集详情失败')
      handleBack()
    }
  } finally {
    loading.value = false
  }
}

const fetchTasks = async () => {
  if (!dataset.value) return

  tasksLoading.value = true
  try {
    // 调用API获取任务列表
    const response = await datasetStore.fetchDatasetTasks(
      dataset.value.dataset_id,
      {
        page: taskPage.value,
        page_size: taskPageSize.value
      }
    )
    
    const newItems = response.items || []

    // 保留本地仍在 processing 的任务，避免后台查询暂时拿不到导致列表瞬移
    const processingCache = new Map(
      taskList.value
        .filter(t => t.status === 'processing')
        .map(t => [t.task_id, t])
    )
    const merged = newItems.map(item => processingCache.get(item.task_id) || item)

    taskList.value = merged
    taskTotal.value = response.total || merged.length
  } catch (error: any) {
    console.error('获取任务列表失败:', error)
    
    // 如果是404，说明后端API未实现，暂时不显示错误
    if (error.response?.status === 404) {
      console.warn('任务列表API未实现，显示空列表')
      taskList.value = []
      taskTotal.value = 0
    } else {
      ElMessage.error('获取任务列表失败')
    }
  } finally {
    tasksLoading.value = false
  }
}

const handleAnnotate = (task: AnnotationTask) => {
  // 跳转到标注页面
  router.push({
    name: 'annotation-editor',
    params: { taskId: task.task_id }
  })
}

// 刷新统计数据（详情接口现在内嵌 statistics）
const refreshDetail = async () => {
  if (!dataset.value) return
  try {
    dataset.value = await datasetStore.fetchDetail(dataset.value.dataset_id)
  } catch {
    // ignore
  }
}

// 打开"添加语料"对话框
const openAddCorpusDialog = () => {
  addCorpusDialogVisible.value = true
}

// 确认添加语料
const confirmAddCorpus = async () => {
  if (!dataset.value || !corpusSelectorRef.value) return

  const selectedIds: string[] = corpusSelectorRef.value.getSelectedIds()
  if (selectedIds.length === 0) {
    ElMessage.warning('请先选择要添加的语料')
    return
  }

  // CorpusSelector 返回 text_id (string)，但后端需要 corpus.id (integer)
  // 通过 getSelectedCorpus() 获取含 id 字段的完整 Corpus 对象
  const selectedCorpus = corpusSelectorRef.value.getSelectedCorpus()
  const corpusIds: number[] = selectedCorpus
    .map((c: any) => c.id)
    .filter((id: number | undefined): id is number => id !== undefined)

  if (corpusIds.length === 0) {
    ElMessage.error('无法获取语料数据库ID，请重试')
    return
  }
  if (corpusIds.length !== selectedCorpus.length) {
    ElMessage.warning(`部分语料缺少ID信息，将添加 ${corpusIds.length} 条`)
  }

  addTasksLoading.value = true
  try {
    const result = await datasetStore.addTasksToDataset(dataset.value.dataset_id, corpusIds)
    ElMessage.success(`添加成功：新增 ${result.added} 条，跳过重复 ${result.skipped} 条`)
    addCorpusDialogVisible.value = false
    // 刷新任务列表和统计
    await Promise.all([fetchTasks(), refreshDetail()])
  } catch (error: any) {
    ElMessage.error(error.message || '添加语料失败')
  } finally {
    addTasksLoading.value = false
  }
}

// 删除单个任务
const handleDeleteTask = async (task: AnnotationTask) => {
  if (!dataset.value) return

  try {
    const confirmMessageVNode = h('div', [
      h('div', `确定要删除任务 ${task.task_id} 吗？`),
      h('div', { style: 'margin-top: 8px; color: #f56c6c;' }, '此操作将同时删除其下的所有标注数据且不可恢复。')
    ])
    await ElMessageBox.confirm(
      confirmMessageVNode,
      '删除确认',
      {
        type: 'warning',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        confirmButtonClass: 'el-button--danger'
      }
    )
  } catch {
    return // 用户取消
  }

  try {
    await datasetStore.removeTaskFromDataset(dataset.value.dataset_id, task.task_id)
    ElMessage.success('任务删除成功')
    // 刷新列表和统计
    await Promise.all([fetchTasks(), refreshDetail()])
  } catch (error: any) {
    ElMessage.error(error.message || '删除任务失败')
  }
}

const selectedTasks = ref<AnnotationTask[]>([])

// 处理任务选择变化
const handleSelectionChange = (selection: AnnotationTask[]) => {
  selectedTasks.value = selection
}

// 判断任务是否可选择（只有pending状态的任务可以批量标注）
const isTaskSelectable = (row: AnnotationTask) => {
  return row.status === 'pending'
}

// 批量标注选中的任务
const handleBatchAnnotateSelected = async () => {
  if (selectedTasks.value.length === 0) {
    ElMessage.warning('请先选择要标注的任务')
    return
  }
  
  try {
    const taskIds = selectedTasks.value.map(t => t.task_id)
    await triggerBatchAnnotation(taskIds)
  } catch (error: any) {
    console.error('批量标注失败:', error)
    ElMessage.error(error.message || '批量标注失败')
  }
}

// 批量标注全部pending任务
const handleBatchAnnotateAll = async () => {
  const pendingTasks = taskList.value.filter(t => t.status === 'pending')
  
  if (pendingTasks.length === 0) {
    ElMessage.warning('没有待标注的任务')
    return
  }
  
  try {
    await triggerBatchAnnotation()
  } catch (error: any) {
    console.error('批量标注失败:', error)
    ElMessage.error(error.message || '批量标注失败')
  }
}

// 触发批量标注
const triggerBatchAnnotation = async (taskIds?: string[]) => {
  if (!dataset.value) {
    ElMessage.error('数据集信息未加载')
    return
  }
  
  try {
    const response = await annotationApi.triggerBatchAnnotation({
      dataset_id: dataset.value.dataset_id,
      task_ids: taskIds
    })

    if (response.success) {
      const jobId = response.data.job_id
      const totalTasks = response.data.total_tasks

      ElMessage.success(`批量标注任务已创建，共 ${totalTasks} 个任务`)

      // 清除选择
      selectedTasks.value = []

      // 前端先将目标任务标记为处理中，保持当前位置
      const targetIds = taskIds && taskIds.length > 0
        ? new Set(taskIds)
        : new Set(taskList.value.filter(t => t.status === 'pending').map(t => t.task_id))

      taskList.value = taskList.value.map(t => {
        if (targetIds.has(t.task_id)) {
          return { ...t, status: 'processing', annotation_type: t.annotation_type || 'automatic' }
        }
        return t
      })

      // 略延时再拉取最新结果，避免立刻翻页丢失位置
      setTimeout(() => {
        fetchTasks()
      }, 5000)
    }
  } catch (error: any) {
    throw error
  }
}

const handleBatchAnnotate = () => {
  // 保留旧方法以兼容
  handleBatchAnnotateAll()
}

// formatDateTime 已从 @/utils/datetime 导入

onMounted(() => {
  fetchDetail()
})
</script>

<style scoped lang="scss">
.dataset-detail {
  padding: 20px;

  .detail-container {
    min-height: 400px;
  }

  .page-title {
    font-size: 20px;
    font-weight: 600;
  }

  .page-header-content {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .detail-content {
    margin-top: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .statistics-section,
  .tasks-section {
    h3 {
      margin: 0 0 16px;
      font-size: 16px;
      font-weight: 600;
      color: #303133;
    }
  }

  .tasks-section {
    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      h3 {
        margin: 0;
      }

      .header-actions {
        display: flex;
        gap: 8px;
      }
    }

    .text-preview {
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      color: #606266;
    }

    .pagination {
      margin-top: 16px;
      display: flex;
      justify-content: center;
    }
  }
}
</style>
