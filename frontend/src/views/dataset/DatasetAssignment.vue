<template>
  <div class="dataset-assignment-container">
    <el-page-header @back="goBack" :content="`数据集分配管理 - ${datasetName}`" />

    <el-card class="assignment-card">
      <template #header>
        <div class="card-header">
          <span>{{ isPlanning ? '分配规划（未提交）' : '分配情况' }}</span>
          <div class="actions">
            <template v-if="!isPlanning">
              <el-button type="primary" @click="enterPlanningMode">
                <el-icon><Edit /></el-icon>
                开始规划
              </el-button>
              <el-button 
                type="warning" 
                @click="handleClearAssignments"
                :disabled="assignments.length === 0"
              >
                <el-icon><Delete /></el-icon>
                清空分配
              </el-button>
              <el-button @click="loadAssignments">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </template>
            <template v-else>
              <el-button type="success" @click="showAutoAssignDialog">
                <el-icon><MagicStick /></el-icon>
                自动分配
              </el-button>
              <el-button @click="clearPlanning">
                <el-icon><Delete /></el-icon>
                清空规划
              </el-button>
              <el-button @click="cancelPlanning">
                取消
              </el-button>
              <el-button 
                type="primary" 
                @click="submitPlanning"
                :loading="submitting"
              >
                <el-icon><Check /></el-icon>
                确认提交
              </el-button>
            </template>
          </div>
        </div>
      </template>

      <!-- 统计信息 -->
      <div class="stats">
        <el-statistic title="总任务数" :value="stats.total_tasks" />
        <el-statistic title="已分配" :value="stats.total_tasks - stats.unassigned_count" />
        <el-statistic title="未分配" :value="stats.unassigned_count" />
        <el-statistic title="标注员" :value="stats.annotator_count" />
        <el-statistic title="复核员" :value="stats.reviewer_count" />
      </div>

      <!-- 规划模式提示 -->
      <el-alert
        v-if="isPlanning"
        title="规划模式"
        type="info"
        :closable="false"
        style="margin-top: 20px"
      >
        <template #default>
          <div>
            <p>当前处于规划模式，所有更改不会立即生效。</p>
            <p>您可以：</p>
            <ul style="margin: 8px 0; padding-left: 20px;">
              <li>使用"自动分配"快速生成分配方案</li>
              <li>使用 +1/+10/-1/-10 按钮调整每个用户的任务数量</li>
              <li>删除不需要的分配</li>
              <li>点击"确认提交"保存所有更改</li>
            </ul>
            <div v-if="plans.length > 0" style="margin-top: 8px;">
              <div v-if="detectConflicts().length > 0" style="color: #f56c6c;">
                ❌ 检测到 {{ detectConflicts().length }} 个任务冲突，无法提交
              </div>
              <div v-else>
                <div v-if="plans.some(p => p.role === 'annotator')">
                  <span v-if="getUnassignedTasks('annotator').length > 0" style="color: #e6a23c;">
                    ⚠️ 标注员：还有 {{ getUnassignedTasks('annotator').length }} 个任务未分配
                  </span>
                  <span v-else style="color: #67c23a;">
                    ✓ 标注员：所有任务已分配
                  </span>
                </div>
                <div v-if="plans.some(p => p.role === 'reviewer')">
                  <span v-if="getUnassignedTasks('reviewer').length > 0" style="color: #e6a23c;">
                    ⚠️ 复核员：还有 {{ getUnassignedTasks('reviewer').length }} 个任务未分配
                  </span>
                  <span v-else style="color: #67c23a;">
                    ✓ 复核员：所有任务已分配
                  </span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </el-alert>

      <!-- 无任务提示 -->
      <el-alert
        v-if="stats.total_tasks === 0"
        title="该数据集还没有任务"
        type="warning"
        description="请先创建数据集并添加任务后再进行分配。数据集需要包含标注任务才能分配给标注员或复核员。"
        :closable="false"
        style="margin-top: 20px"
      />

      <!-- 任务覆盖可视化 -->
      <div v-if="stats.total_tasks > 0 && assignments.length > 0" class="task-coverage">
        <div class="coverage-title">任务分配可视化</div>
        
        <!-- 标注员可视化 -->
        <div v-if="annotatorAssignments.length > 0" class="coverage-section">
          <div class="coverage-section-title">
            <el-tag type="success" size="small">标注员</el-tag>
            <span class="coverage-count">{{ stats.annotator_count }} 人</span>
          </div>
          <div class="coverage-container">
            <div class="coverage-bar">
              <div 
                v-for="assignment in annotatorAssignments" 
                :key="assignment.assignment_id"
                :style="getCoverageStyle(assignment)"
                :class="['coverage-segment', 'role-annotator']"
                :title="`${assignment.username} (${assignment.task_range})`"
              >
                <span class="coverage-label">{{ assignment.username }}</span>
              </div>
            </div>
            <div class="coverage-legend">
              <span class="legend-start">任务 1</span>
              <span class="legend-end">任务 {{ stats.total_tasks }}</span>
            </div>
          </div>
        </div>

        <!-- 复核员可视化 -->
        <div v-if="reviewerAssignments.length > 0" class="coverage-section">
          <div class="coverage-section-title">
            <el-tag type="warning" size="small">复核员</el-tag>
            <span class="coverage-count">{{ stats.reviewer_count }} 人</span>
          </div>
          <div class="coverage-container">
            <div class="coverage-bar">
              <div 
                v-for="assignment in reviewerAssignments" 
                :key="assignment.assignment_id"
                :style="getCoverageStyle(assignment)"
                :class="['coverage-segment', 'role-reviewer']"
                :title="`${assignment.username} (${assignment.task_range})`"
              >
                <span class="coverage-label">{{ assignment.username }}</span>
              </div>
            </div>
            <div class="coverage-legend">
              <span class="legend-start">任务 1</span>
              <span class="legend-end">任务 {{ stats.total_tasks }}</span>
            </div>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="coverage-stats">
          <el-tag type="success">标注员: {{ stats.annotator_count }}</el-tag>
          <el-tag type="warning">复核员: {{ stats.reviewer_count }}</el-tag>
          <el-tag v-if="stats.unassigned_count > 0" type="info">
            未分配: {{ stats.unassigned_count }}
          </el-tag>
          <el-tag v-else type="success">
            <el-icon><Check /></el-icon> 全部已分配
          </el-tag>
        </div>
      </div>

      <!-- 分配列表 -->
      <el-table
        v-loading="loading"
        :data="displayAssignments"
        style="width: 100%; margin-top: 20px"
      >
        <el-table-column prop="username" label="用户" width="150">
          <template #default="{ row }">
            {{ row.username }}
            <el-tag v-if="row.isNew" type="success" size="small" style="margin-left: 8px;">新增</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.role === 'annotator'" type="success">标注员</el-tag>
            <el-tag v-else type="warning">复核员</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="task_range" label="任务范围" width="150" />
        <el-table-column prop="task_count" label="任务数" width="100" />

        <el-table-column v-if="!isPlanning" label="进度" width="200">
          <template #default="{ row }">
            <div class="progress-info">
              <el-progress
                :percentage="getProgress(row)"
                :color="getProgressColor(row)"
              />
              <span class="progress-text">
                已完成: {{ row.completed_count }} | 复核中: {{ row.in_review_count }}
              </span>
            </div>
          </template>
        </el-table-column>

        <el-table-column v-if="!isPlanning" prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.is_active" type="success">活跃</el-tag>
            <el-tag v-else type="info">已转移</el-tag>
          </template>
        </el-table-column>

        <el-table-column v-if="!isPlanning" label="转移信息" min-width="200">
          <template #default="{ row }">
            <div v-if="!row.is_active && row.transferred_to">
              <div>转移给: {{ row.transferred_to_username }}</div>
              <div class="text-secondary">{{ row.transfer_reason }}</div>
            </div>
            <span v-else>-</span>
          </template>
        </el-table-column>

        <el-table-column v-if="!isPlanning" prop="assigned_at" label="分配时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.assigned_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <template v-if="isPlanning">
              <el-button-group v-if="row.task_range !== '全部'">
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, -10)"
                >
                  -10
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, -1)"
                >
                  -1
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, 1)"
                >
                  +1
                </el-button>
                <el-button
                  size="small"
                  @click="adjustPlanTasks(row.assignment_id, 10)"
                >
                  +10
                </el-button>
              </el-button-group>
              <el-button
                type="danger"
                size="small"
                @click="deletePlanItem(row.assignment_id)"
                style="margin-left: 8px;"
              >
                删除
              </el-button>
            </template>
            <template v-else>
              <el-button
                v-if="row.is_active"
                type="warning"
                size="small"
                @click="showTransferDialog(row)"
              >
                转移
              </el-button>
              <el-button
                v-if="row.is_active"
                type="danger"
                size="small"
                @click="handleCancel(row)"
              >
                取消
              </el-button>
            </template>
          </template>
        </el-table-column>

        <template #empty>
          <el-empty :description="isPlanning ? '暂无规划，点击上方按钮开始规划' : '暂无分配记录，点击【开始规划】按钮开始分配'" />
        </template>
      </el-table>
    </el-card>

    <!-- 分配对话框 -->
    <el-dialog
      v-model="assignDialogVisible"
      title="分配数据集"
      width="500px"
    >
      <el-form :model="assignForm" label-width="100px">
        <el-form-item label="角色">
          <el-radio-group v-model="assignForm.role">
            <el-radio value="annotator">标注员</el-radio>
            <el-radio value="reviewer">复核员</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="用户">
          <el-select v-model="assignForm.user_id" placeholder="请选择用户" filterable>
            <el-option
              v-for="user in availableUsers"
              :key="user.id"
              :label="`${user.username} (${getRoleLabel(user.role)})`"
              :value="user.id"
            />
          </el-select>
          <div v-if="availableUsers.length === 0" style="color: #909399; font-size: 12px; margin-top: 4px;">
            所有用户都已分配为{{ assignForm.role === 'annotator' ? '标注员' : '复核员' }}
          </div>
        </el-form-item>

        <el-form-item label="分配模式">
          <el-radio-group v-model="assignForm.mode">
            <el-radio value="full">整体分配</el-radio>
            <el-radio value="range">范围分配</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="assignForm.mode === 'range'" label="起始索引">
          <el-input-number v-model="assignForm.start_index" :min="1" :max="stats.total_tasks" />
        </el-form-item>

        <el-form-item v-if="assignForm.mode === 'range'" label="结束索引">
          <el-input-number v-model="assignForm.end_index" :min="1" :max="stats.total_tasks" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="assignDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAssign" :loading="submitting" :disabled="availableUsers.length === 0">确定</el-button>
      </template>
    </el-dialog>

    <!-- 自动分配对话框 -->
    <el-dialog
      v-model="autoAssignDialogVisible"
      title="自动分配"
      width="500px"
    >
      <el-form :model="autoAssignForm" label-width="100px">
        <el-form-item label="角色">
          <el-radio-group v-model="autoAssignForm.role">
            <el-radio value="annotator">标注员</el-radio>
            <el-radio value="reviewer">复核员</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="选择用户">
          <el-select
            v-model="autoAssignForm.user_ids"
            multiple
            placeholder="请选择用户"
            filterable
          >
            <el-option
              v-for="user in availableUsers"
              :key="user.id"
              :label="`${user.username} (${getRoleLabel(user.role)})`"
              :value="user.id"
            />
          </el-select>
          <div v-if="availableUsers.length === 0" style="color: #909399; font-size: 12px; margin-top: 4px;">
            所有用户都已分配为{{ autoAssignForm.role === 'annotator' ? '标注员' : '复核员' }}
          </div>
        </el-form-item>

        <el-alert
          title="自动分配将平均分配任务给选中的用户"
          type="info"
          :closable="false"
          style="margin-top: 10px"
        />
      </el-form>

      <template #footer>
        <el-button @click="autoAssignDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAutoAssign" :loading="submitting" :disabled="availableUsers.length === 0">确定</el-button>
      </template>
    </el-dialog>

    <!-- 转移对话框 -->
    <el-dialog
      v-model="transferDialogVisible"
      title="转移分配"
      width="500px"
    >
      <el-form :model="transferForm" label-width="100px">
        <el-form-item label="原用户">
          <el-input :value="currentAssignment?.username" disabled />
        </el-form-item>

        <el-form-item label="新用户">
          <el-select v-model="transferForm.new_user_id" placeholder="请选择用户" filterable>
            <el-option
              v-for="user in availableUsers"
              :key="user.id"
              :label="`${user.username} (${getRoleLabel(user.role)})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="转移原因">
          <el-input
            v-model="transferForm.transfer_reason"
            type="textarea"
            :rows="3"
            placeholder="请输入转移原因"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="transferDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleTransfer" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { h } from 'vue'
import { Plus, MagicStick, Refresh, Delete, Check, Edit } from '@element-plus/icons-vue'
import { datasetApi } from '@/api/dataset'
import { userApi } from '@/api/user'
import type { AssignmentInfo } from '@/types/assignment'
import type { User } from '@/types'

const route = useRoute()
const router = useRouter()

// 数据集ID
const datasetId = computed(() => route.params.id as string)

// 状态
const loading = ref(false)
const submitting = ref(false)
const datasetName = ref('')
const assignments = ref<AssignmentInfo[]>([])
const stats = ref({
  total_tasks: 0,
  unassigned_count: 0,
  annotator_count: 0,
  reviewer_count: 0
})

// 规划模式状态
interface AssignmentPlan {
  id: string
  user_id: number
  username: string
  role: 'annotator' | 'reviewer'
  mode: 'full' | 'range'
  start_index?: number
  end_index?: number
  task_count: number
  isNew: boolean
}

const isPlanning = ref(false)
const plans = ref<AssignmentPlan[]>([])
const originalAssignments = ref<AssignmentInfo[]>([])

// 对话框
const assignDialogVisible = ref(false)
const autoAssignDialogVisible = ref(false)
const transferDialogVisible = ref(false)

// 表单
const assignForm = ref({
  user_id: null as number | null,
  role: 'annotator' as 'annotator' | 'reviewer',
  mode: 'full' as 'full' | 'range',
  start_index: 1,
  end_index: 1
})

const autoAssignForm = ref({
  user_ids: [] as number[],
  role: 'annotator' as 'annotator' | 'reviewer'
})

const transferForm = ref({
  new_user_id: null as number | null,
  transfer_reason: ''
})

const currentAssignment = ref<AssignmentInfo | null>(null)

// 可用用户列表
const availableUsers = ref<User[]>([])
// 所有用户列表（用于过滤）
const allUsers = ref<User[]>([])

// 活跃分配列表
const activeAssignments = computed(() => {
  if (isPlanning.value) {
    return plans.value.filter(p => !p.isNew || p.user_id)
  }
  return assignments.value.filter(a => a.is_active)
})

// 标注员分配列表
const annotatorAssignments = computed(() => {
  return activeAssignments.value.filter(a => a.role === 'annotator')
})

// 复核员分配列表
const reviewerAssignments = computed(() => {
  return activeAssignments.value.filter(a => a.role === 'reviewer')
})

// 显示的分配列表（规划模式显示plans，否则显示assignments）
const displayAssignments = computed(() => {
  if (isPlanning.value) {
    return plans.value.map(plan => ({
      assignment_id: plan.id,
      user_id: plan.user_id,
      username: plan.username,
      role: plan.role,
      task_range: plan.mode === 'full' ? '全部' : `${plan.start_index}-${plan.end_index}`,
      task_count: plan.task_count,
      completed_count: 0,
      in_review_count: 0,
      is_active: true,
      transferred_to: null,
      transferred_to_username: null,
      transferred_at: null,
      transfer_reason: null,
      assigned_by: null,
      assigned_at: new Date().toISOString(),
      isPlanning: true,
      isNew: plan.isNew
    }))
  }
  return assignments.value
})

// 已分配的用户ID集合（按角色区分）
const assignedUserIds = computed(() => {
  const annotators = new Set<number>()
  const reviewers = new Set<number>()
  
  assignments.value.forEach(assignment => {
    if (assignment.is_active) {
      if (assignment.role === 'annotator') {
        annotators.add(assignment.user_id)
      } else if (assignment.role === 'reviewer') {
        reviewers.add(assignment.user_id)
      }
    }
  })
  
  return { annotators, reviewers }
})

// 根据当前选择的角色过滤可用用户
const getAvailableUsersForRole = (role: 'annotator' | 'reviewer') => {
  const assigned = role === 'annotator' 
    ? assignedUserIds.value.annotators 
    : assignedUserIds.value.reviewers
  
  // 只显示标注员（annotator），并且排除已分配的用户
  return allUsers.value.filter(
    user => user.role === 'annotator' && !assigned.has(user.id)
  )
}

// 加载分配情况
const loadAssignments = async () => {
  loading.value = true
  try {
    const response = await datasetApi.getAssignments(datasetId.value)
    
    if (response.success) {
      const data = response.data
      assignments.value = data.assignments
      stats.value = {
        total_tasks: data.total_tasks,
        unassigned_count: data.unassigned_count,
        annotator_count: data.annotator_count,
        reviewer_count: data.reviewer_count
      }
      datasetName.value = data.dataset_name
    }
  } catch (error: any) {
    console.error('加载分配情况失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载分配情况失败')
  } finally {
    loading.value = false
  }
}

// 加载用户列表
const loadUsers = async () => {
  try {
    const users = await userApi.list()
    allUsers.value = Array.isArray(users) ? users : []
    availableUsers.value = allUsers.value.filter(
      (user: User) => user.role === 'annotator'
    )
    
    if (availableUsers.value.length === 0) {
      ElMessage.warning('没有可用的标注员，请先创建用户')
    }
  } catch (error: any) {
    console.error('加载用户列表失败', error)
    ElMessage.error(error.response?.data?.detail || '加载用户列表失败')
  }
}

// 显示分配对话框
const showAssignDialog = () => {
  // 检查数据集是否有任务
  if (stats.value.total_tasks === 0) {
    ElMessage.warning('该数据集没有任务，无法分配。请先添加任务到数据集。')
    return
  }
  
  assignForm.value = {
    user_id: null,
    role: 'annotator',
    mode: 'full',
    start_index: 1,
    end_index: stats.value.total_tasks
  }
  // 更新可用用户列表（过滤已分配的用户）
  availableUsers.value = getAvailableUsersForRole('annotator')
  assignDialogVisible.value = true
}

// 显示自动分配对话框
const showAutoAssignDialog = () => {
  // 检查数据集是否有任务
  if (stats.value.total_tasks === 0) {
    ElMessage.warning('该数据集没有任务，无法分配。请先添加任务到数据集。')
    return
  }
  
  // 如果不在规划模式，先进入规划模式
  if (!isPlanning.value) {
    enterPlanningMode()
  }
  
  autoAssignForm.value = {
    user_ids: [],
    role: 'annotator'
  }
  // 更新可用用户列表（过滤已分配的用户）
  availableUsers.value = getAvailableUsersForRole('annotator')
  autoAssignDialogVisible.value = true
}

// 显示转移对话框
const showTransferDialog = (assignment: AssignmentInfo) => {
  currentAssignment.value = assignment
  transferForm.value = {
    new_user_id: null,
    transfer_reason: ''
  }
  // 更新可用用户列表（过滤已分配的用户，但不包括当前用户）
  const assigned = assignment.role === 'annotator' 
    ? assignedUserIds.value.annotators 
    : assignedUserIds.value.reviewers
  
  availableUsers.value = allUsers.value.filter(
    user => user.role === 'annotator' && 
            (user.id === assignment.user_id || !assigned.has(user.id))
  )
  transferDialogVisible.value = true
}

// 处理分配
const handleAssign = async () => {
  if (!assignForm.value.user_id) {
    ElMessage.warning('请选择用户')
    return
  }

  // 检查数据集是否有任务
  if (stats.value.total_tasks === 0) {
    ElMessage.warning('该数据集没有任务，无法分配')
    return
  }

  // 在规划模式下，添加到规划列表
  if (isPlanning.value) {
    const user = allUsers.value.find(u => u.id === assignForm.value.user_id)
    if (!user) {
      ElMessage.error('用户不存在')
      return
    }
    
    const taskCount = assignForm.value.mode === 'full' 
      ? stats.value.total_tasks
      : (assignForm.value.end_index! - assignForm.value.start_index! + 1)
    
    addPlanItem({
      user_id: assignForm.value.user_id,
      username: user.username,
      role: assignForm.value.role,
      mode: assignForm.value.mode,
      start_index: assignForm.value.mode === 'range' ? assignForm.value.start_index : undefined,
      end_index: assignForm.value.mode === 'range' ? assignForm.value.end_index : undefined,
      task_count: taskCount
    })
    
    ElMessage.success('已添加到规划')
    assignDialogVisible.value = false
    return
  }

  // 非规划模式（旧逻辑）
  // 检查是否重复分配
  const existingAssignment = assignments.value.find(
    a => a.user_id === assignForm.value.user_id && 
         a.role === assignForm.value.role && 
         a.is_active
  )
  
  if (existingAssignment) {
    ElMessage.warning(`该用户已被分配为${assignForm.value.role === 'annotator' ? '标注员' : '复核员'}`)
    return
  }

  // 范围模式验证
  if (assignForm.value.mode === 'range') {
    if (!assignForm.value.start_index || !assignForm.value.end_index) {
      ElMessage.warning('请输入任务范围')
      return
    }
    if (assignForm.value.start_index < 1 || assignForm.value.end_index < assignForm.value.start_index) {
      ElMessage.warning('任务范围无效')
      return
    }
    if (assignForm.value.end_index > stats.value.total_tasks) {
      ElMessage.warning(`结束索引不能超过总任务数 ${stats.value.total_tasks}`)
      return
    }
  }

  submitting.value = true
  try {
    // 构建请求数据
    const requestData: any = {
      user_id: assignForm.value.user_id,
      role: assignForm.value.role,
      mode: assignForm.value.mode
    }
    
    // 只在范围模式下发送索引
    if (assignForm.value.mode === 'range') {
      requestData.start_index = assignForm.value.start_index
      requestData.end_index = assignForm.value.end_index
    }
    
    await datasetApi.assign(datasetId.value, requestData)
    ElMessage.success('分配成功')
    assignDialogVisible.value = false
    await loadAssignments()
  } catch (error: any) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') {
      ElMessage.error(detail)
    } else if (detail?.message) {
      ElMessage.error(detail.message)
    } else {
      ElMessage.error('分配失败')
    }
  } finally {
    submitting.value = false
  }
}

// 处理自动分配
const handleAutoAssign = async () => {
  if (autoAssignForm.value.user_ids.length === 0) {
    ElMessage.warning('请至少选择一个用户')
    return
  }

  // 在规划模式下，直接生成方案
  if (isPlanning.value) {
    await autoAssignInPlanning(autoAssignForm.value.user_ids, autoAssignForm.value.role)
    autoAssignDialogVisible.value = false
    return
  }

  // 非规划模式（旧逻辑，保留兼容）
  const existingCount = assignments.value.filter(
    a => a.is_active && a.role === autoAssignForm.value.role
  ).length

  const confirmMessageVNode = h('div', [
    h('div', '即将自动分配任务：'),
    h('div', [
      h('div', `- 选中用户：${autoAssignForm.value.user_ids.length} 个`),
      h('div', `- 角色：${autoAssignForm.value.role === 'annotator' ? '标注员' : '复核员'}`),
      h('div', `- 总任务数：${stats.value.total_tasks}`),
      h('div', `- 每人约：${Math.ceil(stats.value.total_tasks / autoAssignForm.value.user_ids.length)} 个任务`)
    ]),
    existingCount > 0 ? h('div', { style: 'color: #e6a23c; margin: 8px 0 0 0;' }, [
      `⚠️ 当前已有 ${existingCount} 个${autoAssignForm.value.role === 'annotator' ? '标注员' : '复核员'}分配，自动分配可能会与现有分配冲突。建议先清空现有分配。`
    ]) : null,
    h('div', { style: 'margin-top: 8px;' }, '确认自动分配吗？')
  ])
  try {
    await ElMessageBox.confirm(confirmMessageVNode, '确认自动分配', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info',
      distinguishCancelAndClose: true
    })

    submitting.value = true
    await datasetApi.autoAssign(datasetId.value, autoAssignForm.value as any)
    ElMessage.success('自动分配成功')
    autoAssignDialogVisible.value = false
    await loadAssignments()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('自动分配失败:', error)
      ElMessage.error(error.response?.data?.detail || '自动分配失败')
    }
  } finally {
    submitting.value = false
  }
}

// 处理转移
const handleTransfer = async () => {
  if (!transferForm.value.new_user_id) {
    ElMessage.warning('请选择新用户')
    return
  }

  if (!currentAssignment.value) return

  submitting.value = true
  try {
    await datasetApi.transferAssignment(datasetId.value, {
      old_user_id: currentAssignment.value.user_id,
      new_user_id: transferForm.value.new_user_id,
      role: currentAssignment.value.role as any,
      transfer_mode: 'all',
      transfer_reason: transferForm.value.transfer_reason
    })
    ElMessage.success('转移成功')
    transferDialogVisible.value = false
    loadAssignments()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '转移失败')
  } finally {
    submitting.value = false
  }
}

// 处理取消
const handleCancel = async (assignment: AssignmentInfo) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消用户 ${assignment.username} 的分配吗？`,
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await datasetApi.cancelAssignment(
      datasetId.value,
      assignment.user_id,
      assignment.role
    )
    ElMessage.success('取消成功')
    loadAssignments()
  } catch (error: any) {
    if (error !== 'cancel') {
      const detail = error.response?.data?.detail
      if (typeof detail === 'object' && detail.action === 'transfer') {
        ElMessage.warning('该分配有已完成任务，请使用转移功能')
      } else {
        ElMessage.error(detail || '取消失败')
      }
    }
  }
}

// 批量清空分配
const handleClearAssignments = async () => {
  try {
    const activeCount = assignments.value.filter(a => a.is_active).length
    
    if (activeCount === 0) {
      ElMessage.info('没有需要清空的分配')
      return
    }
    
    await ElMessageBox.confirm(
      `确定要清空所有分配吗？这将取消 ${activeCount} 个活跃分配。`,
      '确认清空',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        distinguishCancelAndClose: true
      }
    )

    const result = await datasetApi.clearAssignments(datasetId.value)
    ElMessage.success(result.message || '清空成功')
    await loadAssignments()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清空分配失败:', error)
      ElMessage.error(error.response?.data?.detail || error.message || '清空失败')
    }
  }
}

// 计算进度
const getProgress = (row: AssignmentInfo) => {
  if (row.task_count === 0) return 0
  return Math.round((row.completed_count / row.task_count) * 100)
}

// 获取进度条颜色
const getProgressColor = (row: AssignmentInfo) => {
  const progress = getProgress(row)
  if (progress === 100) return '#67c23a'
  if (progress >= 50) return '#409eff'
  return '#e6a23c'
}

// 格式化日期
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 获取角色标签
const getRoleLabel = (role: string) => {
  const labels: Record<string, string> = {
    admin: '管理员',
    annotator: '标注员',
    reviewer: '复核员',
    viewer: '浏览员'
  }
  return labels[role] || role
}

// 获取任务覆盖样式
const getCoverageStyle = (assignment: any) => {
  if (!assignment.task_range || assignment.task_range === '全部') {
    return {
      left: '0%',
      width: '100%'
    }
  }
  
  // 解析范围 "1-50"
  const match = assignment.task_range.match(/(\d+)-(\d+)/)
  if (match) {
    const start = parseInt(match[1])
    const end = parseInt(match[2])
    const total = stats.value.total_tasks
    
    if (total === 0) {
      return { left: '0%', width: '0%' }
    }
    
    const leftPercent = ((start - 1) / total) * 100
    const widthPercent = ((end - start + 1) / total) * 100
    
    return {
      left: `${leftPercent}%`,
      width: `${widthPercent}%`
    }
  }
  
  return { left: '0%', width: '0%' }
}

// 格式化任务范围（将离散的任务号合并为范围）
const formatTaskRanges = (tasks: number[]) => {
  if (tasks.length === 0) return ''
  if (tasks.length > 20) return `任务 ${tasks[0]}-${tasks[tasks.length - 1]} 等`
  
  const sorted = [...tasks].sort((a, b) => a - b)
  const ranges: string[] = []
  let start = sorted[0]
  let end = sorted[0]
  
  for (let i = 1; i < sorted.length; i++) {
    if (sorted[i] === end + 1) {
      end = sorted[i]
    } else {
      ranges.push(start === end ? `${start}` : `${start}-${end}`)
      start = sorted[i]
      end = sorted[i]
    }
  }
  ranges.push(start === end ? `${start}` : `${start}-${end}`)
  
  return ranges.join(', ')
}

// 返回
const goBack = () => {
  router.back()
}

// ============================================================================
// 规划模式功能
// ============================================================================

// 进入规划模式
const enterPlanningMode = () => {
  isPlanning.value = true
  originalAssignments.value = [...assignments.value]
  
  // 将现有分配转换为规划
  plans.value = assignments.value
    .filter(a => a.is_active)
    .map(a => convertAssignmentToPlan(a))
}

// 退出规划模式
const exitPlanningMode = () => {
  isPlanning.value = false
  plans.value = []
  originalAssignments.value = []
}

// 取消规划
const cancelPlanning = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要取消规划吗？所有未提交的更改将丢失。',
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    exitPlanningMode()
    ElMessage.info('已取消规划')
  } catch {
    // 用户取消
  }
}

// 转换分配为规划
const convertAssignmentToPlan = (assignment: AssignmentInfo): AssignmentPlan => {
  const isFullMode = assignment.task_range === '全部'
  let start_index, end_index
  
  if (!isFullMode) {
    const match = assignment.task_range.match(/(\d+)-(\d+)/)
    if (match) {
      start_index = parseInt(match[1])
      end_index = parseInt(match[2])
    }
  }
  
  return {
    id: `existing-${assignment.assignment_id}`,
    user_id: assignment.user_id,
    username: assignment.username,
    role: assignment.role as 'annotator' | 'reviewer',
    mode: isFullMode ? 'full' : 'range',
    start_index,
    end_index,
    task_count: assignment.task_count,
    isNew: false
  }
}

// 生成临时ID
const generateTempId = () => {
  return `temp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

// 自动分配（规划模式）
const autoAssignInPlanning = async (userIds: number[], role: 'annotator' | 'reviewer') => {
  const taskCount = stats.value.total_tasks
  const perUser = Math.ceil(taskCount / userIds.length)
  
  const newPlans: AssignmentPlan[] = []
  
  for (let i = 0; i < userIds.length; i++) {
    const userId = userIds[i]
    const user = allUsers.value.find(u => u.id === userId)
    if (!user) continue
    
    const start = i * perUser + 1
    const end = Math.min((i + 1) * perUser, taskCount)
    
    newPlans.push({
      id: generateTempId(),
      user_id: userId,
      username: user.username,
      role,
      mode: 'range',
      start_index: start,
      end_index: end,
      task_count: end - start + 1,
      isNew: true
    })
  }
  
  // 移除同角色的旧分配，保留其他角色的分配
  plans.value = plans.value.filter(p => p.role !== role)
  
  // 追加新分配
  plans.value.push(...newPlans)
  
  ElMessage.success(`已生成 ${newPlans.length} 个${role === 'annotator' ? '标注员' : '复核员'}分配方案`)
}

// 调整分配任务数（智能调整）
const adjustPlanTasks = (planId: string, delta: number) => {
  const planIndex = plans.value.findIndex(p => p.id === planId)
  if (planIndex === -1) return
  
  const plan = plans.value[planIndex]
  const totalTasks = stats.value.total_tasks
  
  // 如果是整体分配，不能调整
  if (plan.mode === 'full') {
    ElMessage.warning('整体分配不支持调整，请删除后重新添加范围分配')
    return
  }
  
  if (!plan.start_index || !plan.end_index) return
  
  // 计算新的结束索引
  let newEndIndex = plan.end_index + delta
  
  // 边界检查
  if (newEndIndex < plan.start_index) {
    ElMessage.warning('任务数不能小于1')
    return
  }
  
  if (newEndIndex > totalTasks) {
    newEndIndex = totalTasks
  }
  
  // 更新当前计划
  plan.end_index = newEndIndex
  plan.task_count = newEndIndex - plan.start_index + 1
  
  // 智能调整后续计划
  if (planIndex < plans.value.length - 1) {
    const nextPlan = plans.value[planIndex + 1]
    if (nextPlan.mode === 'range' && nextPlan.start_index && nextPlan.end_index) {
      // 调整下一个计划的起始索引
      const newNextStart = newEndIndex + 1
      
      if (newNextStart <= totalTasks) {
        nextPlan.start_index = newNextStart
        nextPlan.task_count = nextPlan.end_index - nextPlan.start_index + 1
        
        // 如果下一个计划的任务数变为0或负数，删除它
        if (nextPlan.task_count <= 0) {
          plans.value.splice(planIndex + 1, 1)
          ElMessage.info(`已自动删除 ${nextPlan.username} 的分配（任务数为0）`)
        }
      }
    }
  }
  
  ElMessage.success('已调整任务分配')
}

// 添加单个分配到规划（改为手动指定范围）
const addPlanItem = (item: Omit<AssignmentPlan, 'id' | 'isNew'>) => {
  plans.value.push({
    ...item,
    id: generateTempId(),
    isNew: true
  })
}

// 删除规划项
const deletePlanItem = (planId: string) => {
  const index = plans.value.findIndex(p => p.id === planId)
  if (index !== -1) {
    plans.value.splice(index, 1)
  }
}

// 清空规划
const clearPlanning = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有规划吗？',
      '确认清空',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    plans.value = []
    ElMessage.success('已清空规划')
  } catch {
    // 用户取消
  }
}

// 检测冲突（严格模式，按角色分别检测）
const detectConflicts = () => {
  const conflicts: string[] = []
  
  // 按角色分组
  const annotatorPlans = plans.value.filter(p => p.role === 'annotator')
  const reviewerPlans = plans.value.filter(p => p.role === 'reviewer')
  
  // 检测标注员冲突
  const annotatorConflicts = detectRoleConflicts(annotatorPlans, '标注员')
  conflicts.push(...annotatorConflicts)
  
  // 检测复核员冲突
  const reviewerConflicts = detectRoleConflicts(reviewerPlans, '复核员')
  conflicts.push(...reviewerConflicts)
  
  return conflicts
}

// 检测单个角色的冲突
const detectRoleConflicts = (rolePlans: AssignmentPlan[], roleName: string) => {
  const conflicts: string[] = []
  const taskMap = new Map<number, string[]>()
  
  rolePlans.forEach(plan => {
    if (plan.mode === 'full') {
      for (let i = 1; i <= stats.value.total_tasks; i++) {
        if (!taskMap.has(i)) {
          taskMap.set(i, [])
        }
        taskMap.get(i)!.push(plan.username)
      }
    } else if (plan.start_index && plan.end_index) {
      for (let i = plan.start_index; i <= plan.end_index; i++) {
        if (!taskMap.has(i)) {
          taskMap.set(i, [])
        }
        taskMap.get(i)!.push(plan.username)
      }
    }
  })
  
  // 查找冲突
  taskMap.forEach((users, taskIndex) => {
    if (users.length > 1) {
      conflicts.push(`任务 ${taskIndex} 被多个${roleName}重复分配: ${users.join(', ')}`)
    }
  })
  
  return conflicts
}

// 检查是否有未分配的任务（按角色）
const getUnassignedTasks = (role?: 'annotator' | 'reviewer') => {
  const assignedTasks = new Set<number>()
  
  // 只统计指定角色的分配（如果提供了role参数）
  const filteredPlans = role 
    ? plans.value.filter(p => p.role === role)
    : plans.value
  
  filteredPlans.forEach(plan => {
    if (plan.mode === 'full') {
      for (let i = 1; i <= stats.value.total_tasks; i++) {
        assignedTasks.add(i)
      }
    } else if (plan.start_index && plan.end_index) {
      for (let i = plan.start_index; i <= plan.end_index; i++) {
        assignedTasks.add(i)
      }
    }
  })
  
  const unassigned: number[] = []
  for (let i = 1; i <= stats.value.total_tasks; i++) {
    if (!assignedTasks.has(i)) {
      unassigned.push(i)
    }
  }
  
  return unassigned
}

// 提交规划
const submitPlanning = async () => {
  // 允许提交空规划（用于清空所有分配）
  if (plans.value.length === 0) {
    try {
      await ElMessageBox.confirm(
        '当前规划为空，提交后将清空所有现有分配。\n\n确认提交吗？',
        '确认清空',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
    } catch {
      return
    }
    
    // 直接调用清空API
    submitting.value = true
    try {
      await datasetApi.clearAssignments(datasetId.value)
      ElMessage.success('已清空所有分配')
      exitPlanningMode()
      await loadAssignments()
    } catch (error: any) {
      console.error('清空失败:', error)
      const detail = error.response?.data?.detail
      
      // 检查是否是有进度的分配错误
      if (detail && typeof detail === 'object' && detail.assignments_with_progress) {
        const progressList = detail.assignments_with_progress
          .slice(0, 3)
          .map((item: any) => `${item.username}(${item.role}): 已完成${item.completed}个, 复核中${item.in_review}个`)
          .join('\n')
        
        let message = `无法清空分配，以下用户已有标注进度：\n\n${progressList}`
        
        if (detail.assignments_with_progress.length > 3) {
          message += `\n...还有 ${detail.assignments_with_progress.length - 3} 个用户`
        }
        
        message += '\n\n请使用转移功能将任务转移给其他用户。'
        
        ElMessageBox.alert(message, '无法清空分配', {
          confirmButtonText: '知道了',
          type: 'warning'
        })
      } else {
        ElMessage.error(detail?.message || detail || error.message || '清空失败')
      }
    } finally {
      submitting.value = false
    }
    return
  }
  
  // 检测冲突（严格阻止）
  const conflicts = detectConflicts()
  if (conflicts.length > 0) {
    ElMessage.error(`存在任务冲突，无法提交！\n${conflicts.slice(0, 3).join('\n')}${conflicts.length > 3 ? `\n...还有 ${conflicts.length - 3} 个冲突` : ''}`)
    return
  }
  
  // 检查未分配的任务（按角色分别检查）
  const annotatorPlans = plans.value.filter(p => p.role === 'annotator')
  const reviewerPlans = plans.value.filter(p => p.role === 'reviewer')
  
  const warnings: string[] = []
  
  if (annotatorPlans.length > 0) {
    const unassignedAnnotator = getUnassignedTasks('annotator')
    if (unassignedAnnotator.length > 0) {
      const ranges = formatTaskRanges(unassignedAnnotator)
      warnings.push(`标注员：${unassignedAnnotator.length} 个任务未分配 (${ranges})`)
    }
  }
  
  if (reviewerPlans.length > 0) {
    const unassignedReviewer = getUnassignedTasks('reviewer')
    if (unassignedReviewer.length > 0) {
      const ranges = formatTaskRanges(unassignedReviewer)
      warnings.push(`复核员：${unassignedReviewer.length} 个任务未分配 (${ranges})`)
    }
  }
  
  if (warnings.length > 0) {
    try {
      await ElMessageBox.confirm(
        `存在未分配任务：\n\n${warnings.join('\n')}\n\n是否仍要提交？`,
        '存在未分配任务',
        {
          confirmButtonText: '仍要提交',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
    } catch {
      return
    }
  }
  
  // 确认提交
  try {
    await ElMessageBox.confirm(
      `即将提交 ${plans.value.length} 个分配，这将清空现有分配并创建新的分配。\n\n确认提交吗？`,
      '确认提交',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
  } catch {
    return
  }
  
  submitting.value = true
  try {
    // 构建请求数据
    const requestData = {
      assignments: plans.value.map(plan => ({
        user_id: plan.user_id,
        role: plan.role,
        mode: plan.mode,
        start_index: plan.start_index,
        end_index: plan.end_index
      })),
      clear_existing: true,
      role_filter: undefined  // 不使用角色筛选，允许同时提交标注员和复核员
    }
    
    await datasetApi.batchAssign(datasetId.value, requestData)
    ElMessage.success('分配提交成功')
    
    // 退出规划模式并刷新
    exitPlanningMode()
    await loadAssignments()
  } catch (error: any) {
    console.error('提交规划失败:', error)
    const detail = error.response?.data?.detail
    
    // 检查是否是有进度的分配错误
    if (detail && typeof detail === 'object' && detail.assignments_with_progress) {
      const progressList = detail.assignments_with_progress
        .slice(0, 3)
        .map((item: any) => `${item.username}(${item.role}): 已完成${item.completed}个, 复核中${item.in_review}个`)
        .join('\n')
      
      let message = `无法提交分配，以下用户已有标注进度：\n\n${progressList}`
      
      if (detail.assignments_with_progress.length > 3) {
        message += `\n...还有 ${detail.assignments_with_progress.length - 3} 个用户`
      }
      
      message += '\n\n请使用转移功能将任务转移给其他用户，或取消这些用户的分配后再重新规划。'
      
      ElMessageBox.alert(message, '无法提交分配', {
        confirmButtonText: '知道了',
        type: 'warning'
      })
    } else {
      ElMessage.error(detail?.message || detail || error.message || '提交失败')
    }
  } finally {
    submitting.value = false
  }
}

// 监听角色变化，更新可用用户列表
watch(() => assignForm.value.role, (newRole) => {
  availableUsers.value = getAvailableUsersForRole(newRole)
  // 如果当前选择的用户已被分配，清空选择
  if (assignForm.value.user_id && !availableUsers.value.find(u => u.id === assignForm.value.user_id)) {
    assignForm.value.user_id = null
  }
})

watch(() => autoAssignForm.value.role, (newRole) => {
  availableUsers.value = getAvailableUsersForRole(newRole)
  // 过滤掉已分配的用户
  autoAssignForm.value.user_ids = autoAssignForm.value.user_ids.filter(
    id => availableUsers.value.find(u => u.id === id)
  )
})

onMounted(() => {
  loadAssignments()
  loadUsers()
})
</script>

<style scoped lang="scss">
.dataset-assignment-container {
  padding: 20px;

  .assignment-card {
    margin-top: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .actions {
        display: flex;
        gap: 10px;
      }
    }

    .stats {
      display: flex;
      gap: 40px;
      padding: 20px;
      background: #f5f7fa;
      border-radius: 4px;
    }

    .task-coverage {
      margin-top: 20px;
      padding: 20px;
      background: #fafafa;
      border-radius: 4px;
      border: 1px solid #e4e7ed;

      .coverage-title {
        font-size: 14px;
        font-weight: 500;
        color: #303133;
        margin-bottom: 16px;
      }

      .coverage-section {
        margin-bottom: 20px;

        &:last-of-type {
          margin-bottom: 12px;
        }

        .coverage-section-title {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 8px;
          font-size: 13px;
          color: #606266;

          .coverage-count {
            font-weight: 500;
          }
        }
      }

      .coverage-container {
        margin-bottom: 8px;
      }

      .coverage-bar {
        position: relative;
        height: 40px;
        background: #e4e7ed;
        border-radius: 4px;
        overflow: hidden;
      }

      .coverage-segment {
        position: absolute;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 12px;
        font-weight: 500;
        transition: all 0.3s;
        cursor: pointer;

        &.role-annotator {
          background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
        }

        &.role-reviewer {
          background: linear-gradient(135deg, #e6a23c 0%, #f0b95c 100%);
        }

        &:hover {
          opacity: 0.8;
          transform: translateY(-2px);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }

        .coverage-label {
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          padding: 0 8px;
        }
      }

      .coverage-legend {
        display: flex;
        justify-content: space-between;
        margin-top: 8px;
        font-size: 12px;
        color: #909399;
      }

      .coverage-stats {
        display: flex;
        gap: 12px;
        align-items: center;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #e4e7ed;
      }
    }

    .progress-info {
      display: flex;
      flex-direction: column;
      gap: 4px;

      .progress-text {
        font-size: 12px;
        color: #606266;
      }
    }

    .text-secondary {
      font-size: 12px;
      color: #909399;
      margin-top: 4px;
    }
  }
}
</style>
