<template>
  <el-container class="app-layout">
    <el-aside :width="isCollapsed ? '64px' : '220px'" class="sidebar">
      <AppSidebar :collapsed="isCollapsed" />
    </el-aside>
    <el-container>
      <el-header class="header">
        <AppHeader @toggle-sidebar="isCollapsed = !isCollapsed" />
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'

const isCollapsed = ref(false)
</script>

<style scoped lang="scss">
.app-layout {
  height: 100vh;
}
.sidebar {
  background: #304156;
  transition: width 0.3s;
}
.header {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 16px;
  display: flex;
  align-items: center;
}
.main {
  background: #f5f7fa;
  padding: 24px;
}
</style>