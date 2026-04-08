<template>
  <div class="corpus-management">
    <div class="page-header">
      <div class="header-left">
        <h2>语料管理</h2>
        <p class="page-desc">查看和管理已导入的语料记录</p>
      </div>
      <div class="header-right">
        <el-radio-group v-model="viewMode" size="default">
          <el-radio-button value="list">列表视图</el-radio-button>
          <el-radio-button value="grouped">分组视图</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <el-card class="upload-redirect-card" shadow="never">
      <el-alert
        type="info"
        :closable="false"
        show-icon
      >
        <template #title>
          如需上传新的品质失效案例Excel，请前往
          <el-button type="primary" link @click="router.push('/document/import')">
            文档导入
          </el-button>
          页面
        </template>
      </el-alert>
    </el-card>

    <el-card class="preview-card">
      <template #header>
        <div class="card-header">
          <span>{{ viewMode === 'grouped' ? '语料分组（按Excel行）' : '语料列表' }}</span>
          <el-button
            type="primary"
            :icon="Refresh"
            @click="handleRefresh"
          >
            刷新
          </el-button>
        </div>
      </template>
      
      <!-- 列表视图 -->
      <CorpusPreview v-if="viewMode === 'list'" ref="corpusPreviewRef" />
      
      <!-- 分组视图 -->
      <CorpusGroupedView v-else ref="corpusGroupedRef" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Refresh } from '@element-plus/icons-vue'
import CorpusPreview from '@/components/corpus/CorpusPreview.vue'
import CorpusGroupedView from '@/components/corpus/CorpusGroupedView.vue'

const router = useRouter()

const corpusPreviewRef = ref()
const corpusGroupedRef = ref()
const viewMode = ref<'list' | 'grouped'>('grouped')  // 默认使用分组视图

const handleRefresh = () => {
  if (viewMode.value === 'list' && corpusPreviewRef.value) {
    corpusPreviewRef.value.refresh()
  } else if (viewMode.value === 'grouped' && corpusGroupedRef.value) {
    corpusGroupedRef.value.refresh()
  }
}
</script>

<style scoped lang="scss">
.corpus-management {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;

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

  .upload-redirect-card {
    margin-bottom: 20px;
  }

  .preview-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
  }
}
</style>
