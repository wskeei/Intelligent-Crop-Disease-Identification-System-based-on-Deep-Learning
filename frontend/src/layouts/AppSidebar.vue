<template>
  <div class="sidebar-container">
    <div class="logo">
      <div class="logo-icon-wrapper">
        <span class="logo-icon">🌱</span>
      </div>
      <transition name="fade">
        <span v-if="!collapsed" class="logo-text">CropVision</span>
      </transition>
    </div>
    
    <el-menu
      :default-active="route.path"
      :collapse="collapsed"
      class="glass-menu"
      :collapse-transition="false"
      router
    >
      <el-menu-item index="/">
        <el-icon><DataLine /></el-icon>
        <template #title>工作台</template>
      </el-menu-item>
      <el-menu-item index="/predict">
        <el-icon><Aim /></el-icon>
        <template #title>智能识别</template>
      </el-menu-item>
      <el-menu-item index="/history">
        <el-icon><Timer /></el-icon>
        <template #title>历史记录</template>
      </el-menu-item>
      <el-menu-item index="/analytics">
        <el-icon><TrendCharts /></el-icon>
        <template #title>数据分析</template>
      </el-menu-item>
      <el-menu-item index="/diseases">
        <el-icon><Collection /></el-icon>
        <template #title>病害知识库</template>
      </el-menu-item>
      <el-menu-item index="/settings">
        <el-icon><Tools /></el-icon>
        <template #title>系统设置</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { 
  DataLine, 
  Aim, 
  Timer, 
  TrendCharts, 
  Collection, 
  Tools 
} from '@element-plus/icons-vue'

defineProps<{ collapsed: boolean }>()
const route = useRoute()
</script>

<style scoped>
.sidebar-container {
  height: 100%;
  padding-top: 16px;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
}

.logo-icon-wrapper {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 20px;
  font-weight: 800;
  color: #1f2937;
  letter-spacing: -0.5px;
  white-space: nowrap;
}

.glass-menu {
  background: transparent !important;
  border-right: none !important;
  padding: 0 12px;
  
  --el-menu-bg-color: transparent;
  --el-menu-text-color: #4b5563;
  --el-menu-active-color: #059669;
  --el-menu-hover-bg-color: transparent;
}

:deep(.el-menu-item) {
  border-radius: 12px;
  margin-bottom: 8px;
  height: 50px;
  transition: all 0.3s ease;
}

:deep(.el-menu-item:hover),
:deep(.el-menu-item.is-active) {
  background: rgba(16, 185, 129, 0.1) !important;
  color: #059669 !important;
  font-weight: 600;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
  box-shadow: 0 2px 12px rgba(16, 185, 129, 0.05);
}

:deep(.el-icon) {
  font-size: 20px;
  margin-right: 12px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>