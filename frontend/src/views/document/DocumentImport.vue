<template>
  <div class="document-import">
    <div class="page-header">
      <div class="header-left">
        <h2>文档导入</h2>
        <p class="page-desc">上传 Excel 文件并导入 KF、QMS、品质失效案例数据。</p>
      </div>
    </div>

    <el-card class="processor-card" shadow="never">
      <el-radio-group v-model="currentProcessor" @change="handleProcessorChange">
        <el-radio-button
          v-for="processor in processorTabs"
          :key="processor.name"
          :value="processor.name"
        >
          {{ processor.display_name }}
        </el-radio-button>
      </el-radio-group>
    </el-card>

    <el-card class="format-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>{{ currentFormatTip.title }}</span>
        </div>
      </template>

      <el-alert
        type="info"
        :closable="false"
        :description="currentFormatTip.description"
      />

      <div class="format-fields">
        <div class="format-label">必填字段：</div>
        <el-tag
          v-for="field in currentFormatTip.requiredFields"
          :key="field"
          class="field-tag"
          effect="plain"
          type="primary"
        >
          {{ field }}
        </el-tag>
      </div>

      <div v-if="currentFormatTip.aliasTip" class="alias-tip">
        <el-text type="warning">{{ currentFormatTip.aliasTip }}</el-text>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="upload-card">
          <template #header>
            <div class="card-header">
              <span>上传 Excel 文件</span>
            </div>
          </template>

          <el-upload
            ref="uploadRef"
            class="excel-uploader"
            :auto-upload="false"
            :limit="1"
            accept=".xlsx,.xls"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
          >
            <el-button type="primary">选择 Excel 文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 `.xlsx`、`.xls` 格式</div>
            </template>
          </el-upload>

          <el-button
            type="success"
            class="upload-btn"
            :loading="store.isUploading"
            :disabled="!selectedFile"
            @click="handleUpload"
          >
            上传并处理
          </el-button>

          <div v-if="excelProgressVisible" class="transfer-progress">
            <el-progress
              :percentage="store.excelUploadProgress.percentage"
              :status="excelProgressStatus"
              :stroke-width="8"
              :show-text="false"
            />
            <p class="progress-text">{{ excelProgressText }}</p>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="files-card">
          <template #header>
            <div class="card-header">
              <span>已处理文件</span>
              <el-button
                type="default"
                :icon="Refresh"
                @click="handleRefreshFiles"
              >
                刷新
              </el-button>
            </div>
          </template>

          <el-table
            :data="store.processedFiles"
            v-loading="store.loading"
            stripe
            style="width: 100%"
          >
            <el-table-column prop="filename" label="文件名" min-width="160" show-overflow-tooltip />
            <el-table-column prop="data_source" label="数据源" width="120" show-overflow-tooltip />
            <el-table-column prop="table_count" label="表格数" width="80" align="center" />
            <el-table-column prop="processed_time" label="处理时间" width="160" show-overflow-tooltip />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  size="small"
                  @click="handleImport(row)"
                >
                  导入图谱数据库
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click="handleDelete(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-empty
            v-if="!store.loading && store.processedFiles.length === 0"
            description="暂无已处理文件"
          />
        </el-card>
      </el-col>
    </el-row>

    <el-card v-if="currentProcessor === 'qms'" class="images-card">
      <template #header>
        <div class="card-header">
          <span>图片上传</span>
        </div>
      </template>

      <el-alert
        type="info"
        :closable="false"
        description="QMS Excel 中的图片按文件名外链引用，需要单独上传 ZIP 压缩包。数据源标识必须与 Excel 文件名规范化后的数据源完全一致，导出时才能正确匹配图片。"
        style="margin-bottom: 12px"
      />

      <el-space wrap>
        <el-input
          v-model="imageDataSource"
          placeholder="请输入数据源标识"
          style="width: 220px"
        />
        <el-upload
          ref="imageUploadRef"
          class="image-uploader"
          :auto-upload="false"
          :limit="1"
          accept=".zip"
          :on-change="handleImageFileChange"
          :on-remove="handleImageFileRemove"
        >
          <el-button>选择 ZIP 文件</el-button>
          <template #tip>
            <span class="el-upload__tip">上传图片压缩包（`.zip`）</span>
          </template>
        </el-upload>
        <el-button
          type="warning"
          :disabled="!selectedImageFile || !imageDataSource"
          :loading="store.isImageUploading"
          @click="handleImageUpload"
        >
          上传图片
        </el-button>
        <el-button
          :disabled="!imageDataSource"
          :icon="Refresh"
          @click="handleQueryImages"
        >
          查询图片
        </el-button>
      </el-space>

      <div v-if="imageProgressVisible" class="transfer-progress">
        <el-progress
          :percentage="store.imageUploadProgress.percentage"
          :status="imageProgressStatus"
          :stroke-width="8"
          :show-text="false"
        />
        <p class="progress-text">{{ imageProgressText }}</p>
      </div>

      <div v-if="imageUploadStatus" class="status-alert">
        <el-alert
          :type="imageUploadStatus.type"
          :title="imageUploadStatus.message"
          :closable="false"
          show-icon
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { useDocumentStore } from '@/stores/document'
import { documentApi } from '@/api/document'
import type { UploadFile } from 'element-plus'

const store = useDocumentStore()
const router = useRouter()

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
  set: (value: string) => store.setCurrentProcessor(value)
})

interface FormatTip {
  title: string
  description: string
  requiredFields: string[]
  aliasTip?: string
}

const formatTips: Record<string, FormatTip> = {
  kf: {
    title: 'KF 快反文件格式要求',
    description: '请上传快反问题记录 Excel，字段名需与系统要求一致。',
    requiredFields: [
      '快反编号',
      '发生时间',
      '问题原因及分析',
      '问题图片',
      '短期改善措施',
      '长期改善措施',
      '所属分类',
      '客户名称',
      '产品型号',
      '缺陷类型不良现象'
    ],
    aliasTip: '兼容常见旧字段别名，例如：短期措施 -> 短期改善措施，长期措施 -> 长期改善措施，问题描述 -> 问题原因及分析。'
  },
  qms: {
    title: 'QMS 不合格品文件格式要求',
    description: '请上传 QMS 不合格品 Excel，需包含完整的质量追溯字段。',
    requiredFields: [
      '制令单号',
      '录入时间',
      '客户名称',
      '型号',
      '条码',
      '位号',
      '车间',
      '产线',
      '岗位',
      '不良项目',
      '质检节点',
      '状态',
      '照片'
    ]
  },
  failure_case: {
    title: '品质失效案例文件格式要求',
    description: '请上传品质失效案例 Excel，系统会自动识别并规范化同义字段。',
    requiredFields: [
      '问题分类',
      '客户/发生工程/供应商',
      '质量问题',
      '问题描述',
      '问题处理',
      '原因分析',
      '采取措施'
    ],
    aliasTip: '第二列支持同义表头：问题来源、供应商、客户；上传后会统一为“客户/发生工程/供应商”。'
  }
}

const defaultFormatTip: FormatTip = {
  title: '文件格式要求',
  description: '请按当前处理器对应字段准备 Excel 后再上传。',
  requiredFields: []
}

const currentFormatTip = computed<FormatTip>(() => {
  return formatTips[currentProcessor.value] || defaultFormatTip
})

const uploadRef = ref()
const imageUploadRef = ref()
const selectedFile = ref<File | null>(null)
const selectedImageFile = ref<File | null>(null)
const imageDataSource = ref('')
const imageUploadStatus = ref<{ type: 'success' | 'warning' | 'info'; message: string } | null>(null)

const formatBytes = (bytes?: number | null) => {
  if (!bytes || bytes <= 0) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB']
  let value = bytes
  let unitIndex = 0

  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024
    unitIndex += 1
  }

  return `${value.toFixed(value >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`
}

const resolveProgressStatus = (phase: string): 'success' | 'exception' | undefined => {
  if (phase === 'success') return 'success'
  if (phase === 'exception') return 'exception'
  return undefined
}

const buildUploadProgressText = (
  state: { loaded: number; total: number | null; percentage: number; phase: string; message: string },
  processingText: string
) => {
  if (state.phase === 'uploading') {
    if (state.total) {
      return `已上传 ${formatBytes(state.loaded)} / ${formatBytes(state.total)} (${state.percentage}%)`
    }

    return `已上传 ${formatBytes(state.loaded)}`
  }

  if (state.phase === 'processing') {
    return state.message || processingText
  }

  return state.message
}

const excelProgressVisible = computed(() => store.excelUploadProgress.phase !== 'idle')
const excelProgressStatus = computed(() => resolveProgressStatus(store.excelUploadProgress.phase))
const excelProgressText = computed(() => buildUploadProgressText(store.excelUploadProgress, '文件已上传，正在等待服务器处理...'))

const imageProgressVisible = computed(() => store.imageUploadProgress.phase !== 'idle')
const imageProgressStatus = computed(() => resolveProgressStatus(store.imageUploadProgress.phase))
const imageProgressText = computed(() => buildUploadProgressText(store.imageUploadProgress, '压缩包已上传，正在等待服务器处理...'))

const handleFileChange = (file: UploadFile) => {
  selectedFile.value = file.raw || null
  store.resetExcelUploadProgress()
}

const handleFileRemove = () => {
  selectedFile.value = null
  store.resetExcelUploadProgress()
}

const resetExcelSelection = () => {
  selectedFile.value = null
  uploadRef.value?.clearFiles?.()
}

const handleUpload = async () => {
  if (!selectedFile.value) return

  try {
    const result = await store.uploadExcel(selectedFile.value)
    resetExcelSelection()

    if (!result.success) {
      ElMessage.error(result.message || '上传失败')
      return
    }

    if (store.currentProcessor === 'failure_case' && result.corpus_count && result.corpus_count > 0) {
      ElMessage.success(`上传成功，已生成 ${result.corpus_count} 条语料记录`)

      try {
        await ElMessageBox.confirm(
          `已为品质失效案例生成 ${result.corpus_count} 条语料记录，是否现在前往语料管理页面查看？`,
          '语料已就绪',
          {
            confirmButtonText: '前往语料管理',
            cancelButtonText: '稍后再去',
            type: 'success'
          }
        )

        router.push({ name: 'corpus' })
      } catch {
        // 用户取消跳转
      }

      return
    }

    ElMessage.success(result.message || '上传成功')
  } catch (error: any) {
    ElMessage.error(error?.message || '上传失败')
  }
}

const handleProcessorChange = async (value: string) => {
  await store.setCurrentProcessor(value)
  store.resetExcelUploadProgress()
  store.resetImageUploadProgress()
  imageUploadStatus.value = null
}

const handleRefreshFiles = () => {
  store.fetchProcessedFiles()
}

const handleImport = async (row: { data_source: string }) => {
  try {
    const result = await store.importJsonData(row.data_source)

    if (result.success) {
      ElMessage.success(`导入成功，新增 ${result.inserted_records} 条记录`)
    } else {
      ElMessage.error(result.message || '导入失败')
    }
  } catch (error: any) {
    ElMessage.error(error?.message || '导入失败')
  }
}

const handleDelete = async (row: { data_source: string }) => {
  try {
    await ElMessageBox.confirm(
      `确认彻底删除数据源“${row.data_source}”吗？这会同时删除处理文件、图片目录以及数据库中的相关记录，操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const result = await documentApi.deleteProcessedFile(store.currentProcessor, row.data_source)

    if (result.success) {
      ElMessage.success(result.message || '删除成功')
      store.fetchProcessedFiles()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error?.message || '删除失败')
    }
  }
}

const handleImageFileChange = (file: UploadFile) => {
  selectedImageFile.value = file.raw || null
  store.resetImageUploadProgress()
}

const handleImageFileRemove = () => {
  selectedImageFile.value = null
  store.resetImageUploadProgress()
}

const resetImageSelection = () => {
  selectedImageFile.value = null
  imageUploadRef.value?.clearFiles?.()
}

const handleImageUpload = async () => {
  if (!selectedImageFile.value || !imageDataSource.value) return

  imageUploadStatus.value = null

  try {
    const result = await store.uploadImagesZip(selectedImageFile.value, imageDataSource.value)

    if (result.success) {
      imageUploadStatus.value = {
        type: 'success',
        message: result.message || '图片上传成功'
      }
      resetImageSelection()
    } else {
      imageUploadStatus.value = {
        type: 'warning',
        message: result.message || '图片上传失败'
      }
    }
  } catch (error: any) {
    imageUploadStatus.value = {
      type: 'warning',
      message: error?.message || '图片上传失败'
    }
  }
}

const handleQueryImages = async () => {
  if (!imageDataSource.value) return

  try {
    const result = await documentApi.getImagesInfo(imageDataSource.value)

    if (result.count > 0) {
      imageUploadStatus.value = {
        type: 'success',
        message: `当前已有 ${result.count} 张图片`
      }
    } else {
      imageUploadStatus.value = {
        type: 'info',
        message: '当前目录下暂无图片'
      }
    }
  } catch {
    imageUploadStatus.value = {
      type: 'warning',
      message: '查询失败'
    }
  }
}

onMounted(() => {
  store.fetchProcessors()
  store.fetchProcessedFiles()
})
</script>

<style scoped lang="scss">
.document-import {
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

  .format-card {
    margin-bottom: 20px;

    .format-fields {
      margin-top: 12px;
      display: flex;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 8px;

      .format-label {
        color: #606266;
        font-size: 14px;
        line-height: 28px;
      }

      .field-tag {
        margin: 0;
      }
    }

    .alias-tip {
      margin-top: 10px;
    }
  }

  .upload-card,
  .files-card,
  .images-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
  }

  .excel-uploader {
    margin-bottom: 12px;
  }

  .upload-btn {
    width: 100%;
  }

  .image-uploader {
    display: inline-block;
  }

  .transfer-progress {
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 8px;
    background: #f5f7fa;

    .progress-text {
      margin: 10px 0 0;
      color: #606266;
      font-size: 13px;
      line-height: 1.5;
    }
  }

  .status-alert {
    margin-top: 12px;
  }
}
</style>
