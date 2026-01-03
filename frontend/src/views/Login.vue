<template>
  <div class="login-container">
    <div class="circles">
      <div class="circle c1"></div>
      <div class="circle c2"></div>
    </div>
    
    <GlassCard class="login-card" v-motion-pop-visible>
      <div class="logo-area">
        <div class="logo-icon">🌱</div>
        <h2>欢迎回来</h2>
        <p class="subtitle">智能作物病害识别系统</p>
      </div>
      
      <el-form 
        ref="formRef"
        :model="form"
        :rules="rules"
        class="login-form"
        label-position="top"
        size="large"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="用户名" 
            :prefix-icon="User"
            class="glass-input"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="密码" 
            :prefix-icon="Lock"
            show-password
            class="glass-input"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-button 
          type="primary" 
          class="login-btn" 
          :loading="loading"
          @click="handleLogin"
        >
          登 录
        </el-button>
      </el-form>
      
      <div class="footer">
        <span>测试账号: admin / 123456</span>
      </div>
    </GlassCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import GlassCard from '@/components/GlassCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (form.password === '123456') {
        loading.value = true
        await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API
        authStore.login(form.username)
        ElMessage.success('登录成功')
        router.push('/')
      } else {
        ElMessage.error('密码错误 (提示: 123456)')
      }
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
  position: relative;
  overflow: hidden;
}

.circles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.c1 {
  width: 400px;
  height: 400px;
  background: rgba(16, 185, 129, 0.4);
  top: -100px;
  right: -100px;
  animation: float 10s ease-in-out infinite;
}

.c2 {
  width: 300px;
  height: 300px;
  background: rgba(59, 130, 246, 0.3);
  bottom: -50px;
  left: -50px;
  animation: float 15s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(30px); }
}

.login-card {
  width: 400px;
  padding: 40px !important;
  z-index: 10;
}

.logo-area {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: inline-block;
  animation: bounce 2s infinite;
}

.logo-area h2 {
  font-size: 28px;
  color: #1f2937;
  margin-bottom: 8px;
}

.subtitle {
  color: #6b7280;
  font-size: 14px;
}

:deep(.glass-input .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(4px);
  border-radius: 12px;
  box-shadow: none !important;
  border: 1px solid rgba(255, 255, 255, 0.8);
  padding: 4px 12px;
}

:deep(.glass-input .el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.9);
  border-color: #10b981;
}

.login-btn {
  width: 100%;
  height: 48px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  margin-top: 24px;
}

.footer {
  text-align: center;
  margin-top: 24px;
  color: #9ca3af;
  font-size: 12px;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
