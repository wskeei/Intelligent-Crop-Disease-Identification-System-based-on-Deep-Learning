<template>
  <div class="dashboard">
    <h2>工作台</h2>
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

    <el-row :gutter="16" class="quick-actions">
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Camera } from '@element-plus/icons-vue'
import { statsApi } from '@/api'
import type { StatsOverview } from '@/types'

const stats = ref<StatsOverview | null>(null)
const healthyPercent = computed(() => 
  stats.value ? Math.round(stats.value.healthy_rate * 100) : 0
)

onMounted(async () => {
  const { data } = await statsApi.overview()
  stats.value = data
})
</script>

<style scoped lang="scss">
.dashboard h2 {
  margin-bottom: 24px;
}
.stat-cards {
  margin-bottom: 24px;
}
.quick-actions .el-button {
  margin-right: 12px;
}
</style>