<template>
  <div class="data-statistics">
    <div class="page-header">
      <div class="header-left">
        <h2>数据分析</h2>
        <p class="page-desc">KF/QMS/品质案例数据统计与分布概览</p>
      </div>
    </div>

    <el-card class="processor-card" shadow="never">
      <el-radio-group v-model="currentProcessor">
        <el-radio-button
          v-for="p in processorTabs"
          :key="p.name"
          :value="p.name"
        >
          {{ p.display_name }}
        </el-radio-button>
      </el-radio-group>
    </el-card>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <el-statistic title="总事件数" :value="stats?.total_events ?? 0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <el-statistic title="缺陷类型数" :value="stats?.defect_distribution?.length ?? 0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <el-statistic title="客户数" :value="stats?.customer_ranking?.length ?? 0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <el-statistic title="4M分布项" :value="stats?.four_m_distribution?.length ?? 0" />
        </el-card>
      </el-col>
    </el-row>

    <el-card class="distribution-card">
      <template #header>
        <div class="card-header">
          <span>缺陷分布</span>
          <el-button type="default" :icon="Refresh" @click="loadStats">刷新</el-button>
        </div>
      </template>

      <div class="distribution-content">
        <div class="chart-panel">
          <SimplePieChart :data="stats?.defect_distribution ?? []" />
        </div>
        <div class="table-panel">
          <el-table
            :data="stats?.defect_distribution ?? []"
            v-loading="loading"
            stripe
            style="width: 100%"
          >
            <el-table-column prop="name" label="缺陷名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="count" label="数量" width="120" align="center" sortable />
          </el-table>

          <el-empty
            v-if="!loading && (!stats?.defect_distribution || stats.defect_distribution.length === 0)"
            description="暂无数据"
          />
        </div>
      </div>
    </el-card>

    <el-card class="distribution-card" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>客户排名</span>
        </div>
      </template>

      <div class="distribution-content">
        <div class="chart-panel">
          <SimplePieChart :data="stats?.customer_ranking ?? []" />
        </div>
        <div class="table-panel">
          <el-table
            :data="stats?.customer_ranking ?? []"
            v-loading="loading"
            stripe
            style="width: 100%"
          >
            <el-table-column type="index" label="排名" width="70" align="center" />
            <el-table-column prop="name" label="客户名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="count" label="事件数" width="120" align="center" sortable />
          </el-table>

          <el-empty
            v-if="!loading && (!stats?.customer_ranking || stats.customer_ranking.length === 0)"
            description="暂无数据"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { useDocumentStore } from '@/stores/document'
import type { StatisticsData } from '@/types'
import SimplePieChart from '@/components/charts/SimplePieChart.vue'

const store = useDocumentStore()

const defaultProcessors = [
  { name: 'kf', display_name: 'KF快反' },
  { name: 'qms', display_name: 'QMS质量' },
  { name: 'failure_case', display_name: '品质案例' }
]

const processorTabs = computed(() => {
  return store.processors.length > 0 ? store.processors : defaultProcessors
})

const currentProcessor = computed({
  get: () => store.currentProcessor,
  set: (val) => store.setCurrentProcessor(val)
})

const stats = ref<StatisticsData | null>(null)
const loading = ref(false)

async function loadStats() {
  loading.value = true
  try {
    stats.value = await store.getStatistics()
  } catch (e: any) {
    stats.value = null
    ElMessage.error(e?.response?.data?.detail || '加载统计数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (store.processors.length === 0) {
    await store.fetchProcessors()
  }
  await loadStats()
})

watch(
  () => store.currentProcessor,
  () => {
    loadStats()
  }
)
</script>

<style scoped lang="scss">
.data-statistics {
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
  }

  .processor-card {
    margin-bottom: 20px;
  }

  .stats-row {
    margin-bottom: 20px;
  }

  .stat-card {
    text-align: center;
  }

  .distribution-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }

    .distribution-content {
      display: flex;
      gap: 20px;
      align-items: flex-start;
    }

    .chart-panel {
      width: 380px;
      flex-shrink: 0;
    }

    .table-panel {
      flex: 1;
      min-width: 0;
    }
  }

  @media (max-width: 1200px) {
    .distribution-card {
      .distribution-content {
        flex-direction: column;
      }

      .chart-panel {
        width: 100%;
      }
    }
  }
}
</style>
