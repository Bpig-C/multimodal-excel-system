<template>
  <div class="file-uploader">
    <el-upload
      ref="uploadRef"
      class="upload-area"
      drag
      :before-upload="handleBeforeUpload"
      :http-request="handleUpload"
      :show-file-list="false"
      :disabled="uploading"
      accept=".xlsx,.xls"
    >
      <div class="upload-content">
        <el-icon v-if="!uploading" class="upload-icon">
          <UploadFilled />
        </el-icon>
        <el-icon v-else class="upload-icon uploading">
          <Loading />
        </el-icon>
        
        <div class="upload-text">
          <p v-if="!uploading" class="primary-text">
            将Excel文件拖到此处，或<em>点击上传</em>
          </p>
          <p v-else class="primary-text">上传中...</p>
          <p class="hint-text">支持 .xlsx 和 .xls 格式文件</p>
        </div>
      </div>
    </el-upload>

    <!-- 上传进度 -->
    <div v-if="uploading" class="upload-progress">
      <el-progress
        :percentage="uploadProgress"
        :status="uploadStatus"
        :stroke-width="8"
      />
      <p class="progress-text">{{ progressText }}</p>
    </div>

    <!-- 文件格式说明 -->
    <el-collapse v-if="!uploading" class="format-info">
      <el-collapse-item title="Excel文件格式说明" name="format">
        <div class="format-content">
          <div class="format-item">
            <h4>必需列</h4>
            <ul>
              <li><code>问题描述</code> - 问题的详细描述</li>
              <li><code>原因分析</code> - 问题原因分析</li>
              <li><code>采取措施</code> - 采取的解决措施</li>
            </ul>
          </div>
          
          <div class="format-item">
            <h4>图片支持</h4>
            <p>Excel中的内嵌图片会自动提取并关联到对应的语料记录</p>
            <p>支持WPS和Microsoft Excel格式</p>
          </div>

          <div class="format-item">
            <h4>文本处理</h4>
            <p>系统会自动：</p>
            <ul>
              <li>以单元格为单位处理文本（一个单元格生成一条语料）</li>
              <li>提取DISPIMG公式并转换为Markdown格式</li>
              <li>生成唯一的语料ID</li>
            </ul>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Loading } from '@element-plus/icons-vue'
import type { UploadRequestOptions } from 'element-plus'
import { useCorpusStore } from '@/stores'

const emit = defineEmits<{
  success: [response: any]
  error: [error: any]
}>()

const corpusStore = useCorpusStore()

// 状态
const uploadRef = ref()
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref<'success' | 'exception' | 'warning' | undefined>()
const progressText = ref('')

// 上传前验证
const handleBeforeUpload = (file: File) => {
  const fileName = file.name.toLowerCase()
  const isValidType = fileName.endsWith('.xlsx') || fileName.endsWith('.xls')
  
  if (!isValidType) {
    ElMessage.error('只支持 Excel 格式文件（.xlsx 或 .xls）')
    return false
  }

  const maxSize = 100 * 1024 * 1024 // 100MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 100MB')
    return false
  }

  return true
}

// 处理上传
const handleUpload = async (options: UploadRequestOptions) => {
  const { file } = options

  uploading.value = true
  uploadProgress.value = 0
  uploadStatus.value = undefined
  progressText.value = '正在上传文件...'

  try {
    // 模拟进度
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10
      }
    }, 300)

    const result = await corpusStore.upload(file as File)

    clearInterval(progressInterval)

    uploadProgress.value = 100
    uploadStatus.value = 'success'
    progressText.value = result.message || `上传成功！共 ${result.total_sentences} 条语料`
    
    setTimeout(() => {
      uploading.value = false
      emit('success', result)
    }, 1500)
  } catch (error: any) {
    uploadProgress.value = 0
    uploadStatus.value = 'exception'
    progressText.value = '上传失败，请重试'
    
    setTimeout(() => {
      uploading.value = false
    }, 2000)

    emit('error', error)
    ElMessage.error(error.message || '上传失败')
  }
}
</script>

<style scoped lang="scss">
.file-uploader {
  .upload-area {
    width: 100%;

    :deep(.el-upload) {
      width: 100%;
    }

    :deep(.el-upload-dragger) {
      width: 100%;
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px dashed #d9d9d9;
      border-radius: 8px;
      transition: all 0.3s;

      &:hover {
        border-color: #409eff;
      }
    }
  }

  .upload-content {
    text-align: center;

    .upload-icon {
      font-size: 60px;
      color: #c0c4cc;
      margin-bottom: 16px;

      &.uploading {
        color: #409eff;
        animation: rotating 2s linear infinite;
      }
    }

    .upload-text {
      .primary-text {
        margin: 0 0 8px;
        font-size: 14px;
        color: #606266;

        em {
          color: #409eff;
          font-style: normal;
        }
      }

      .hint-text {
        margin: 0;
        font-size: 12px;
        color: #909399;
      }
    }
  }

  .upload-progress {
    margin-top: 20px;
    padding: 16px;
    background: #f5f7fa;
    border-radius: 8px;

    .progress-text {
      margin: 12px 0 0;
      text-align: center;
      font-size: 13px;
      color: #606266;
    }
  }

  .format-info {
    margin-top: 20px;

    .format-content {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .format-item {
      h4 {
        margin: 0 0 8px;
        font-size: 14px;
        color: #303133;
        font-weight: 600;
      }

      p {
        margin: 0 0 8px;
        font-size: 13px;
        color: #606266;
      }

      ul {
        margin: 0;
        padding-left: 20px;
        font-size: 13px;
        color: #606266;

        li {
          margin-bottom: 4px;
        }
      }

      code {
        padding: 2px 6px;
        background: #f5f7fa;
        border: 1px solid #e4e7ed;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        color: #e6a23c;
        font-size: 12px;
      }
    }
  }
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
