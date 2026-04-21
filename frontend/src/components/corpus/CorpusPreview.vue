<template>
  <div class="corpus-preview">
    <!-- 筛选工具栏 -->
    <div class="filter-toolbar">
      <el-input
        v-model="searchFileName"
        placeholder="按文件名搜索"
        clearable
        style="width: 250px"
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
        style="width: 200px"
        @change="handleFilterChange"
      >
        <el-option label="全部" value="" />
        <el-option label="问题描述" value="问题描述" />
        <el-option label="原因分析" value="原因分析" />
        <el-option label="采取措施" value="采取措施" />
      </el-select>

      <el-checkbox v-model="showOnlyWithImages" @change="handleFilterChange">
        仅显示包含图片的语料
      </el-checkbox>

      <div class="stats">
        <span>共 {{ total }} 条语料</span>
        <span v-if="filteredCount !== total">（筛选后 {{ filteredCount }} 条）</span>
      </div>
    </div>

    <!-- 语料列表 -->
    <div v-loading="loading" class="corpus-list">
      <el-empty v-if="!loading && list.length === 0" description="暂无语料数据" />

      <div
        v-for="item in list"
        :key="item.text_id"
        class="corpus-item"
      >
        <div class="corpus-header">
          <div class="corpus-id">
            <el-tag size="small">{{ item.text_id }}</el-tag>
            <el-tag v-if="item.text_type" type="info" size="small">
              {{ item.text_type }}
            </el-tag>
          </div>
          <div class="corpus-meta">
            <span class="meta-item">
              <el-icon><Document /></el-icon>
              {{ item.source_file }}
            </span>
            <span class="meta-item">
              第 {{ item.source_row }} 行
            </span>
            <span v-if="item.has_images" class="meta-item">
              <el-icon><Picture /></el-icon>
              {{ item.images?.length || 0 }} 张图片
            </span>
          </div>
        </div>

        <div class="corpus-content">
          <p class="corpus-text">{{ item.text }}</p>
        </div>

        <!-- 图片缩略图 -->
        <div v-if="item.has_images && item.images && item.images.length > 0" class="corpus-images">
          <div
            v-for="image in item.images"
            :key="image.image_id"
            class="image-thumbnail"
            @click="handlePreviewImage(image)"
          >
            <el-image
              :src="getImageUrl(image.file_path)"
              :alt="image.original_name"
              fit="cover"
              lazy
            >
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                  <span>加载失败</span>
                </div>
              </template>
            </el-image>
            <div class="image-name">{{ image.original_name }}</div>
          </div>
        </div>

        <div class="corpus-actions">
          <el-button size="small" @click="handleView(item)">
            查看详情
          </el-button>
          <el-button
            size="small"
            type="danger"
            plain
            @click="handleDelete(item)"
          >
            删除
          </el-button>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 图片预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="图片预览"
      width="800px"
    >
      <el-image
        v-if="previewImage"
        :src="getImageUrl(previewImage.file_path)"
        :alt="previewImage.original_name"
        fit="contain"
        style="width: 100%"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Picture, Search } from '@element-plus/icons-vue'
import { useCorpusStore } from '@/stores'
import type { Corpus, Image } from '@/types'
import { buildBackendUrl } from '@/utils/backendUrl'

const corpusStore = useCorpusStore()

const getImageUrl = (filePath: string) => buildBackendUrl(`/images/${filePath}`)

const searchFileName = ref('')
const selectedType = ref('')
const showOnlyWithImages = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const previewVisible = ref(false)
const previewImage = ref<Image | null>(null)

const loading = computed(() => corpusStore.loading)
const list = computed(() => corpusStore.corpusList)
const total = computed(() => corpusStore.total)
const filteredCount = computed(() => list.value.length)

const fetchList = async () => {
  await corpusStore.fetchList({
    page: currentPage.value,
    page_size: pageSize.value,
    source_file: searchFileName.value || undefined,
    text_type: selectedType.value || undefined,
    has_images: showOnlyWithImages.value || undefined
  })
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchList()
}

const handlePageChange = () => {
  fetchList()
}

const handleView = (item: Corpus) => {
  console.log('查看详情:', item)
}

const handleDelete = async (item: Corpus) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除语料 ${item.text_id} 吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await corpusStore.deleteCorpus(item.text_id)
    ElMessage.success('删除成功')

    if (list.value.length === 0 && currentPage.value > 1) {
      currentPage.value--
    }

    fetchList()
  } catch (error: any) {
    if (error !== 'cancel') {
      const msg = error?.response?.data?.detail || '删除失败'
      ElMessage.warning(msg)
    }
  }
}

const handlePreviewImage = (image: Image) => {
  previewImage.value = image
  previewVisible.value = true
}

onMounted(() => {
  fetchList()
})

defineExpose({
  refresh: fetchList
})
</script>

<style scoped lang="scss">
.corpus-preview {
  .filter-toolbar {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 8px;

    .stats {
      margin-left: auto;
      font-size: 14px;
      color: #606266;

      span + span {
        margin-left: 8px;
        color: #909399;
      }
    }
  }

  .corpus-list {
    min-height: 400px;

    .corpus-item {
      margin-bottom: 16px;
      padding: 16px;
      background: #fff;
      border: 1px solid #e4e7ed;
      border-radius: 8px;
      transition: all 0.3s;

      &:hover {
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
      }

      .corpus-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;

        .corpus-id {
          display: flex;
          gap: 8px;
        }

        .corpus-meta {
          display: flex;
          gap: 16px;
          font-size: 13px;
          color: #909399;

          .meta-item {
            display: flex;
            align-items: center;
            gap: 4px;
          }
        }
      }

      .corpus-content {
        margin-bottom: 12px;

        .corpus-text {
          margin: 0;
          font-size: 14px;
          line-height: 1.6;
          color: #303133;
        }
      }

      .corpus-images {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
        flex-wrap: wrap;

        .image-thumbnail {
          width: 120px;
          cursor: pointer;
          transition: all 0.3s;

          &:hover {
            transform: scale(1.05);
          }

          .el-image {
            width: 120px;
            height: 120px;
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid #e4e7ed;
          }

          .image-error {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #c0c4cc;

            .el-icon {
              font-size: 32px;
              margin-bottom: 8px;
            }

            span {
              font-size: 12px;
            }
          }

          .image-name {
            margin-top: 4px;
            font-size: 12px;
            color: #909399;
            text-align: center;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }
        }
      }

      .corpus-actions {
        display: flex;
        gap: 8px;
        justify-content: flex-end;
      }
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}
</style>
