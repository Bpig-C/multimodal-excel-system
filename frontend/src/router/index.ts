import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const routes: RouteRecordRaw[] = [
  // 登录页面
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  
  // 主布局
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      // 首页/Dashboard
      {
        path: '',
        name: 'home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
      },

      // 语料管理（浏览员不可访问）
      {
        path: 'corpus',
        name: 'corpus',
        component: () => import('@/views/corpus/CorpusManagement.vue'),
        meta: { title: '语料管理', requiresRole: ['admin', 'annotator'] }
      },
      
      // 数据集管理（所有角色可访问）
      {
        path: 'datasets',
        name: 'datasets',
        component: () => import('@/views/dataset/DatasetManagement.vue'),
        meta: { title: '数据集管理' }
      },
      // Task 47: 我的数据集（必须在 :id 之前！）
      {
        path: 'datasets/my',
        name: 'my-datasets',
        component: () => import('@/views/dataset/MyDatasets.vue'),
        meta: { title: '我的数据集', requiresRole: ['annotator', 'reviewer'] }
      },
      {
        path: 'datasets/:id',
        name: 'dataset-detail',
        component: () => import('@/views/dataset/DatasetDetail.vue'),
        meta: { title: '数据集详情' }
      },
      // Task 47: 数据集分配管理
      {
        path: 'datasets/:id/assign',
        name: 'dataset-assignment',
        component: () => import('@/views/dataset/DatasetAssignment.vue'),
        meta: { title: '数据集分配', requiresAdmin: true }
      },
      
      // 标签配置（浏览员不可访问）
      {
        path: 'labels',
        name: 'labels',
        component: () => import('@/views/label/LabelManagement.vue'),
        meta: { title: '标签配置', requiresRole: ['admin', 'annotator'] }
      },
      
      // 标注任务（浏览员不可访问）
      {
        path: 'annotations',
        name: 'annotations',
        component: () => import('@/views/annotation/AnnotationList.vue'),
        meta: { title: '标注任务', requiresRole: ['admin', 'annotator'] }
      },
      {
        path: 'annotations/:taskId',
        name: 'annotation-editor',
        component: () => import('@/views/annotation/AnnotationPage.vue'),
        meta: { title: '标注编辑器', requiresRole: ['admin', 'annotator'] }
      },
      
      // 复核管理（管理员和标注员可访问）
      {
        path: 'review',
        name: 'review',
        component: () => import('@/views/review/ReviewList.vue'),
        meta: { title: '复核管理', requiresRole: ['admin', 'annotator'] }
      },
      {
        path: 'review/:reviewId',
        name: 'review-detail',
        component: () => import('@/views/review/ReviewDetail.vue'),
        meta: { title: '复核详情', requiresRole: ['admin', 'annotator'] }
      },
      
      // 用户管理（管理员）
      {
        path: 'users',
        name: 'users',
        component: () => import('@/views/user/UserManagement.vue'),
        meta: { title: '用户管理', requiresAdmin: true }
      },

      // 文档管理
      {
        path: 'document/import',
        name: 'DocumentImport',
        component: () => import('@/views/document/DocumentImport.vue'),
        meta: { title: '表格数据导入', requiresAuth: true }
      },
      {
        path: 'document/data-list',
        name: 'DataList',
        component: () => import('@/views/document/DataList.vue'),
        meta: { title: '数据列表', requiresAuth: true }
      },
      {
        path: 'document/statistics',
        name: 'DataStatistics',
        component: () => import('@/views/document/DataStatistics.vue'),
        meta: { title: '数据分析', requiresAuth: true }
      },

      // 多模态格式转换
      {
        path: 'multimodal/export',
        name: 'MultimodalExport',
        component: () => import('@/views/multimodal/MultimodalExport.vue'),
        meta: { title: '多模态语料导出', requiresAuth: true }
      }
    ]
  },
  
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth !== false) {
    if (!authStore.isAuthenticated) {
      // 未登录，跳转到登录页
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
    
    // 检查是否需要管理员权限
    if (to.meta.requiresAdmin && authStore.user?.role !== 'admin') {
      // 权限不足
      ElMessage.warning('权限不足，需要管理员权限')
      next({ name: 'home' })
      return
    }
    
    // 检查是否需要特定角色
    if (to.meta.requiresRole && Array.isArray(to.meta.requiresRole)) {
      const userRole = authStore.user?.role
      if (userRole && !to.meta.requiresRole.includes(userRole)) {
        // 角色不匹配
        ElMessage.warning('权限不足，无法访问该页面')
        next({ name: 'home' })
        return
      }
    }
  }
  
  // 已登录用户访问登录页，跳转到首页
  if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }
  
  next()
})

export default router
