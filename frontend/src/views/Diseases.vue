<template>
  <div class="diseases-page">
    <div class="header-section" v-motion-slide-top>
      <h2>病害知识库</h2>
      <p class="subtitle">全面收录各类农业病害特征与防治方案</p>
      
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索病害名称..."
          class="glass-input"
          size="large"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>
    
    <div class="disease-grid">
      <div 
        v-for="(disease, index) in filteredDiseases" 
        :key="disease.id"
        class="disease-item"
        v-motion-pop-visible
        :delay="index * 50"
      >
        <GlassCard class="disease-card" @click="$router.push(`/diseases/${disease.id}`)">
           <div class="image-wrapper">
             <div class="image-placeholder">
               <span>{{ disease.icon }}</span>
             </div>
             <div class="category-tag">{{ disease.category }}</div>
           </div>
           
           <div class="content">
             <h3>{{ disease.name }}</h3>
             <p class="description">{{ disease.description }}</p>
             
             <div class="footer">
               <span class="severity" :class="disease.severityLevel">
                 {{ disease.severity }}
               </span>
               <el-button link type="primary">
                 详情 <el-icon><ArrowRight /></el-icon>
               </el-button>
             </div>
           </div>
        </GlassCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search, ArrowRight } from '@element-plus/icons-vue'
import GlassCard from '@/components/GlassCard.vue'

const searchQuery = ref('')

// Mock data
const diseases = [
  {
    id: 'apple_scab',
    name: '苹果黑星病',
    category: '真菌病害',
    icon: '🍎',
    description: '主要危害叶片、果实和嫩梢。叶片发病初期产生黄绿色斑点...',
    severity: '高风险',
    severityLevel: 'high'
  },
  {
    id: 'corn_common_rust',
    name: '玉米普通锈病',
    category: '真菌病害',
    icon: '🌽',
    description: '在叶片两面散生或聚生圆形至长椭圆形隆起的夏孢子堆...',
    severity: '中风险',
    severityLevel: 'medium'
  },
  {
    id: 'grape_black_rot',
    name: '葡萄黑腐病',
    category: '真菌病害',
    icon: '🍇',
    description: '主要危害果实、叶片。果实受害后变黑、干缩...',
    severity: '高风险',
    severityLevel: 'high'
  },
  {
    id: 'tomato_bacterial_spot',
    name: '番茄细菌性斑点病',
    category: '细菌病害',
    icon: '🍅',
    description: '叶片上产生深褐色至黑色圆形小斑点，周围有黄色晕圈...',
    severity: '中风险',
    severityLevel: 'medium'
  },
  {
    id: 'potato_early_blight',
    name: '马铃薯早疫病',
    category: '真菌病害',
    icon: '🥔',
    description: '主要侵染叶片。病斑圆形或近圆形，黑褐色，具同心轮纹...',
    severity: '低风险',
    severityLevel: 'low'
  },
  {
    id: 'strawberry_leaf_scorch',
    name: '草莓叶枯病',
    category: '真菌病害',
    icon: '🍓',
    description: '叶片上产生紫红色小斑点，后扩大为不规则形病斑...',
    severity: '中风险',
    severityLevel: 'medium'
  }
]

const filteredDiseases = computed(() => {
  if (!searchQuery.value) return diseases
  const q = searchQuery.value.toLowerCase()
  return diseases.filter(d => 
    d.name.includes(q) || d.category.includes(q)
  )
})
</script>

<style scoped>
.diseases-page {
  max-width: 1400px;
  margin: 0 auto;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
}
.header-section h2 {
  font-size: 32px;
  color: #1f2937;
  margin-bottom: 8px;
}
.subtitle {
  color: #6b7280;
  margin-bottom: 24px;
}

.search-bar {
  max-width: 500px;
  margin: 0 auto;
}

:deep(.glass-input .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  border-radius: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 8px 16px;
}

.disease-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.disease-card {
  height: 100%;
  padding: 0;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.image-wrapper {
  height: 160px;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.image-placeholder {
  font-size: 64px;
}

.category-tag {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: #059669;
}

.content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.content h3 {
  font-size: 18px;
  color: #1f2937;
  margin-bottom: 8px;
}

.description {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.severity {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
}
.severity.high { color: #dc2626; background: #fee2e2; }
.severity.medium { color: #d97706; background: #fef3c7; }
.severity.low { color: #059669; background: #d1fae5; }
</style>