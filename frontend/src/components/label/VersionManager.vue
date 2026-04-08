<template>
  <div class="version-manager">
    <div class="toolbar">
      <el-button type="primary" @click="handleCreateSnapshot">创建版本快照</el-button>
      <el-button @click="handleCompare" :disabled="selectedVersions.length !== 2">
        比较版本
      </el-button>
    </div>

    <el-table
      :data="labelStore.versions"
      v-loading="labelStore.loading"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" :selectable="row => !row.is_active" />
      <el-table-column prop="version_name" label="版本名称" width="200">
        <template #default="{ row }">
          {{ row.version_name }}
          <el-tag v-if="isDefaultVersion(row)" type="warning" size="small" style="margin-left: 8px;">
            默认
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="version_id" label="版本ID" width="150" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="实体类型数" width="120">
        <template #default="{ row }">
          {{ row.entity_types?.length || 0 }}
        </template>
      </el-table-column>
      <el-table-column label="关系类型数" width="120">
        <template #default="{ row }">
          {{ row.relation_types?.length || 0 }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
            {{ row.is_active ? '当前版本' : '历史版本' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button
            size="small"
            @click="handleViewDetail(row)"
          >
            查看详情
          </el-button>
          <el-button
            size="small"
            type="primary"
            @click="handleActivate(row)"
            v-if="!row.is_active"
          >
            激活
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建快照对话框 -->
    <VersionSnapshotDialog
      v-model:visible="snapshotDialogVisible"
      @success="handleSnapshotSuccess"
    />

    <!-- 版本比较对话框 -->
    <VersionCompare
      v-model:visible="compareDialogVisible"
      :version1="selectedVersions[0]"
      :version2="selectedVersions[1]"
    />

    <!-- 版本详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="版本详情"
      width="900px"
    >
      <div v-if="currentVersion">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="版本名称">
            {{ currentVersion.version_name }}
            <el-tag v-if="isDefaultVersion(currentVersion)" type="warning" size="small" style="margin-left: 8px;">
              默认版本（只读）
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="版本ID">{{ currentVersion.version_id }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ currentVersion.description }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentVersion.created_at }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentVersion.is_active ? 'success' : 'info'">
              {{ currentVersion.is_active ? '当前版本' : '历史版本' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider>实体类型 ({{ currentVersion.entity_types?.length || 0 }})</el-divider>
        <el-table :data="currentVersion.entity_types" max-height="300">
          <el-table-column prop="type_name" label="类型名称" width="150" />
          <el-table-column prop="type_name_zh" label="中文名称" width="150" />
          <el-table-column label="颜色" width="100">
            <template #default="{ row }">
              <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
                {{ row.type_name_zh }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
        </el-table>

        <el-divider>关系类型 ({{ currentVersion.relation_types?.length || 0 }})</el-divider>
        <el-table :data="currentVersion.relation_types" max-height="300">
          <el-table-column prop="type_name" label="类型名称" width="150" />
          <el-table-column prop="type_name_zh" label="中文名称" width="150" />
          <el-table-column label="颜色" width="100">
            <template #default="{ row }">
              <el-tag :color="row.color" :style="{ backgroundColor: row.color, color: '#fff' }">
                {{ row.type_name_zh }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { LabelSchemaVersion } from '@/api/label'
import VersionSnapshotDialog from './VersionSnapshotDialog.vue'
import VersionCompare from './VersionCompare.vue'

const labelStore = useLabelStore()
const snapshotDialogVisible = ref(false)
const compareDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const selectedVersions = ref<LabelSchemaVersion[]>([])
const currentVersion = ref<LabelSchemaVersion | null>(null)

// 判断是否为默认版本
const isDefaultVersion = (version: LabelSchemaVersion) => {
  return version.version_id === 'DEFAULT_V1.0'
}

const handleCreateSnapshot = () => {
  snapshotDialogVisible.value = true
}

const handleSnapshotSuccess = () => {
  ElMessage.success('版本快照创建成功')
  labelStore.fetchVersions()
}

const handleSelectionChange = (selection: LabelSchemaVersion[]) => {
  selectedVersions.value = selection
}

const handleCompare = () => {
  if (selectedVersions.value.length === 2) {
    compareDialogVisible.value = true
  }
}

const handleViewDetail = (row: LabelSchemaVersion) => {
  currentVersion.value = row
  detailDialogVisible.value = true
}

const handleActivate = async (row: LabelSchemaVersion) => {
  try {
    const message = isDefaultVersion(row)
      ? `确定要切换回默认配置吗？这将恢复系统默认的16种实体类型和1种关系类型。`
      : `确定要激活版本 "${row.version_name}" 吗？这将替换当前的标签体系配置。`
    
    await ElMessageBox.confirm(
      message,
      '警告',
      { type: 'warning' }
    )
    await labelStore.activateVersion(row.version_id)
    ElMessage.success('版本激活成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('激活失败')
    }
  }
}

onMounted(() => {
  labelStore.fetchVersions()
})
</script>

<style scoped>
.version-manager {
  padding: 20px;
}

.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
</style>
