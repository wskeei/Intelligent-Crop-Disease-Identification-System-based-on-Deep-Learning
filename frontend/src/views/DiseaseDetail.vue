<template>
  <div class="disease-detail-page">
    <div class="header-actions" v-motion-slide-top>
      <el-button @click="$router.back()" circle class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <h2>病害详情</h2>
    </div>

    <GlassCard class="detail-card" v-motion-fade>
      <div class="content">
         <div class="placeholder-icon">🌿</div>
         <h3>详情内容正在建设中</h3>
         <p>我们正在整理该病害的详细特征、发病规律与防治方法。</p>
         <el-button type="primary" @click="$router.back()">返回知识库</el-button>
      </div>
    </GlassCard>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft } from '@element-plus/icons-vue'
import GlassCard from '@/components/GlassCard.vue'
</script>

<style scoped>
.disease-detail-page {
  max-width: 800px;
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
  color: #1f2937;
  margin: 0;
}

.back-btn {
  border: none;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.detail-card {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.content h3 {
  font-size: 20px;
  color: #374151;
  margin-bottom: 8px;
}

.content p {
  color: #6b7280;
  margin-bottom: 24px;
}
</style>