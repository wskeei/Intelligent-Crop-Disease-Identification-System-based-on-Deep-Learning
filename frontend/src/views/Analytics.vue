<template>
  <div class="analytics-page">
    <h2>数据分析</h2>
    
    <!-- 时间范围选择 -->
    <el-card class="filter-card">
      <el-radio-group v-model="timeRange" @change="fetchData">
        <el-radio-button value="7">近7天</el-radio-button>
        <el-radio-button value="30">近30天</el-radio-button>
        <el-radio-button value="90">近90天</el-radio-button>
        <el-radio-button value="all">全部</el-radio-button>
      </el-radio-group>
    </el-card>

    <el-row :gutter="16" class="charts-row">
      <!-- 识别趋势折线图 -->
      <el-col :span="14">
        <el-card>
          <template #header>识别趋势</template>
          <div ref="trendChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      
      <!-- 病害类型分布饼图 -->
      <el-col :span="10">
        <el-card>
          <template #header>病害类型分布</template>
          <div ref="pieChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="charts-row">
      <!-- 作物健康状况柱状图 -->
      <el-col :span="12">
        <el-card>
          <template #header>作物健康状况</template>
          <div ref="barChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      
      <!-- Top 10 病害排行 -->
      <el-col :span="12">
        <el-card>
          <template #header>Top 10 病害排行</template>
          <div ref="rankChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { statsApi } from '@/api'
import type { StatsOverview, TrendData } from '@/types'

const timeRange = ref('30')
const trendChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()
const barChartRef = ref<HTMLElement>()
const rankChartRef = ref<HTMLElement>()

let trendChart: echarts.ECharts
let pieChart: echarts.ECharts
let barChart: echarts.ECharts
let rankChart: echarts.ECharts

const formatClassName = (name: string) => name.replace(/___/g, ' - ').replace(/_/g, ' ')

const initCharts = () => {
  if (trendChartRef.value) trendChart = echarts.init(trendChartRef.value)
  if (pieChartRef.value) pieChart = echarts.init(pieChartRef.value)
  if (barChartRef.value) barChart = echarts.init(barChartRef.value)
  if (rankChartRef.value) rankChart = echarts.init(rankChartRef.value)
}

const updateTrendChart = (data: TrendData[]) => {
  trendChart?.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['总数', '健康', '病害'] },
    xAxis: { type: 'category', data: data.map(d => d.date) },
    yAxis: { type: 'value' },
    series: [
      { name: '总数', type: 'line', data: data.map(d => d.total), smooth: true },
      { name: '健康', type: 'line', data: data.map(d => d.healthy), smooth: true, itemStyle: { color: '#67C23A' } },
      { name: '病害', type: 'line', data: data.map(d => d.diseased), smooth: true, itemStyle: { color: '#F56C6C' } }
    ]
  })
}

const updatePieChart = (data: StatsOverview) => {
  pieChart?.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: data.by_class.slice(0, 8).map(item => ({
        name: formatClassName(item.class),
        value: item.count
      }))
    }]
  })
}

const updateBarChart = (data: StatsOverview) => {
  const crops = data.by_crop.slice(0, 8)
  barChart?.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['健康', '病害'] },
    xAxis: { type: 'category', data: crops.map(c => c.crop), axisLabel: { rotate: 30 } },
    yAxis: { type: 'value' },
    series: [
      { name: '健康', type: 'bar', stack: 'total', data: crops.map(c => c.healthy), itemStyle: { color: '#67C23A' } },
      { name: '病害', type: 'bar', stack: 'total', data: crops.map(c => c.diseased), itemStyle: { color: '#F56C6C' } }
    ]
  })
}

const updateRankChart = (data: StatsOverview) => {
  const top10 = data.by_class.slice(0, 10).reverse()
  rankChart?.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: top10.map(d => formatClassName(d.class)) },
    series: [{ type: 'bar', data: top10.map(d => d.count), itemStyle: { color: '#409EFF' } }]
  })
}

const fetchData = async () => {
  const days = timeRange.value === 'all' ? 365 : parseInt(timeRange.value)
  const endDate = new Date().toISOString().split('T')[0]
  const startDate = new Date(Date.now() - days * 86400000).toISOString().split('T')[0]
  
  const [statsRes, trendRes] = await Promise.all([
    statsApi.overview(),
    statsApi.trend({ start_date: startDate, end_date: endDate })
  ])
  
  updateTrendChart(trendRes.data.data)
  updatePieChart(statsRes.data)
  updateBarChart(statsRes.data)
  updateRankChart(statsRes.data)
}

onMounted(async () => {
  await nextTick()
  initCharts()
  fetchData()
})
</script>

<style scoped lang="scss">
.analytics-page h2 { margin-bottom: 24px; }
.filter-card { margin-bottom: 16px; }
.charts-row { margin-bottom: 16px; }
</style>