<template>
  <div class="settings-page">
    <div class="header-section" v-motion-slide-top>
      <h2>系统设置</h2>
      <p class="subtitle">管理系统偏好与模型参数</p>
    </div>

    <div class="settings-container">
      <el-row :gutter="24">
        <el-col :span="8" v-motion-slide-left :delay="200">
          <GlassCard class="menu-card">
            <div 
              v-for="item in menuItems" 
              :key="item.key"
              class="menu-item" 
              :class="{ active: activeTab === item.key }"
              @click="activeTab = item.key"
            >
              <el-icon><component :is="item.icon" /></el-icon>
              <span>{{ item.label }}</span>
            </div>
          </GlassCard>
        </el-col>
        
        <el-col :span="16" v-motion-slide-right :delay="200">
          <GlassCard class="content-card">
            <div v-if="activeTab === 'general'">
               <h3><el-icon><Monitor /></el-icon> 通用设置</h3>
               <el-divider />
               <el-form label-position="top">
                 <el-form-item label="系统主题">
                   <el-radio-group v-model="settings.theme">
                     <el-radio label="light">清新绿 (默认)</el-radio>
                     <el-radio label="dark">深邃夜</el-radio>
                     <el-radio label="auto">跟随系统</el-radio>
                   </el-radio-group>
                 </el-form-item>
                 <el-form-item label="语言偏好">
                   <el-select v-model="settings.language">
                     <el-option label="简体中文" value="zh-CN" />
                     <el-option label="English" value="en-US" />
                   </el-select>
                 </el-form-item>
                 <el-form-item label="动画效果">
                   <el-switch v-model="settings.animations" active-text="开启界面动画" />
                 </el-form-item>
               </el-form>
            </div>
            
            <div v-else-if="activeTab === 'model'">
              <h3><el-icon><Cpu /></el-icon> 模型设置</h3>
              <el-divider />
              <el-form label-position="top">
                 <el-form-item label="置信度阈值">
                   <div class="slider-box">
                     <el-slider v-model="settings.confidenceThreshold" :min="0" :max="1" :step="0.05" show-input />
                   </div>
                   <p class="hint">低于此值的识别结果将被标记为"不确定"</p>
                 </el-form-item>
                 <el-form-item label="模型选择">
                   <el-select v-model="settings.model" style="width: 100%">
                     <el-option label="ResNet50 (高精度)" value="resnet50" />
                     <el-option label="MobileNetV3 (快速)" value="mobilenetv3" />
                   </el-select>
                 </el-form-item>
                 <el-form-item label="TTA (测试时增强)">
                   <el-switch v-model="settings.tta" active-text="开启 TTA 以提高准确率" />
                 </el-form-item>
              </el-form>
            </div>
            
            <div v-else-if="activeTab === 'notifications'">
              <h3><el-icon><Bell /></el-icon> 通知设置</h3>
              <el-divider />
              <el-form label-position="top">
                <el-form-item label="识别完成通知">
                   <el-switch v-model="settings.notifyComplete" />
                </el-form-item>
                <el-form-item label="异常结果警报">
                   <el-switch v-model="settings.notifyAlert" />
                </el-form-item>
                <el-form-item label="每周报告推送">
                   <el-switch v-model="settings.weeklyReport" />
                </el-form-item>
              </el-form>
            </div>
          </GlassCard>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Monitor, Cpu, Bell, User } from '@element-plus/icons-vue'
import GlassCard from '@/components/GlassCard.vue'

const activeTab = ref('general')

const menuItems = [
  { key: 'general', label: '通用设置', icon: Monitor },
  { key: 'model', label: '模型参数', icon: Cpu },
  { key: 'notifications', label: '通知管理', icon: Bell },
  { key: 'account', label: '账户信息', icon: User },
]

const settings = reactive({
  theme: 'light',
  language: 'zh-CN',
  animations: true,
  confidenceThreshold: 0.75,
  model: 'resnet50',
  tta: false,
  notifyComplete: true,
  notifyAlert: true,
  weeklyReport: false
})
</script>

<style scoped>
.settings-page {
  max-width: 1000px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 32px;
}
.header-section h2 {
  font-size: 28px;
  color: #1f2937;
  margin-bottom: 8px;
}
.subtitle {
  color: #6b7280;
}

.menu-card {
  padding: 12px !important;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  cursor: pointer;
  color: #4b5563;
  transition: all 0.3s;
  font-weight: 500;
}

.menu-item:hover {
  background: rgba(16, 185, 129, 0.05);
  color: #10b981;
}

.menu-item.active {
  background: linear-gradient(90deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
  color: #059669;
  font-weight: 600;
}

.content-card h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1f2937;
  margin-bottom: 0;
}

.hint {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}
</style>