<template>
  <div class="header-container">
    <div class="left">
      <el-icon 
        class="toggle-btn" 
        @click="$emit('toggle-sidebar')"
      >
        <component :is="isCollapsed ? Expand : Fold" />
      </el-icon>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item v-if="route.name !== 'Dashboard'">{{ routeTitle }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="right">
      <el-button circle plain text>
        <el-icon><Bell /></el-icon>
      </el-button>
      <div class="user-profile">
        <el-avatar :size="36" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
        <span class="username">Admin</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Fold, Expand, Bell } from '@element-plus/icons-vue'

defineProps<{ isCollapsed?: boolean }>()
defineEmits(['toggle-sidebar'])
const route = useRoute()

const routeTitles: Record<string, string> = {
  Predict: 'New Scan',
  History: 'History',
  Analytics: 'Analytics',
  Diseases: 'Knowledge Base',
  DiseaseDetail: 'Disease Detail',
  Settings: 'Settings',
  Dashboard: 'Dashboard'
}
const routeTitle = computed(() => routeTitles[route.name as string] || '')
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 0 12px;
}
.left {
  display: flex;
  align-items: center;
  gap: 24px;
}
.toggle-btn {
  font-size: 22px;
  cursor: pointer;
  color: #4b5563;
  transition: color 0.3s;
}
.toggle-btn:hover {
  color: #10b981;
}
.right {
  display: flex;
  align-items: center;
  gap: 20px;
}
.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background 0.3s;
}
.user-profile:hover {
  background: rgba(255, 255, 255, 0.8);
}
.username {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}
:deep(.el-breadcrumb__inner) {
  color: #6b7280;
  font-weight: 500;
}
:deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: #10b981;
}
</style>