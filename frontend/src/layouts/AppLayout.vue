<template>
  <el-container class="app-layout">
    <el-aside :width="isCollapsed ? '64px' : '260px'" class="sidebar-wrapper">
      <AppSidebar :collapsed="isCollapsed" />
    </el-aside>
    <el-container>
      <el-header class="header-wrapper">
        <AppHeader @toggle-sidebar="isCollapsed = !isCollapsed" />
      </el-header>
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-scale" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
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

<style scoped>
.app-layout {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: transparent;
}

.sidebar-wrapper {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-right: 1px solid rgba(255, 255, 255, 0.6);
  transition: width 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: 10;
}

.header-wrapper {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.01);
  padding: 0;
  height: 64px;
}

.main-content {
  padding: 32px;
  overflow-y: auto;
  position: relative;
}

/* Transition Animations */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-scale-enter-from {
  opacity: 0;
  transform: scale(0.98) translateY(10px);
}

.fade-scale-leave-to {
  opacity: 0;
  transform: scale(1.02);
}
</style>