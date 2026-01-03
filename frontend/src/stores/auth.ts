import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// Create an axios instance with base URL
const api = axios.create({
    baseURL: 'http://localhost:8000'
})

export const useAuthStore = defineStore('auth', () => {
    const user = ref<{ username: string; role: string } | null>(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null)
    const token = ref<string | null>(localStorage.getItem('token'))
    const isAuthenticated = ref(!!token.value)
    const router = useRouter()

    async function login(username: string, password: string): Promise<boolean> {
        try {
            const formData = new FormData()
            formData.append('username', username)
            formData.append('password', password)

            const response = await api.post('/api/auth/token', formData)
            const { access_token } = response.data

            const userInfo = { username, role: 'user' }
            user.value = userInfo
            token.value = access_token
            isAuthenticated.value = true

            localStorage.setItem('user', JSON.stringify(userInfo))
            localStorage.setItem('token', access_token)

            return true
        } catch (error) {
            console.error('Login failed:', error)
            return false
        }
    }

    function logout() {
        user.value = null
        token.value = null
        isAuthenticated.value = false
        localStorage.removeItem('user')
        localStorage.removeItem('token')
        router.push('/login')
    }

    return { user, token, isAuthenticated, login, logout }
})
