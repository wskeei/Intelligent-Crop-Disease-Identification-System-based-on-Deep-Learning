<template>
  <div class="dashboard">
    <div class="header-section" v-motion-slide-top>
      <h2>工作台</h2>
      <p class="subtitle">实时监控作物健康状态与系统运行情况</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stat-cards">
      <div class="stat-item" v-motion-slide-bottom :delay="100">
        <GlassCard>
          <div class="stat-content">
            <div class="stat-icon bg-blue">
              <el-icon><DataLine /></el-icon>
            </div>
            <div class="stat-info">
              <div class="label">今日识别数</div>
              <div class="value">{{ stats?.today_count || 0 }}</div>
            </div>
          </div>
        </GlassCard>
      </div>
      <div class="stat-item" v-motion-slide-bottom :delay="200">
        <GlassCard>
          <div class="stat-content">
            <div class="stat-icon bg-purple">
              <el-icon><Collection /></el-icon>
            </div>
            <div class="stat-info">
              <div class="label">总识别数</div>
              <div class="value">{{ stats?.total || 0 }}</div>
            </div>
          </div>
        </GlassCard>
      </div>
      <div class="stat-item" v-motion-slide-bottom :delay="300">
        <GlassCard>
          <div class="stat-content">
            <div class="stat-icon bg-green">
              <el-icon><SuccessFilled /></el-icon>
            </div>
            <div class="stat-info">
              <div class="label">健康作物占比</div>
              <div class="value">{{ healthyPercent }}%</div>
            </div>
          </div>
        </GlassCard>
      </div>
      <div class="stat-item" v-motion-slide-bottom :delay="400">
        <GlassCard>
          <div class="stat-content">
            <div class="stat-icon bg-orange">
              <el-icon><Menu /></el-icon>
            </div>
            <div class="stat-info">
              <div class="label">支持作物种类</div>
              <div class="value">14</div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="section-row" v-motion-fade :delay="500">
      <GlassCard class="action-card">
        <div class="card-title">快捷操作</div>
        <div class="action-buttons">
          <el-button type="primary" size="large" class="main-btn" @click="$router.push('/predict')">
            <el-icon><Camera /></el-icon> 开始识别
          </el-button>
          <el-button size="large" class="glass-btn" @click="$router.push('/history')">
            <el-icon><Clock /></el-icon> 查看历史
          </el-button>
          <el-button size="large" class="glass-btn" @click="$router.push('/analytics')">
            <el-icon><PieChart /></el-icon> 数据报告
          </el-button>
        </div>
      </GlassCard>
    </div>

    <!-- 最近记录和病害分布 -->
    <div class="section-row chart-row">
      <div class="col-left" v-motion-slide-left :delay="600">
        <GlassCard class="h-full">
          <div class="card-header">
            <span>最近识别记录</span>
            <el-button link type="primary" @click="$router.push('/history')">查看更多</el-button>
          </div>
          <el-table :data="recentRecords" style="width: 100%; background: transparent" :row-style="{ background: 'transparent' }" :header-cell-style="{ background: 'transparent' }">
            <el-table-column label="图片" width="80">
              <template #default="{ row }">
                <el-image 
                  :src="`/uploads/${row.image_path}`" 
                  style="width: 48px; height: 48px; border-radius: 8px" 
                  fit="cover" 
                  class="table-img"
                />
              </template>
            </el-table-column>
            <el-table-column label="病害名称">
              <template #default="{ row }">
                <span class="disease-tag">{{ formatClassName(row.predicted_class) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="置信度" width="100">
              <template #default="{ row }">
                <span class="confidence-text">{{ (row.confidence * 100).toFixed(1) }}%</span>
              </template>
            </el-table-column>
            <el-table-column label="时间" width="160">
              <template #default="{ row }">
                <span class="time-text">{{ formatDate(row.created_at) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </GlassCard>
      </div>
      <div class="col-right" v-motion-slide-right :delay="600">
        <GlassCard class="h-full">
          <div class="card-title">病害分布 Top 5</div>
          <div ref="chartRef" style="height: 300px; width: 100%"></div>
        </GlassCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Camera, DataLine, Collection, SuccessFilled, Menu, Clock, PieChart } from '@element-plus/icons-vue'
import GlassCard from '@/components/GlassCard.vue'
import * as echarts from 'echarts'
import { statsApi, historyApi } from '@/api'
import type { StatsOverview, PredictionRecord } from '@/types'

const stats = ref<StatsOverview | null>(null)
const recentRecords = ref<PredictionRecord[]>([])
const chartRef = ref<HTMLElement>()

const healthyPercent = computed(() => 
  stats.value ? Math.round(stats.value.healthy_rate * 100) : 0
)

const formatClassName = (name: string) => name.replace(/___/g, ' - ').replace(/_/g, ' ')
const formatDate = (date: string) => new Date(date).toLocaleString('zh-CN')

const initChart = () => {
  if (!chartRef.value || !stats.value?.by_class.length) return
  const chart = echarts.init(chartRef.value)
  const top5 = stats.value.by_class.slice(0, 5)
  
  chart.setOption({
    tooltip: { 
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#e5e7eb',
      textStyle: { color: '#374151' }
    },
    legend: {
      top: '5%',
      left: 'center',
      textStyle: { color: '#4b5563' }
    },
    series: [{
      name: '病害分布',
      type: 'pie',
      radius: ['45%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: { show: false, position: 'center' },
      emphasis: {
        label: { show: true, fontSize: 18, fontWeight: 'bold' }
      },
      data: top5.map(item => ({
        name: formatClassName(item.class),
        value: item.count
      }))
    }],
    color: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6']
  })
  
  // Resize chart on window resize
  window.addEventListener('resize', () => chart.resize())
}

onMounted(async () => {
  try {
    const [statsRes, historyRes] = await Promise.all([
      statsApi.overview(),
      historyApi.list({ limit: 5 })
    ])
    stats.value = statsRes.data
    recentRecords.value = historyRes.data
    initChart()
  } catch (error) {
    console.error('Failed to load dashboard data', error)
  }
})
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 32px;
}
.header-section h2 {
  font-size: 28px;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 8px;
}
.subtitle {
  color: #6b7280;
  font-size: 16px;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.bg-blue { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
.bg-purple { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); }
.bg-green { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.bg-orange { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }

.stat-info .label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}
.stat-info .value {
  font-size: 24px;
  font-weight: 800;
  color: #1f2937;
}

.section-row {
  margin-bottom: 32px;
}

.card-title, .card-header span {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 20px;
  display: block;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.action-buttons {
  display: flex;
  gap: 16px;
}

.main-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  font-weight: 600;
  padding: 12px 24px;
  height: auto;
}

.glass-btn {
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.6);
  color: #4b5563;
  backdrop-filter: blur(4px);
}
.glass-btn:hover {
  background: rgba(255, 255, 255, 0.8);
  color: #10b981;
  border-color: #10b981;
}

.chart-row {
  display: flex;
  gap: 24px;
}
.col-left { flex: 3; }
.col-right { flex: 2; }

.h-full { height: 100%; }

.table-img {
  transition: transform 0.2s;
}
.table-img:hover {
  transform: scale(1.1);
}

.disease-tag {
  font-weight: 600;
  color: #374151;
}

:deep(.el-table) {
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: transparent;
  --el-table-row-hover-bg-color: rgba(16, 185, 129, 0.05);
  color: #4b5563;
}
:deep(.el-table th.el-table__cell) {
  background: transparent;
  color: #6b7280;
  font-weight: 600;
}
</style>
