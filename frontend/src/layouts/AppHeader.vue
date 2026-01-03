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
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="route.name !== 'Dashboard'">{{ routeTitle }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="right">
      <el-button circle plain text>
        <el-icon><Bell /></el-icon>
      </el-button>
      
      <el-dropdown trigger="click" @command="handleCommand">
        <div class="user-profile">
          <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
          <span class="username">{{ authStore.user?.username || 'User' }}</span>
          <el-icon class="el-icon--right"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
            <el-dropdown-item command="settings">系统设置</el-dropdown-item>
            <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Fold, Expand, Bell, ArrowDown } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

defineProps<{ isCollapsed?: boolean }>()
defineEmits(['toggle-sidebar'])
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const routeTitles: Record<string, string> = {
  Predict: '智能识别',
  History: '历史记录',
  Analytics: '数据分析',
  Diseases: '病害知识库',
  DiseaseDetail: '病害详情',
  Settings: '系统设置',
  Dashboard: '工作台'
}
const routeTitle = computed(() => routeTitles[route.name as string] || '')

const handleCommand = (command: string) => {
  if (command === 'logout') {
    authStore.logout()
    ElMessage.success('已退出登录')
  } else if (command === 'settings') {
    router.push('/settings')
  }
}
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
  gap: 8px;
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
