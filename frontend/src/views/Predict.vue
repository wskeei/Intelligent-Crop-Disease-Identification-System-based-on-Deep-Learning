<template>
  <div class="predict-page">
    <div class="header-section" v-motion-slide-top>
      <h2>智能识别</h2>
      <p class="subtitle">上传作物图片，AI 助手将为您诊断病虫害</p>
    </div>
    
    <div class="content-row">
      <div class="col-left" v-motion-slide-left :delay="200">
        <GlassCard class="upload-card">
          <div class="card-title">上传图片</div>
          <el-upload
            class="upload-area"
            drag
            :auto-upload="false"
            :show-file-list="false"
            accept="image/jpeg,image/png,image/webp"
            :on-change="handleFileChange"
          >
            <div v-if="!previewUrl" class="upload-placeholder">
              <div class="icon-circle">
                <el-icon class="upload-icon"><UploadFilled /></el-icon>
              </div>
              <div class="upload-text">点击或拖拽图片到此处上传</div>
              <div class="upload-tip">支持 JPG、PNG、WebP 格式，最大 10MB</div>
            </div>
            <img v-else :src="previewUrl" class="preview-image" />
          </el-upload>
          
          <div class="actions">
             <el-button 
              type="primary" 
              size="large"
              :loading="loading" 
              :disabled="!selectedFile"
              @click="handlePredict"
              class="predict-btn"
            >
              <el-icon class="mr-2"><Aim /></el-icon> 开始识别
            </el-button>
             <el-button 
              v-if="previewUrl"
              size="large"
              @click="clearFile"
              class="clear-btn"
            >
              重新上传
            </el-button>
          </div>
        </GlassCard>
      </div>
      
      <div class="col-right" v-if="result || loading">
        <GlassCard class="result-card" v-motion-pop-visible>
           <div v-if="loading" class="loading-state">
             <div class="scanning-animation"></div>
             <p>正在分析图像特征...</p>
           </div>
           
           <div v-else-if="result" class="result-content">
              <div class="result-header">
                <div class="badge">识别成功</div>
                <div class="confidence-badge">{{ (result.confidence * 100).toFixed(1) }}% 置信度</div>
              </div>
              
              <div class="main-result">
                <div class="disease-icon">🌿</div>
                <div class="disease-info">
                  <div class="label">诊断结果</div>
                  <div class="value">{{ formatClassName(result.predicted_class) }}</div>
                </div>
              </div>
              
              <div class="probability-bar">
                 <div class="bar-bg">
                   <div class="bar-fill" :style="{ width: `${result.confidence * 100}%` }"></div>
                 </div>
              </div>
              
              <div class="suggestions" v-if="result.predicted_class !== 'Healthy'">
                <div class="section-title">可能原因与建议</div>
                <p class="suggestion-text">系统检测到病害特征，建议查阅知识库获取详细防治方案。</p>
                <el-button type="primary" link @click="$router.push(`/diseases/${result.predicted_class}`)">
                  查看防治详情 <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
              
              <div class="divider"></div>
              
              <div class="other-results">
                <div class="section-title">其他可能性</div>
                <div v-for="(pred, idx) in result.top_predictions.slice(1, 4)" :key="idx" class="other-item">
                  <span>{{ formatClassName(pred.class) }}</span>
                  <span class="other-score">{{ (pred.confidence * 100).toFixed(1) }}%</span>
                </div>
              </div>
           </div>
        </GlassCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled, Aim, ArrowRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { UploadFile } from 'element-plus'
import GlassCard from '@/components/GlassCard.vue'
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

const clearFile = () => {
  selectedFile.value = null
  previewUrl.value = ''
  result.value = null
}

const handlePredict = async () => {
  if (!selectedFile.value) return
  loading.value = true
  // Reset result to show loading state effectively if re-running
  result.value = null
  
  try {
    const { data } = await predictApi.upload(selectedFile.value)
    // Simulate a small delay for better UX animation if API is too fast
    await new Promise(resolve => setTimeout(resolve, 800))
    result.value = data
    ElMessage.success('识别完成')
  } catch {
    ElMessage.error('识别失败，请重试')
    loading.value = false // Stop loading on error
  } finally {
    if (result.value) loading.value = false
  }
}

const formatClassName = (name: string) => {
  return name.replace(/___/g, ' - ').replace(/_/g, ' ')
}
</script>

<style scoped>
.predict-page {
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 32px;
  text-align: center;
}
.header-section h2 {
  font-size: 32px;
  background: linear-gradient(135deg, #1f2937 0%, #4b5563 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 8px;
}
.subtitle {
  color: #6b7280;
  font-size: 16px;
}

.content-row {
  display: flex;
  gap: 32px;
  align-items: flex-start;
  justify-content: center;
}

.col-left, .col-right {
  flex: 1;
  max-width: 500px;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 20px;
}

.upload-area {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.4);
  border: 2px dashed rgba(16, 185, 129, 0.3);
  border-radius: 16px;
  transition: all 0.3s;
}

:deep(.el-upload-dragger:hover) {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.05);
}

.upload-placeholder {
  text-align: center;
}

.icon-circle {
  width: 80px;
  height: 80px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.upload-icon {
  font-size: 40px;
  color: #10b981;
}

.upload-text {
  font-size: 16px;
  color: #374151;
  margin-bottom: 8px;
}

.upload-tip {
  font-size: 13px;
  color: #9ca3af;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.actions {
  margin-top: 24px;
  display: flex;
  gap: 16px;
}

.predict-btn {
  flex: 1;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.clear-btn {
  border-color: #e5e7eb;
  color: #6b7280;
}

/* Result Card Styles */
.result-content {
  padding: 8px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
}

.badge {
  background: #ecfdf5;
  color: #059669;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.confidence-badge {
  color: #6b7280;
  font-size: 13px;
}

.main-result {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.disease-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2);
}

.disease-info .label {
  font-size: 14px;
  color: #6b7280;
}

.disease-info .value {
  font-size: 24px;
  font-weight: 800;
  color: #1f2937;
}

.probability-bar {
  margin-bottom: 24px;
}
.bar-bg {
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  background: #10b981;
  border-radius: 4px;
  transition: width 1s ease-out;
}

.divider {
  height: 1px;
  background: #f3f4f6;
  margin: 24px 0;
}

.section-title {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 12px;
}

.other-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px dashed #f3f4f6;
  font-size: 14px;
  color: #4b5563;
}
.other-item:last-child {
  border-bottom: none;
}
.other-score {
  color: #9ca3af;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #6b7280;
}
.scanning-animation {
  width: 60px;
  height: 60px;
  border: 4px solid #f3f4f6;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.mr-2 { margin-right: 8px; }
</style>
