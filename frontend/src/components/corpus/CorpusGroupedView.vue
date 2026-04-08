<template>
  <div class="corpus-grouped-view">
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


      <el-checkbox v-model="showOnlyWithImages" :disabled="showOnlyWithoutImages" @change="onShowWithImagesChange">
        仅显示包含图片的语料
      </el-checkbox>
      <el-checkbox v-model="showOnlyWithoutImages" :disabled="showOnlyWithImages" @change="onShowWithoutImagesChange">
        仅显示不包含图片的语料
      </el-checkbox>

      <div class="stats">
        <span>共 {{ total }} 行数据</span>
      </div>
    </div>

    <!-- 分组列表 -->
    <div v-loading="loading" class="grouped-list">
      <el-empty v-if="!loading && list.length === 0" description="暂无语料数据" />
      
      <!-- 每一行Excel数据作为一个卡片 -->
      <el-card
        v-for="row in list"
        :key="`${row.source_file}-${row.source_row}`"
        class="row-card"
        shadow="hover"
      >
        <!-- 卡片头部：文件信息 -->
        <template #header>
          <div class="card-header">
            <div class="file-info">
              <el-icon><Document /></el-icon>
              <span class="file-name">{{ row.source_file }}</span>
              <el-tag size="small" type="info">第 {{ row.source_row }} 行</el-tag>
              <el-tag v-if="row.total_images > 0" size="small" type="warning">
                <el-icon><Picture /></el-icon>
                {{ row.total_images }} 张图片
              </el-tag>
            </div>
            <div class="card-actions">
              <el-button size="small" @click="handleViewRow(row)">
                查看详情
              </el-button>
              <el-button
                size="small"
                type="danger"
                plain
                :loading="deletingKey === `${row.source_file}-${row.source_row}-row`"
                @click="handleDeleteRow(row)"
              >
                删除本行
              </el-button>
              <el-button
                size="small"
                type="danger"
                :loading="deletingKey === `${row.source_file}-file`"
                @click="handleDeleteFile(row)"
              >
                删除该文件
              </el-button>
            </div>
          </div>
        </template>

        <!-- 卡片内容：各字段内容 -->
        <div class="row-content">
          <div
            v-for="item in row.items"
            :key="item.text_id"
            class="field-item"
          >
            <div class="field-header">
              <el-tag size="small">{{ item.source_field }}</el-tag>
              <span class="text-id">{{ item.text_id }}</span>
            </div>
            <div class="field-text">{{ item.text }}</div>
            
            <!-- 该字段的图片 -->
            <div v-if="item.images && item.images.length > 0" class="field-images">
              <div
                v-for="image in item.images"
                :key="image.image_id"
                class="image-thumbnail"
                @click="handlePreviewImage(image)"
              >
                <el-image
                  :src="`${apiBaseUrl}/images/${image.file_path}`"
                  :alt="image.original_name"
                  fit="cover"
                  lazy
                >
                  <template #error>
                    <div class="image-error">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
              </div>
            </div>
          </div>
        </div>
      </el-card>
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
        :src="`${apiBaseUrl}/images/${previewImage.file_path}`"
        :alt="previewImage.original_name"
        fit="contain"
        style="width: 100%"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Picture, Search } from '@element-plus/icons-vue'
import { request } from '@/api/request'
import type { Image } from '@/types'

// API基础URL
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '')

// 类型定义
interface GroupedCorpusItem {
  text_id: string
  text: string
  text_type: string
  source_field: string
  has_images: boolean
  images: Image[]
}

interface GroupedCorpusRow {
  source_file: string
  source_row: number
  items: GroupedCorpusItem[]
  total_images: number
  created_at: string
}

// 状态
const loading = ref(false)
const list = ref<GroupedCorpusRow[]>([])
const total = ref(0)
const searchFileName = ref('')
const selectedType = ref('')
const showOnlyWithImages = ref(false)
const showOnlyWithoutImages = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const previewVisible = ref(false)
const previewImage = ref<Image | null>(null)
const deletingKey = ref<string | null>(null)

// 方法
const fetchList = async () => {
  loading.value = true
  try {
    const response = await request.get<{
      total: number
      items: GroupedCorpusRow[]
    }>('/corpus/grouped', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        source_file: searchFileName.value || undefined,
        source_field: selectedType.value || undefined,
        has_images: showOnlyWithImages.value ? true : (showOnlyWithoutImages.value ? false : undefined)
      }
    })
    list.value = response.items
    total.value = response.total
  } catch (error: any) {
    ElMessage.error(error.message || '获取数据失败')
  } finally {
    loading.value = false
  }
}


const handleFilterChange = () => {
  currentPage.value = 1
  fetchList()
}

const onShowWithImagesChange = () => {
  if (showOnlyWithImages.value) showOnlyWithoutImages.value = false
  handleFilterChange()
}
const onShowWithoutImagesChange = () => {
  if (showOnlyWithoutImages.value) showOnlyWithImages.value = false
  handleFilterChange()
}

const handlePageChange = () => {
  fetchList()
}

const handleViewRow = (row: GroupedCorpusRow) => {
  console.log('查看行详情:', row)
  // TODO: 实现详情查看
}

const handleDeleteRow = async (row: GroupedCorpusRow) => {
  try {
    await ElMessageBox.confirm(
      `确认删除文件「${row.source_file}」第 ${row.source_row} 行的所有语料？已被数据集引用的语料会被跳过并提示。`,
      '删除确认',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )
  } catch {
    return
  }

  const key = `${row.source_file}-${row.source_row}-row`
  deletingKey.value = key
  try {
    const res = await request.delete<{
      success: boolean
      message: string
      data?: { deleted: number; skipped: number; skipped_text_ids?: string[] }
    }>('/corpus/by-row', {
      params: { source_file: row.source_file, source_row: row.source_row }
    })
    ElMessage.success(res.message || '删除成功')
    fetchList()
  } catch (error: any) {
    const msg = error?.response?.data?.detail || '删除失败'
    // 提示但降低警示级别
    ElMessage.warning(msg)
  } finally {
    deletingKey.value = null
  }
}

const handleDeleteFile = async (row: GroupedCorpusRow) => {
  try {
    await ElMessageBox.confirm(
      `确认删除文件「${row.source_file}」下的所有语料？已被数据集引用的语料会被跳过并提示。`,
      '删除确认',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )
  } catch {
    return
  }

  const key = `${row.source_file}-file`
  deletingKey.value = key
  try {
    const res = await request.delete<{
      success: boolean
      message: string
      data?: { deleted: number; skipped: number; skipped_text_ids?: string[] }
    }>('/corpus/by-file', { params: { source_file: row.source_file } })
    ElMessage.success(res.message || '删除成功')
    fetchList()
  } catch (error: any) {
    const msg = error?.response?.data?.detail || '删除失败'
    ElMessage.warning(msg)
  } finally {
    deletingKey.value = null
  }
}

const handlePreviewImage = (image: Image) => {
  previewImage.value = image
  previewVisible.value = true
}

// 生命周期
onMounted(() => {
  fetchList()
})

// 暴露方法供父组件调用
defineExpose({
  refresh: fetchList
})
</script>

<style scoped lang="scss">
.corpus-grouped-view {
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
    }
  }

  .grouped-list {
    min-height: 400px;

    .row-card {
      margin-bottom: 20px;

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        .file-info {
          display: flex;
          align-items: center;
          gap: 12px;
          flex: 1;

          .el-icon {
            font-size: 18px;
            color: #409eff;
          }

          .file-name {
            font-weight: 600;
            color: #303133;
          }
        }

        .card-actions {
          display: flex;
          gap: 8px;
        }
      }

      .row-content {
        display: flex;
        flex-direction: column;
        gap: 16px;

        .field-item {
          padding: 12px;
          background: #f9fafc;
          border-radius: 6px;
          border-left: 3px solid #409eff;

          .field-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;

            .text-id {
              font-size: 12px;
              color: #909399;
            }
          }

          .field-text {
            font-size: 14px;
            line-height: 1.6;
            color: #303133;
            margin-bottom: 8px;
          }

          .field-images {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;

            .image-thumbnail {
              width: 100px;
              height: 100px;
              cursor: pointer;
              transition: all 0.3s;

              &:hover {
                transform: scale(1.05);
              }

              .el-image {
                width: 100%;
                height: 100%;
                border-radius: 4px;
                overflow: hidden;
                border: 1px solid #e4e7ed;
              }

              .image-error {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100%;
                color: #c0c4cc;

                .el-icon {
                  font-size: 24px;
                }
              }
            }
          }
        }
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
