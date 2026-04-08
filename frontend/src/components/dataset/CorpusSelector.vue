<template>
  <div class="corpus-selector">
    <!-- 选择模式切换 -->
    <div class="mode-selector">
      <el-radio-group v-model="selectionMode" @change="handleModeChange">
        <el-radio-button label="sentence">
          <el-icon><List /></el-icon>
          句子级选择
        </el-radio-button>
        <el-radio-button label="file">
          <el-icon><FolderOpened /></el-icon>
          按文件选择
        </el-radio-button>
        <el-radio-button label="row">
          <el-icon><Document /></el-icon>
          按行选择
        </el-radio-button>
      </el-radio-group>

      <!-- 通用筛选：是否包含图片 -->
      <el-checkbox v-model="showOnlyWithImages" @change="handleImageFilterChange('with')" style="margin-left: 16px">
        <el-icon><Picture /></el-icon>
        仅显示含图片
      </el-checkbox>
      <el-checkbox v-model="showOnlyWithoutImages" @change="handleImageFilterChange('without')" style="margin-left: 8px">
        仅显示非图片
      </el-checkbox>

      <el-button
        size="small"
        :icon="CloseBold"
        @click="handleClearSelection"
        style="margin-left: auto"
      >
        清空选择
      </el-button>
    </div>

    <!-- 句子级选择模式的筛选工具栏 -->
    <div v-if="selectionMode === 'sentence'" class="filter-toolbar">
      <el-input
        v-model="searchFileName"
        placeholder="按文件名搜索"
        clearable
        style="width: 200px"
        @change="handleFilterChange"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="selectedType"
        placeholder="按字段分类筛选"
        clearable
        style="width: 180px"
        @change="handleFilterChange"
      >
        <el-option label="全部" value="" />
        <el-option label="问题描述" value="问题描述" />
        <el-option label="原因分析" value="原因分析" />
        <el-option label="采取措施" value="采取措施" />
        <el-option label="问题处理" value="问题处理" />
        <el-option label="质量问题" value="质量问题" />
      </el-select>

      <el-input-number
        v-model="rowStart"
        placeholder="起始行"
        :min="1"
        :controls="false"
        style="width: 100px"
        @change="handleFilterChange"
      />
      <span style="margin: 0 4px">-</span>
      <el-input-number
        v-model="rowEnd"
        placeholder="结束行"
        :min="rowStart || 1"
        :controls="false"
        style="width: 100px"
        @change="handleFilterChange"
      />

      <el-button
        size="small"
        :icon="Select"
        @click="handleSelectAll"
      >
        全选当前页
      </el-button>
    </div>

    <!-- 内容区域 -->
    <div v-loading="loading" class="content-area">
      <!-- 模式1: 句子级列表 -->
      <div v-if="selectionMode === 'sentence'" class="corpus-table">
        <el-table
          ref="tableRef"
          :data="corpusList"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="text_id" label="ID" width="150" show-overflow-tooltip />
          <el-table-column prop="text_type" label="字段分类" width="120">
            <template #default="{ row }">
              <el-tag size="small" type="info">{{ row.text_type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="text" label="内容" min-width="300" show-overflow-tooltip />
          <el-table-column prop="source_file" label="来源文件" width="180" show-overflow-tooltip />
          <el-table-column prop="source_row" label="行号" width="80" align="center" />
          <el-table-column label="图片" width="80" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.has_images" size="small" type="warning">
                <el-icon><Picture /></el-icon>
                {{ row.images?.length || 0 }}
              </el-tag>
              <span v-else class="no-image">-</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 模式2: 按文件选择 -->
      <div v-else-if="selectionMode === 'file'" class="file-selector">
        <el-empty v-if="fileGroups.length === 0" description="暂无文件" />
        <div v-else class="file-list">
          <div
            v-for="file in fileGroups"
            :key="file.name"
            class="file-item"
            :class="{ selected: isFileSelected(file.name) }"
            @click="handleSelectFile(file.name)"
          >
            <el-checkbox :model-value="isFileSelected(file.name)" @click.stop />
            <el-icon class="file-icon"><Document /></el-icon>
            <div class="file-info">
              <span class="file-name">{{ file.name }}</span>
              <span class="file-stats">
                <el-tag size="small" type="info">{{ file.count }} 条语料</el-tag>
                <el-tag v-if="file.imageCount > 0" size="small" type="warning">
                  <el-icon><Picture /></el-icon>
                  {{ file.imageCount }} 张图片
                </el-tag>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 模式3: 按行选择 -->
      <div v-else-if="selectionMode === 'row'" class="row-selector">
        <el-empty v-if="rowGroups.length === 0" description="暂无数据" />
        <div v-else class="row-list">
          <div
            v-for="row in rowGroups"
            :key="`${row.file}|||${row.row}`"
            class="row-item"
            :class="{ selected: isRowSelected(row.file, row.row) }"
            @click="handleSelectRow(row.file, row.row)"
          >
            <el-checkbox :model-value="isRowSelected(row.file, row.row)" @click.stop />
            <div class="row-info">
              <div class="row-header">
                <span class="row-title">{{ row.file }} - 第 {{ row.row }} 行</span>
                <span class="row-stats">
                  <el-tag size="small" type="info">{{ row.count }} 个字段</el-tag>
                  <el-tag v-if="row.imageCount > 0" size="small" type="warning">
                    <el-icon><Picture /></el-icon>
                    {{ row.imageCount }} 张图片
                  </el-tag>
                </span>
              </div>
              <div class="row-preview">
                <el-tag
                  v-for="field in row.fields"
                  :key="field.text_id"
                  size="small"
                  type="info"
                  style="margin-right: 8px"
                >
                  {{ field.text_type }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页（仅在句子级选择模式显示） -->
    <div v-if="selectionMode === 'sentence'" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 文件/行模式的数据提示 -->
    <div v-else class="mode-info">
      <el-alert
        type="info"
        :closable="false"
        show-icon
      >
        <template #title>
          <span v-if="selectionMode === 'file'">
            当前显示 {{ fileGroups.length }} 个文件，共 {{ total }} 条语料
          </span>
          <span v-else-if="selectionMode === 'row'">
            当前显示 {{ rowGroups.length }} 行，共 {{ total }} 条语料
          </span>
        </template>
      </el-alert>
    </div>

    <!-- 已选择统计 -->
    <div class="selection-summary">
      <div class="summary-title">
        <el-icon><Select /></el-icon>
        已选择 {{ selectedIds.length }} 条语料
      </div>
      <div v-if="selectedIds.length > 0" class="summary-details">
        <div class="detail-item">
          <span class="label">按文件:</span>
          <el-tag
            v-for="(count, file) in selectedByFile"
            :key="file"
            size="small"
            style="margin-right: 8px"
          >
            {{ file }}: {{ count }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">按分类:</span>
          <el-tag
            v-for="(count, type) in selectedByType"
            :key="type"
            size="small"
            type="info"
            style="margin-right: 8px"
          >
            {{ type }}: {{ count }}
          </el-tag>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Search,
  FolderOpened,
  List,
  Select,
  CloseBold,
  Document,
  Picture
} from '@element-plus/icons-vue'
import { useCorpusStore } from '@/stores'
import type { Corpus } from '@/types'
import type { ElTable } from 'element-plus'

const corpusStore = useCorpusStore()

// 选择模式
type SelectionMode = 'sentence' | 'file' | 'row'
const selectionMode = ref<SelectionMode>('sentence')

// 状态
const searchFileName = ref('')
const selectedType = ref('')
const rowStart = ref<number>()
const rowEnd = ref<number>()
const showOnlyWithImages = ref(false)
const showOnlyWithoutImages = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedIds = ref<string[]>([])
const tableRef = ref<InstanceType<typeof ElTable>>()

// 计算属性
const loading = computed(() => corpusStore.loading)
const corpusList = computed(() => corpusStore.corpusList)
const total = computed(() => corpusStore.total)

// 文件分组（增强版，包含图片统计）
const fileGroups = computed(() => {
  const groups = new Map<string, { count: number; imageCount: number }>()
  corpusList.value.forEach(corpus => {
    const existing = groups.get(corpus.source_file) || { count: 0, imageCount: 0 }
    groups.set(corpus.source_file, {
      count: existing.count + 1,
      imageCount: existing.imageCount + (corpus.images?.length || 0)
    })
  })
  return Array.from(groups.entries()).map(([name, stats]) => ({ 
    name, 
    count: stats.count,
    imageCount: stats.imageCount
  }))
})

// 行分组（增强版，包含字段预览和图片统计）
const rowGroups = computed(() => {
  const groups = new Map<string, { count: number; imageCount: number; fields: Corpus[] }>()
  corpusList.value.forEach(corpus => {
    // 使用特殊分隔符避免文件名中的 - 干扰
    const key = `${corpus.source_file}|||${corpus.source_row}`
    const existing = groups.get(key) || { count: 0, imageCount: 0, fields: [] }
    groups.set(key, {
      count: existing.count + 1,
      imageCount: existing.imageCount + (corpus.images?.length || 0),
      fields: [...existing.fields, corpus]
    })
  })
  return Array.from(groups.entries()).map(([key, stats]) => {
    const [file, row] = key.split('|||')
    return { 
      file, 
      row: parseInt(row), 
      count: stats.count,
      imageCount: stats.imageCount,
      fields: stats.fields
    }
  })
})

// 全局统计：基于所有已选择的ID（不仅仅是当前页）
// 需要从后端获取完整的语料信息来统计
const allSelectedCorpus = ref<Corpus[]>([])

// 按文件统计选择（基于全局）
const selectedByFile = computed(() => {
  const stats: Record<string, number> = {}
  
  // 统计当前页的
  corpusList.value.forEach(corpus => {
    if (selectedIds.value.includes(corpus.text_id)) {
      stats[corpus.source_file] = (stats[corpus.source_file] || 0) + 1
    }
  })
  
  // 统计已缓存的其他页的
  allSelectedCorpus.value.forEach(corpus => {
    if (selectedIds.value.includes(corpus.text_id) && 
        !corpusList.value.find(c => c.text_id === corpus.text_id)) {
      stats[corpus.source_file] = (stats[corpus.source_file] || 0) + 1
    }
  })
  
  return stats
})

// 按分类统计选择（基于全局）
const selectedByType = computed(() => {
  const stats: Record<string, number> = {}
  
  // 统计当前页的
  corpusList.value.forEach(corpus => {
    if (selectedIds.value.includes(corpus.text_id)) {
      stats[corpus.text_type] = (stats[corpus.text_type] || 0) + 1
    }
  })
  
  // 统计已缓存的其他页的
  allSelectedCorpus.value.forEach(corpus => {
    if (selectedIds.value.includes(corpus.text_id) && 
        !corpusList.value.find(c => c.text_id === corpus.text_id)) {
      stats[corpus.text_type] = (stats[corpus.text_type] || 0) + 1
    }
  })
  
  return stats
})

// 方法
const fetchList = async () => {
  // 在文件/行选择模式下，使用更大的页面大小以获取更多数据
  const effectivePageSize = (selectionMode.value === 'file' || selectionMode.value === 'row') 
    ? 1000  // 使用后端允许的最大值（已提高到1000）
    : pageSize.value

  await corpusStore.fetchList({
    page: currentPage.value,
    page_size: effectivePageSize,
    source_file: searchFileName.value || undefined,
    source_field: selectedType.value || undefined,
    has_images: showOnlyWithImages.value ? true : (showOnlyWithoutImages.value ? false : undefined)
  })
}

const handleModeChange = () => {
  // 切换模式时重置筛选条件（保留"是否包含图片"）
  searchFileName.value = ''
  selectedType.value = ''
  rowStart.value = undefined
  rowEnd.value = undefined
  currentPage.value = 1
  
  // 切换到文件/行模式时，加载更多数据
  fetchList()
}

const handleImageFilterChange = (which: 'with' | 'without') => {
  // 两个图片筛选互斥
  if (which === 'with' && showOnlyWithImages.value) {
    showOnlyWithoutImages.value = false
  } else if (which === 'without' && showOnlyWithoutImages.value) {
    showOnlyWithImages.value = false
  }
  // 切换图片筛选时重置选择状态（清除上次选择的语料）
  handleClearSelection()
  currentPage.value = 1
  fetchList()
}

const handleFilterChange = () => {
  // 文件名搜索或字段分类筛选的变更需要重置选择，避免保留其他页数据的历史选择
  handleClearSelection()
  currentPage.value = 1
  fetchList()
}

const handlePageChange = () => {
  fetchList()
}

const handleSelectionChange = (selection: Corpus[]) => {
  // 更新选中的ID列表（仅在句子级选择模式）
  const currentPageIds = corpusList.value.map(c => c.text_id)
  // 移除当前页的所有ID
  selectedIds.value = selectedIds.value.filter(id => !currentPageIds.includes(id))
  // 添加新选中的ID
  selectedIds.value.push(...selection.map(c => c.text_id))
  
  // 缓存选中的语料信息（用于统计）
  updateSelectedCorpusCache(selection)
}

const handleSelectAll = () => {
  if (!tableRef.value) return
  tableRef.value.toggleAllSelection()
}

const handleClearSelection = () => {
  selectedIds.value = []
  allSelectedCorpus.value = []
  if (tableRef.value) {
    tableRef.value.clearSelection()
  }
}

const isFileSelected = (fileName: string) => {
  const fileCorpus = corpusList.value.filter(c => c.source_file === fileName)
  if (fileCorpus.length === 0) return false
  return fileCorpus.every(c => selectedIds.value.includes(c.text_id))
}

const handleSelectFile = (fileName: string) => {
  const fileCorpus = corpusList.value.filter(c => c.source_file === fileName)
  const fileTextIds = fileCorpus.map(c => c.text_id)
  
  if (isFileSelected(fileName)) {
    // 取消选择
    selectedIds.value = selectedIds.value.filter(id => !fileTextIds.includes(id))
    // 从缓存中移除
    allSelectedCorpus.value = allSelectedCorpus.value.filter(c => !fileTextIds.includes(c.text_id))
  } else {
    // 选择
    selectedIds.value = [...new Set([...selectedIds.value, ...fileTextIds])]
    // 添加到缓存
    updateSelectedCorpusCache(fileCorpus)
  }
}

const isRowSelected = (fileName: string, row: number) => {
  const rowCorpus = corpusList.value.filter(
    c => c.source_file === fileName && c.source_row === row
  )
  if (rowCorpus.length === 0) return false
  return rowCorpus.every(c => selectedIds.value.includes(c.text_id))
}

const handleSelectRow = (fileName: string, row: number) => {
  const rowCorpus = corpusList.value.filter(
    c => c.source_file === fileName && c.source_row === row
  )
  const rowTextIds = rowCorpus.map(c => c.text_id)
  
  if (isRowSelected(fileName, row)) {
    // 取消选择
    selectedIds.value = selectedIds.value.filter(id => !rowTextIds.includes(id))
    // 从缓存中移除
    allSelectedCorpus.value = allSelectedCorpus.value.filter(c => !rowTextIds.includes(c.text_id))
  } else {
    // 选择
    selectedIds.value = [...new Set([...selectedIds.value, ...rowTextIds])]
    // 添加到缓存
    updateSelectedCorpusCache(rowCorpus)
  }
}

// 更新选中语料的缓存
const updateSelectedCorpusCache = (newSelection: Corpus[]) => {
  newSelection.forEach(corpus => {
    // 如果不在缓存中，添加进去
    if (!allSelectedCorpus.value.find(c => c.text_id === corpus.text_id)) {
      allSelectedCorpus.value.push(corpus)
    }
  })
  
  // 清理缓存：移除未选中的
  allSelectedCorpus.value = allSelectedCorpus.value.filter(c => 
    selectedIds.value.includes(c.text_id)
  )
}

const updateTableSelection = () => {
  if (!tableRef.value || selectionMode.value !== 'sentence') return
  
  corpusList.value.forEach(corpus => {
    const isSelected = selectedIds.value.includes(corpus.text_id)
    tableRef.value!.toggleRowSelection(corpus, isSelected)
  })
}

// 监听语料列表变化，更新表格选择状态
watch(corpusList, () => {
  updateTableSelection()
}, { immediate: true })

// 生命周期
onMounted(() => {
  fetchList()
})

// 暴露方法供父组件调用
defineExpose({
  getSelectedIds: () => selectedIds.value,
  getSelectedCorpus: () => {
    // 返回选中的完整 Corpus 对象
    // 从当前页和缓存中获取
    const selected: Corpus[] = []
    
    // 从当前页获取
    corpusList.value.forEach(corpus => {
      if (selectedIds.value.includes(corpus.text_id)) {
        selected.push(corpus)
      }
    })
    
    // 从缓存获取（其他页的）
    allSelectedCorpus.value.forEach(corpus => {
      if (selectedIds.value.includes(corpus.text_id) && 
          !selected.find(c => c.text_id === corpus.text_id)) {
        selected.push(corpus)
      }
    })
    
    return selected
  },
  clearSelection: handleClearSelection
})
</script>

<style scoped lang="scss">
.corpus-selector {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .mode-selector {
    display: flex;
    align-items: center;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 8px;
    gap: 16px;
  }

  .filter-toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    padding: 12px;
    background: #fff;
    border: 1px solid #ebeef5;
    border-radius: 8px;
  }

  .content-area {
    min-height: 400px;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    background: #fff;

    .corpus-table {
      .no-image {
        color: #c0c4cc;
      }
    }

    .file-selector,
    .row-selector {
      padding: 16px;

      .file-list,
      .row-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
        max-height: 500px;
        overflow-y: auto;
      }

      .file-item,
      .row-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px;
        background: #f5f7fa;
        border: 2px solid transparent;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;

        &:hover {
          background: #ecf5ff;
          border-color: #b3d8ff;
        }

        &.selected {
          background: #ecf5ff;
          border-color: #409eff;
        }

        .file-icon {
          font-size: 24px;
          color: #409eff;
        }

        .file-info,
        .row-info {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 8px;

          .file-name,
          .row-title {
            font-size: 14px;
            font-weight: 600;
            color: #303133;
          }

          .file-stats,
          .row-stats {
            display: flex;
            gap: 8px;
          }

          .row-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
          }

          .row-preview {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
          }
        }
      }
    }
  }

  .pagination {
    display: flex;
    justify-content: center;
    padding: 16px;
    background: #fff;
    border: 1px solid #ebeef5;
    border-radius: 8px;
  }

  .mode-info {
    padding: 16px;
    background: #fff;
    border: 1px solid #ebeef5;
    border-radius: 8px;
  }

  .selection-summary {
    padding: 16px;
    background: #f0f9ff;
    border: 1px solid #b3d8ff;
    border-radius: 8px;

    .summary-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 16px;
      font-weight: 600;
      color: #409eff;
      margin-bottom: 12px;
    }

    .summary-details {
      display: flex;
      flex-direction: column;
      gap: 8px;

      .detail-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        flex-wrap: wrap;

        .label {
          color: #606266;
          font-weight: 500;
          min-width: 60px;
        }
      }
    }
  }
}
</style>
