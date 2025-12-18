<template>
  <div class="sidebar-container">
    <div class="logo">
      <span v-if="!collapsed">🌱 CropVision-AI</span>
      <span v-else>🌱</span>
    </div>
    <el-menu
      :default-active="route.path"
      :collapse="collapsed"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409eff"
      router
    >
      <el-menu-item index="/">
        <el-icon><DataBoard /></el-icon>
        <template #title>工作台</template>
      </el-menu-item>
      <el-menu-item index="/predict">
        <el-icon><Camera /></el-icon>
        <template #title>智能识别</template>
      </el-menu-item>
      <el-menu-item index="/history">
        <el-icon><Clock /></el-icon>
        <template #title>历史记录</template>
      </el-menu-item>
      <el-menu-item index="/analytics">
        <el-icon><PieChart /></el-icon>
        <template #title>数据分析</template>
      </el-menu-item>
      <el-menu-item index="/diseases">
        <el-icon><Reading /></el-icon>
        <template #title>病害知识库</template>
      </el-menu-item>
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <template #title>系统设置</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { DataBoard, Camera, Clock, PieChart, Reading, Setting } from '@element-plus/icons-vue'

defineProps<{ collapsed: boolean }>()
const route = useRoute()
</script>

<style scoped lang="scss">
.sidebar-container {
  height: 100%;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #3d4a5a;
}
.el-menu {
  border-right: none;
}
</style>