<template>
  <div class="login-container">
    <div class="circles">
      <div class="circle c1"></div>
      <div class="circle c2"></div>
    </div>
    
    <GlassCard class="login-card" v-motion-pop-visible>
      <div class="logo-area">
        <div class="logo-icon">🌱</div>
        <h2>注册账户</h2>
        <p class="subtitle">加入智能作物病害识别系统</p>
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
          />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="form.confirmPassword" 
            type="password" 
            placeholder="确认密码" 
            :prefix-icon="Lock"
            show-password
            class="glass-input"
          />
        </el-form-item>
        
        <el-button 
          type="primary" 
          class="login-btn" 
          :loading="loading"
          @click="handleRegister"
        >
          注 册
        </el-button>
        
        <div class="register-link">
          已有账号？ <router-link to="/login">立即登录</router-link>
        </div>
      </el-form>
      
    </GlassCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import GlassCard from '@/components/GlassCard.vue'
import axios from 'axios'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

const validatePass2 = (_: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度不能小于 3 位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于 6 位', trigger: 'blur' }
  ],
  confirmPassword: [
    { validator: validatePass2, trigger: 'blur' }
  ]
})

const handleRegister = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await axios.post('http://localhost:8000/api/auth/register', {
          username: form.username,
          password: form.password,
          email: null // Optional
        })
        ElMessage.success('注册成功，请登录')
        router.push('/login')
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '注册失败，请稍后重试')
      } finally {
        loading.value = false
      }
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
  background: var(--bg-gradient);
  position: relative;
  overflow: hidden;
}

.circles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
}

.c1 {
  width: 400px;
  height: 400px;
  background: #34d399;
  top: -100px;
  left: -100px;
}

.c2 {
  width: 300px;
  height: 300px;
  background: #60a5fa;
  bottom: -50px;
  right: -50px;
}

.login-card {
  width: 400px;
  padding: 40px 32px !important;
  z-index: 1;
}

.logo-area {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: inline-block;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.logo-area h2 {
  font-size: 24px;
  color: var(--text-main);
  margin-bottom: 8px;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

.login-form {
  margin-top: 24px;
}

.glass-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.4);
  box-shadow: none;
  border: 1px solid rgba(255, 255, 255, 0.6);
  padding: 8px 12px;
}

.glass-input :deep(.el-input__inner) {
  color: var(--text-main);
}

.login-btn {
  width: 100%;
  margin-top: 24px;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.register-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: var(--text-secondary);
}

.register-link a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
