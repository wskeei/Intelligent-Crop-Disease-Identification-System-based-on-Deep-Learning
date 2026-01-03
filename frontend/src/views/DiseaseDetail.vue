<template>
  <div class="disease-detail-page">
    <div class="header-actions" v-motion-slide-top>
      <el-button @click="$router.back()" circle class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <h2>{{ disease?.name || '加载中...' }}</h2>
    </div>

    <div v-if="disease" class="content-wrapper">
      <!-- Left Column: Icon and Basic Info -->
      <div class="left-col" v-motion-slide-left>
        <GlassCard class="info-card">
          <div class="icon-wrapper">
             <span class="icon">{{ disease.icon }}</span>
          </div>
          <div class="basic-info">
            <el-tag :type="getSeverityType(disease.severityLevel)" effect="dark" class="severity-tag">
              {{ disease.severity }}
            </el-tag>
            <span class="category">{{ disease.category }}</span>
          </div>
          <p class="description">{{ disease.description }}</p>
        </GlassCard>
      </div>

      <!-- Right Column: Detailed Content -->
      <div class="right-col" v-motion-slide-right :delay="200">
        <GlassCard class="detail-section">
          <h3><span class="emoji">🔍</span> 症状表现</h3>
          <ul>
            <li v-for="(symp, idx) in disease.symptoms" :key="idx">{{ symp }}</li>
          </ul>
        </GlassCard>

        <GlassCard class="detail-section" :delay="300">
           <h3><span class="emoji">🌡️</span> 发病原因</h3>
           <ul>
             <li v-for="(cause, idx) in disease.causes" :key="idx">{{ cause }}</li>
           </ul>
        </GlassCard>

        <GlassCard class="detail-section" :delay="400">
           <h3><span class="emoji">🛡️</span> 预防措施</h3>
           <ul>
             <li v-for="(prev, idx) in disease.prevention" :key="idx">{{ prev }}</li>
           </ul>
        </GlassCard>
        
        <GlassCard class="detail-section" :delay="500">
           <h3><span class="emoji">💊</span> 治疗方案</h3>
           <ul>
             <li v-for="(treat, idx) in disease.treatment" :key="idx">{{ treat }}</li>
           </ul>
        </GlassCard>
      </div>
    </div>
    
    <div v-else class="loading-state">
      <GlassCard>
        <el-empty description="未找到相关病害信息" />
      </GlassCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import GlassCard from '@/components/GlassCard.vue'
import { diseases } from '@/constants/diseases'

const route = useRoute()
const diseaseId = route.params.id as string

const disease = computed(() => diseases.find(d => d.id === diseaseId))

const getSeverityType = (level: string) => {
  switch (level) {
    case 'high': return 'danger'
    case 'medium': return 'warning'
    case 'low': return 'success'
    default: return 'info'
  }
}
</script>

<style scoped>
.disease-detail-page {
  max-width: 1200px;
  margin: 0 auto;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.header-actions h2 {
  font-size: 24px;
  color: var(--text-main);
  margin: 0;
}

.back-btn {
  border: none;
  background: var(--glass-bg);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.content-wrapper {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 24px;
  align-items: start;
}

.info-card {
  text-align: center;
  padding: 32px !important;
}

.icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.1));
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
}

.icon {
  font-size: 64px;
}

.basic-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 16px;
}

.category {
  color: var(--text-secondary);
  font-size: 14px;
  background: rgba(0,0,0,0.05);
  padding: 2px 8px;
  border-radius: 4px;
}

.description {
  color: var(--text-secondary);
  line-height: 1.6;
  text-align: left;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  color: var(--text-main);
  font-size: 18px;
}

.detail-section ul {
  padding-left: 20px;
  color: var(--text-secondary);
  line-height: 1.8;
}

.detail-section li {
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }
}
</style>