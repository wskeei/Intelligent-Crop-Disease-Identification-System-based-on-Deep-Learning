<template>
  <div class="header-container">
    <div class="left">
      <el-icon class="toggle-btn" @click="$emit('toggle-sidebar')">
        <Fold />
      </el-icon>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="route.name !== 'Dashboard'">{{ routeTitle }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="right">
      <el-tooltip content="切换主题">
        <el-icon class="action-icon"><Sunny /></el-icon>
      </el-tooltip>
      <el-avatar :size="32">U</el-avatar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Fold, Sunny } from '@element-plus/icons-vue'

defineEmits(['toggle-sidebar'])
const route = useRoute()

const routeTitles: Record<string, string> = {
  Predict: '智能识别',
  History: '历史记录',
  Analytics: '数据分析',
  Diseases: '病害知识库',
  DiseaseDetail: '病害详情',
  Settings: '系统设置',
}
const routeTitle = computed(() => routeTitles[route.name as string] || '')
</script>

<style scoped lang="scss">
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
}
.left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.toggle-btn {
  font-size: 20px;
  cursor: pointer;
}
.right {
  display: flex;
  align-items: center;
  gap: 16px;
}
.action-icon {
  font-size: 18px;
  cursor: pointer;
}
</style>