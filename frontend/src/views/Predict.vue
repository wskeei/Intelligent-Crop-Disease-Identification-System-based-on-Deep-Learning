<template>
  <div class="predict-page">
    <h2>智能识别</h2>
    
    <el-row :gutter="24">
      <el-col :span="12">
        <el-card>
          <template #header>上传图片</template>
          <el-upload
            class="upload-area"
            drag
            :auto-upload="false"
            :show-file-list="false"
            accept="image/jpeg,image/png,image/webp"
            :on-change="handleFileChange"
          >
            <div v-if="!previewUrl" class="upload-placeholder">
              <el-icon class="upload-icon"><UploadFilled /></el-icon>
              <div>点击或拖拽图片到此处上传</div>
              <div class="upload-tip">支持 JPG、PNG、WebP 格式，最大 10MB</div>
            </div>
            <img v-else :src="previewUrl" class="preview-image" />
          </el-upload>
          <el-button 
            type="primary" 
            :loading="loading" 
            :disabled="!selectedFile"
            @click="handlePredict"
            style="margin-top: 16px; width: 100%"
          >
            开始识别
          </el-button>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card v-if="result">
          <template #header>识别结果</template>
          <div class="result-main">
            <div class="disease-name">{{ formatClassName(result.predicted_class) }}</div>
            <div class="confidence">
              置信度: 
              <el-progress :percentage="Math.round(result.confidence * 100)" :stroke-width="20" />
            </div>
          </div>
          <el-divider />
          <div class="top-predictions">
            <div class="title">其他可能结果</div>
            <div v-for="(pred, idx) in result.top_predictions.slice(1)" :key="idx" class="pred-item">
              <span>{{ formatClassName(pred.class) }}</span>
              <span>{{ (pred.confidence * 100).toFixed(1) }}%</span>
            </div>
          </div>
        </el-card>
        <el-empty v-else description="上传图片后查看识别结果" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { UploadFile } from 'element-plus'
import { predictApi } from '@/api'
import type { PredictionResult } from '@/types'

const selectedFile = ref<File | null>(null)
const previewUrl = ref('')
const loading = ref(false)
const result = ref<PredictionResult | null>(null)

const handleFileChange = (file: UploadFile) => {
  if (file.raw) {
    selectedFile.value = file.raw
    previewUrl.value = URL.createObjectURL(file.raw)
    result.value = null
  }
}

const handlePredict = async () => {
  if (!selectedFile.value) return
  loading.value = true
  try {
    const { data } = await predictApi.upload(selectedFile.value)
    result.value = data
    ElMessage.success('识别完成')
  } catch {
    ElMessage.error('识别失败，请重试')
  } finally {
    loading.value = false
  }
}

const formatClassName = (name: string) => {
  return name.replace(/___/g, ' - ').replace(/_/g, ' ')
}
</script>

<style scoped lang="scss">
.predict-page h2 {
  margin-bottom: 24px;
}
.upload-area {
  width: 100%;
}
.upload-placeholder {
  padding: 40px;
  text-align: center;
  color: #909399;
}
.upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
.upload-tip {
  font-size: 12px;
  margin-top: 8px;
}
.preview-image {
  max-width: 100%;
  max-height: 300px;
}
.result-main {
  text-align: center;
}
.disease-name {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 16px;
}
.top-predictions {
  .title {
    font-weight: bold;
    margin-bottom: 12px;
  }
  .pred-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #eee;
  }
}
</style>