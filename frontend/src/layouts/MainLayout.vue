<template>
  <el-container class="main-layout">
    <el-header class="header">
      <div class="header-left">
        <router-link to="/" class="title-link">
          <h1 class="title">{{ appTitle }}</h1>
          <span class="subtitle">本系统重点面向KF、QMS和品质失效案例及视频数据的多模态标注工作。</span>
        </router-link>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            <span>{{ authStore.user?.username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container>
      <el-aside width="240px" class="aside">
        <el-menu
          :default-active="activeMenu"
          router
          class="menu"
        >
          <el-sub-menu index="/source-management">
            <template #title>
              <el-icon><FolderOpened /></el-icon>
              <span>数据源管理</span>
            </template>
            <el-menu-item index="/document/import">表格数据导入</el-menu-item>
            <el-menu-item index="/document/data-list">数据列表</el-menu-item>
            <el-menu-item index="/document/statistics">数据分析</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/annotation-management">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>实体关系标注</span>
            </template>
            <el-menu-item
              v-if="authStore.user?.role !== 'viewer'"
              index="/corpus"
            >
              标注原始语料管理
            </el-menu-item>
            <el-menu-item
              v-if="['admin', 'viewer'].includes(authStore.user?.role)"
              index="/datasets"
            >
              数据集管理
            </el-menu-item>
            <el-menu-item
              v-if="authStore.user?.role !== 'viewer'"
              index="/labels"
            >
              实体关系标签配置
            </el-menu-item>
            <el-menu-item
              v-if="authStore.user?.role !== 'viewer'"
              index="/annotations"
            >
              实体关系标注任务
            </el-menu-item>
            <el-menu-item
              v-if="['admin', 'annotator'].includes(authStore.user?.role)"
              index="/review"
            >
              标注复核管理
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/multimodal-convert">
            <template #title>
              <el-icon><Share /></el-icon>
              <span>多模态格式转换</span>
            </template>
            <el-menu-item index="/multimodal/export">多模态语料导出</el-menu-item>
          </el-sub-menu>

          <el-menu-item
            v-if="authStore.user?.role === 'admin'"
            index="/users"
          >
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  User,
  Document,
  FolderOpened,
  Share
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const appTitle = import.meta.env.VITE_APP_TITLE || '面向离散型电子信息制造业的多模态语料库构建平台'

const activeMenu = computed(() => route.path)

const handleCommand = (command: string) => {
  if (command === 'logout') {
    authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #409eff;
  color: white;
  padding: 0 20px;
}

.header-left .title {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.header-left .subtitle {
  font-size: 11px;
  font-weight: normal;
  margin-left: 12px;
  opacity: 0.85;
}

.title-link {
  text-decoration: none;
  color: inherit;
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e4e7ed;
}

.menu {
  border-right: none;
  height: 100%;
}

.main {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>
