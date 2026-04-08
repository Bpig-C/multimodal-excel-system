<template>
  <div class="data-list">
    <div class="page-header">
      <div class="header-left">
        <h2>数据列表</h2>
        <p class="page-desc">查看已导入的 KF/QMS/品质案例数据记录</p>
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

    <el-card class="table-card">
      <el-table
        :data="listData"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column :label="'\u56fe\u7247'" min-width="180">
          <template #default="{ row }">
            <div v-if="getRowImageUrls(row).length" class="image-cell">
              <el-image
                v-for="(img, idx) in getRowImageUrls(row).slice(0, 3)"
                :key="`${row.id}-${idx}`"
                :src="toAbsoluteImageUrl(img)"
                :preview-src-list="getRowImageUrls(row).map((u) => toAbsoluteImageUrl(u))"
                preview-teleported
                fit="cover"
                class="thumb"
              >
                <template #error>
                  <div class="thumb-error">{{ '\u9884\u89c8\u5f02\u5e38' }}</div>
                </template>
              </el-image>
              <span
                v-if="getRowImageUrls(row).length > 3"
                class="image-more"
              >
                +{{ getRowImageUrls(row).length - 3 }}
              </span>
              <span
                v-if="getRowMissingImageCount(row) > 0"
                class="image-missing"
              >
                {{ '\u7f3a\u5931' }}{{ getRowMissingImageCount(row) }}{{ '\u5f20' }}
              </span>
            </div>
            <span
              v-else-if="getRowMissingImageCount(row) > 0"
              class="no-image warning"
            >
              {{ '\u672a\u4e0a\u4f20\u56fe\u7247' }}
            </span>
            <span v-else class="no-image">{{ '\u65e0\u56fe\u7247' }}</span>
          </template>
        </el-table-column>

        <el-table-column
          v-for="col in tableColumns"
          :key="col"
          :prop="col"
          :label="getColumnLabel(col)"
          show-overflow-tooltip
          min-width="140"
        />
      </el-table>

      <el-empty
        v-if="!loading && listData.length === 0"
        description="暂无数据"
      />

      <div class="table-footer">
        <div class="total-hint" v-if="totalCount > 0">
          共 {{ totalCount }} 条记录
        </div>

        <el-pagination
          v-if="totalCount > 0"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalCount"
          :page-size="pageSize"
          :current-page="currentPage"
          :page-sizes="pageSizeOptions"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useDocumentStore } from '@/stores/document'
import { documentApi } from '@/api/document'

const store = useDocumentStore()

const defaultProcessors = [
  { name: 'kf', display_name: 'KF快反' },
  { name: 'qms', display_name: 'QMS质量' },
  { name: 'failure_case', display_name: '品质案例' }
]

const PROCESSOR_COLUMN_LABELS: Record<string, Record<string, string>> = {
  kf: {
    id: '快反编号',
    occurrence_time: '发生时间',
    problem_analysis: '问题原因及分析',
    short_term_measure: '短期改善措施',
    long_term_measure: '长期改善措施',
    classification: '所属分类',
    data_source: '数据源'
  },
  qms: {
    id: '制令单号',
    entry_time: '录入时间',
    model: '型号',
    barcode: '条码',
    position: '位号',
    status: '状态',
    data_source: '数据源'
  },
  failure_case: {
    id: '记录ID',
    source_file: '源文件',
    source_row: '源行号',
    问题分类: '问题分类',
    '客户/发生工程/供应商': '客户/发生工程/供应商',
    质量问题: '质量问题',
    问题描述: '问题描述',
    问题处理: '问题处理',
    原因分析: '原因分析',
    采取措施: '采取措施',
    闂鍒嗙被: '问题分类',
    '瀹㈡埛/鍙戠敓宸ョ▼/渚涘簲鍟?': '客户/发生工程/供应商',
    璐ㄩ噺闂: '质量问题',
    闂鎻忚堪: '问题描述',
    闂澶勭悊: '问题处理',
    鍘熷洜鍒嗘瀽: '原因分析',
    閲囧彇鎺柦: '采取措施',
    data_source: '数据源'
  }
}

const processorTabs = computed(() => {
  return store.processors.length > 0 ? store.processors : defaultProcessors
})

const currentProcessor = computed({
  get: () => store.currentProcessor,
  set: (val) => store.setCurrentProcessor(val)
})

const listData = ref<any[]>([])
const totalCount = ref(0)
const loading = ref(false)

const currentPage = ref(1)
const pageSize = ref(50)
const pageSizeOptions = [20, 50, 100, 200]

const processorFieldMapping = ref<Record<string, string>>({})
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL.replace(/\/api\/v1\/?$/, '')
const hiddenColumns = new Set([
  'image_paths',
  'image_preview_urls',
  'image_count',
  'image_available_count',
  'image_missing_count'
])

const tableColumns = computed(() => {
  if (listData.value.length === 0) return []
  return Object.keys(listData.value[0]).filter((key) => !hiddenColumns.has(key))
})

function getColumnLabel(column: string) {
  const staticMap = PROCESSOR_COLUMN_LABELS[currentProcessor.value] || {}
  if (staticMap[column]) return staticMap[column]

  if (processorFieldMapping.value[column]) {
    return processorFieldMapping.value[column]
  }

  if (column === 'id' && processorFieldMapping.value.event_id) {
    return processorFieldMapping.value.event_id
  }

  return column
}

function toAbsoluteImageUrl(path: string) {
  if (!path) return ''
  if (/^https?:\/\//i.test(path)) return path
  const normalized = path.startsWith('/') ? path : `/${path}`
  return `${apiBaseUrl}${normalized}`
}

function getRowImageUrls(row: any): string[] {
  if (Array.isArray(row?.image_preview_urls)) {
    return row.image_preview_urls
  }
  if (typeof row?.image_preview_urls === 'string' && row.image_preview_urls.trim()) {
    return [row.image_preview_urls.trim()]
  }
  return []
}

function getRowMissingImageCount(row: any): number {
  if (typeof row?.image_missing_count === 'number' && row.image_missing_count > 0) {
    return row.image_missing_count
  }
  const total = typeof row?.image_count === 'number' ? row.image_count : 0
  const available = getRowImageUrls(row).length
  const missing = total - available
  return missing > 0 ? missing : 0
}

async function loadFieldMapping() {
  try {
    const res = await documentApi.getFieldMapping(store.currentProcessor)
    processorFieldMapping.value = res.field_mapping || {}
  } catch {
    processorFieldMapping.value = {}
  }
}

async function loadList() {
  loading.value = true
  try {
    const res = await documentApi.getDataList(store.currentProcessor, {
      page: currentPage.value,
      page_size: pageSize.value
    })
    listData.value = res.data
    totalCount.value = res.total_count ?? res.count
  } catch (e: any) {
    listData.value = []
    totalCount.value = 0
    ElMessage.error(e?.response?.data?.detail || '加载数据列表失败')
  } finally {
    loading.value = false
  }
}

function handlePageChange(page: number) {
  currentPage.value = page
  loadList()
}

function handleSizeChange(size: number) {
  pageSize.value = size
  currentPage.value = 1
  loadList()
}

onMounted(async () => {
  if (store.processors.length === 0) {
    await store.fetchProcessors()
  }
  await loadFieldMapping()
  await loadList()
})

watch(
  () => store.currentProcessor,
  async () => {
    currentPage.value = 1
    await loadFieldMapping()
    await loadList()
  }
)
</script>

<style scoped lang="scss">
.data-list {
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

  .processor-card,
  .table-card {
    margin-bottom: 20px;
  }

  .table-footer {
    margin-top: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .total-hint {
    font-size: 14px;
    color: #909399;
    white-space: nowrap;
  }

  .image-cell {
    display: flex;
    align-items: center;
    gap: 6px;
    min-height: 48px;

    .thumb {
      width: 42px;
      height: 42px;
      border-radius: 4px;
      border: 1px solid #ebeef5;
      overflow: hidden;
      flex-shrink: 0;
    }

    .thumb-error {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      font-size: 12px;
      color: #909399;
      background: #f5f7fa;
    }

    .image-more {
      font-size: 12px;
      color: #909399;
      white-space: nowrap;
    }

    .image-missing {
      font-size: 12px;
      color: #e6a23c;
      white-space: nowrap;
    }
  }

  .no-image {
    color: #c0c4cc;
    font-size: 13px;

    &.warning {
      color: #e6a23c;
    }
  }
}
</style>
