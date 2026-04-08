<template>
  <div class="label-management">
    <el-page-header @back="$router.back()" title="返回">
      <template #content>
        <span class="page-title">标签体系管理</span>
      </template>
      <template #extra>
        <el-space>
          <el-button @click="handleImport">导入配置</el-button>
          <el-button @click="handleExport">导出配置</el-button>
          <el-button type="primary" @click="handlePromptPreview">Prompt预览</el-button>
        </el-space>
      </template>
    </el-page-header>

    <el-tabs v-model="activeTab" class="label-tabs">
      <el-tab-pane label="实体类型" name="entity">
        <EntityTypeConfig />
      </el-tab-pane>
      <el-tab-pane label="关系类型" name="relation">
        <RelationTypeConfig />
      </el-tab-pane>
      <el-tab-pane label="版本管理" name="version">
        <VersionManager />
      </el-tab-pane>
    </el-tabs>

    <!-- 导入对话框 -->
    <LabelImportExport
      v-model:visible="importDialogVisible"
      mode="import"
      @success="handleImportSuccess"
    />

    <!-- Prompt预览对话框 -->
    <PromptPreview
      v-model:visible="promptPreviewVisible"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import EntityTypeConfig from '@/components/label/EntityTypeConfig.vue'
import RelationTypeConfig from '@/components/label/RelationTypeConfig.vue'
import VersionManager from '@/components/label/VersionManager.vue'
import LabelImportExport from '@/components/label/LabelImportExport.vue'
import PromptPreview from '@/components/label/PromptPreview.vue'

const labelStore = useLabelStore()
const activeTab = ref('entity')
const importDialogVisible = ref(false)
const promptPreviewVisible = ref(false)

const handleImport = () => {
  importDialogVisible.value = true
}

const handleExport = async () => {
  try {
    const data = await labelStore.exportLabels()
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `label-config-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handlePromptPreview = () => {
  promptPreviewVisible.value = true
}

const handleImportSuccess = () => {
  ElMessage.success('导入成功')
}
</script>

<style scoped>
.label-management {
  padding: 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
}

.label-tabs {
  margin-top: 20px;
}
</style>
