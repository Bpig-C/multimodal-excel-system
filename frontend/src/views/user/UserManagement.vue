<template>
  <div class="user-management">
    <!-- 页面标题和操作栏 -->
    <div class="header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        创建用户
      </el-button>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-select
        v-model="filterRole"
        placeholder="筛选角色"
        clearable
        style="width: 200px"
        @change="loadUsers"
      >
        <el-option label="管理员" value="admin" />
        <el-option label="标注员" value="annotator" />
        <el-option label="浏览员" value="viewer" />
      </el-select>

      <el-button @click="loadUsers" :loading="loading">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <!-- 用户列表 -->
    <el-table
      :data="users"
      v-loading="loading"
      stripe
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="200" />
      <el-table-column prop="role" label="角色" width="150">
        <template #default="{ row }">
          <el-tag :type="getRoleTagType(row.role)">
            {{ getRoleLabel(row.role) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="200">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="200">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleEdit(row)"
          >
            编辑
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(row)"
            :disabled="row.id === currentUser?.id"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadUsers"
        @current-change="loadUsers"
      />
    </div>

    <!-- 创建/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '创建用户' : '编辑用户'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="formData.username"
            placeholder="请输入用户名"
            :disabled="dialogMode === 'edit'"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
          <div v-if="dialogMode === 'edit'" class="form-tip">
            留空则不修改密码
          </div>
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="formData.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="标注员" value="annotator" />
            <el-option label="浏览员" value="viewer" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { userApi } from '@/api/user'
import { formatDateTimeShort } from '@/utils/datetime'
import { useUserStore } from '@/stores/user'
import type { User } from '@/types'

// Store
const userStore = useUserStore()
const currentUser = computed(() => userStore.currentUser)

// 数据
const users = ref<User[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const filterRole = ref<string>('')

// 对话框
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const submitting = ref(false)
const formRef = ref<FormInstance>()

// 表单数据
const formData = ref({
  id: 0,
  username: '',
  password: '',
  role: 'annotator' as 'admin' | 'annotator' | 'viewer'
})

// 表单验证规则
const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    {
      validator: (rule, value, callback) => {
        if (dialogMode.value === 'create' && !value) {
          callback(new Error('请输入密码'))
        } else if (value && value.length < 6) {
          callback(new Error('密码长度至少 6 个字符'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

// 加载用户列表
const loadUsers = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const response = await userApi.list({
      role: filterRole.value || undefined,
      skip,
      limit: pageSize.value
    })

    // 后端返回的是数组
    if (Array.isArray(response)) {
      users.value = response
      // 注意：后端没有返回总数，这里使用数组长度
      // 如果返回的数据等于 pageSize，说明可能还有更多数据
      if (response.length === pageSize.value) {
        total.value = (currentPage.value) * pageSize.value + 1
      } else {
        total.value = (currentPage.value - 1) * pageSize.value + response.length
      }
    } else {
      users.value = []
      total.value = 0
    }
  } catch (error: any) {
    console.error('加载用户列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载用户列表失败')
  } finally {
    loading.value = false
  }
}

// 创建用户
const handleCreate = () => {
  dialogMode.value = 'create'
  formData.value = {
    id: 0,
    username: '',
    password: '',
    role: 'annotator'
  }
  dialogVisible.value = true
}

// 编辑用户
const handleEdit = (user: User) => {
  dialogMode.value = 'edit'
  formData.value = {
    id: user.id,
    username: user.username,
    password: '',
    role: user.role
  }
  dialogVisible.value = true
}

// 删除用户
const handleDelete = async (user: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.username}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await userApi.delete(user.id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除用户失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    if (dialogMode.value === 'create') {
      // 创建用户
      await userApi.create({
        username: formData.value.username,
        password: formData.value.password,
        role: formData.value.role
      })
      ElMessage.success('创建成功')
    } else {
        const confirmMessageVNode = h('div', [
          h('div', `确定要删除用户 "${user.username}" 吗？`),
          h('div', { style: 'margin-top: 8px; color: #f56c6c;' }, '此操作不可恢复。')
        ])
        await ElMessageBox.confirm(
          confirmMessageVNode,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
    }

    dialogVisible.value = false
    loadUsers()
  } catch (error: any) {
    console.error('提交失败:', error)
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

// 获取角色标签类型
const getRoleTagType = (role: string) => {
  const typeMap: Record<string, any> = {
    admin: 'danger',
    annotator: 'primary',
    reviewer: 'success'
  }
  return typeMap[role] || ''
}

// 获取角色标签文本
const getRoleLabel = (role: string) => {
  const labelMap: Record<string, string> = {
    admin: '管理员',
    annotator: '标注员',
    viewer: '浏览员'
  }
  return labelMap[role] || role
}

// 格式化日期
const formatDate = (dateString: string) => formatDateTimeShort(dateString)

// 初始化
onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>
