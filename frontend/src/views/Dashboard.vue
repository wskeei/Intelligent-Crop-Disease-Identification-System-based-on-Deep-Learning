<template>
  <div class="dashboard">
    <h2>工作台</h2>
    
    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="今日识别数" :value="stats?.today_count || 0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="总识别数" :value="stats?.total || 0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="健康作物占比" :value="healthyPercent" suffix="%" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="支持作物种类" :value="14" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷操作 -->
    <el-row :gutter="16" class="section">
      <el-col :span="24">
        <el-card>
          <template #header>快捷操作</template>
          <el-button type="primary" size="large" @click="$router.push('/predict')">
            <el-icon><Camera /></el-icon> 开始识别
          </el-button>
          <el-button size="large" @click="$router.push('/history')">查看历史</el-button>
          <el-button size="large" @click="$router.push('/analytics')">数据报告</el-button>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近记录和病害分布 -->
    <el-row :gutter="16" class="section">
      <el-col :span="14">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近识别记录</span>
              <el-button link type="primary" @click="$router.push('/history')">查看更多</el-button>
            </div>
          </template>
          <el-table :data="recentRecords" size="small">
            <el-table-column label="图片" width="70">
              <template #default="{ row }">
                <el-image :src="`/uploads/${row.image_path}`" style="width: 50px; height: 50px" fit="cover" />
              </template>
            </el-table-column>
            <el-table-column label="病害名称">
              <template #default="{ row }">{{ formatClassName(row.predicted_class) }}</template>
            </el-table-column>
            <el-table-column label="置信度" width="100">
              <template #default="{ row }">{{ (row.confidence * 100).toFixed(1) }}%</template>
            </el-table-column>
            <el-table-column label="时间" width="160">
              <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
            </el-table-column>
          </el-table>
          <el-empty v-if="!recentRecords.length" description="暂无识别记录" />
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card>
          <template #header>病害分布 Top 5</template>
          <div ref="chartRef" style="height: 280px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Camera } from '@element-plus/icons-vue'
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
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: top5.map(item => ({
        name: formatClassName(item.class),
        value: item.count
      })),
      label: { show: false },
      emphasis: { label: { show: true, fontWeight: 'bold' } }
    }]
  })
}

onMounted(async () => {
  const [statsRes, historyRes] = await Promise.all([
    statsApi.overview(),
    historyApi.list({ limit: 5 })
  ])
  stats.value = statsRes.data
  recentRecords.value = historyRes.data
  initChart()
})
</script>

<style scoped lang="scss">
.dashboard h2 { margin-bottom: 24px; }
.stat-cards, .section { margin-bottom: 16px; }
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.el-button + .el-button { margin-left: 12px; }
</style>