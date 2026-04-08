<template>
  <div class="home-page">
    <el-card class="welcome-card">
      <template #header>
        <h2>欢迎使用面向离散型电子信息制造业的多模态语料库构建平台</h2>
      </template>
      
      <div class="user-info">
        <p>当前用户: <strong>{{ authStore.user?.username }}</strong></p>
        <p>角色: <el-tag :type="roleTagType">{{ roleText }}</el-tag></p>
      </div>
      
      <el-divider />
      
      <div class="quick-actions">
        <h3>快速访问</h3>
        <div class="action-grid">
          <!-- 管理员和标注员 -->
          <el-card v-if="canAccessCorpus" shadow="hover" class="action-card" @click="goTo('/corpus')">
            <el-icon class="action-icon"><Document /></el-icon>
            <div class="action-title">语料管理</div>
            <div class="action-desc">上传和管理语料数据</div>
          </el-card>
          
          <!-- 所有角色 -->
          <el-card shadow="hover" class="action-card" @click="goTo('/datasets')">
            <el-icon class="action-icon"><Folder /></el-icon>
            <div class="action-title">数据集管理</div>
            <div class="action-desc">{{ authStore.user?.role === 'viewer' ? '查看和导出数据集' : '创建和管理数据集' }}</div>
          </el-card>
          
          <!-- 管理员和标注员 -->
          <el-card v-if="canAccessLabels" shadow="hover" class="action-card" @click="goTo('/labels')">
            <el-icon class="action-icon"><PriceTag /></el-icon>
            <div class="action-title">标签配置</div>
            <div class="action-desc">配置实体和关系标签</div>
          </el-card>
          
          <!-- 管理员和标注员 -->
          <el-card v-if="canAccessAnnotations" shadow="hover" class="action-card" @click="goTo('/annotations')">
            <el-icon class="action-icon"><Edit /></el-icon>
            <div class="action-title">标注任务</div>
            <div class="action-desc">进行实体关系标注</div>
          </el-card>
          
          <!-- 管理员和标注员 -->
          <el-card v-if="canAccessReview" shadow="hover" class="action-card" @click="goTo('/review')">
            <el-icon class="action-icon"><Check /></el-icon>
            <div class="action-title">复核管理</div>
            <div class="action-desc">复核标注结果</div>
          </el-card>
          
          <!-- 仅管理员 -->
          <el-card v-if="isAdmin" shadow="hover" class="action-card" @click="goTo('/users')">
            <el-icon class="action-icon"><User /></el-icon>
            <div class="action-title">用户管理</div>
            <div class="action-desc">管理系统用户</div>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Document, Folder, PriceTag, Edit, Check, User } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const roleText = computed(() => {
  const roleMap: Record<string, string> = {
    admin: '管理员',
    annotator: '标注员',
    viewer: '浏览员'
  }
  return roleMap[authStore.user?.role || ''] || authStore.user?.role
})

const roleTagType = computed(() => {
  const typeMap: Record<string, any> = {
    admin: 'danger',
    annotator: 'success',
    viewer: 'info'
  }
  return typeMap[authStore.user?.role || ''] || 'info'
})

const isAdmin = computed(() => authStore.user?.role === 'admin')
const canAccessCorpus = computed(() => ['admin', 'annotator'].includes(authStore.user?.role || ''))
const canAccessLabels = computed(() => ['admin', 'annotator'].includes(authStore.user?.role || ''))
const canAccessAnnotations = computed(() => ['admin', 'annotator'].includes(authStore.user?.role || ''))
const canAccessReview = computed(() => ['admin', 'annotator'].includes(authStore.user?.role || ''))

const goTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped lang="scss">
.home-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;

  .welcome-card {
    h2 {
      margin: 0;
      color: #303133;
    }
  }

  .user-info {
    padding: 16px 0;
    
    p {
      margin: 8px 0;
      font-size: 14px;
      color: #606266;
      
      strong {
        color: #303133;
        font-size: 16px;
      }
    }
  }

  .quick-actions {
    h3 {
      margin: 0 0 20px;
      color: #303133;
      font-size: 18px;
    }

    .action-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 16px;

      .action-card {
        cursor: pointer;
        text-align: center;
        padding: 24px 16px;
        transition: all 0.3s;

        &:hover {
          transform: translateY(-4px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .action-icon {
          font-size: 48px;
          color: #409eff;
          margin-bottom: 12px;
        }

        .action-title {
          font-size: 16px;
          font-weight: 600;
          color: #303133;
          margin-bottom: 8px;
        }

        .action-desc {
          font-size: 13px;
          color: #909399;
          line-height: 1.5;
        }
      }
    }
  }
}
</style>
