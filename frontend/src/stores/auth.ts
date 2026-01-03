import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
    const user = ref<{ username: string; role: string } | null>(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null)
    const isAuthenticated = ref(!!user.value)
    const router = useRouter()

    function login(username: string) {
        // Mock login logic
        const mockUser = { username, role: 'admin' }
        user.value = mockUser
        isAuthenticated.value = true
        localStorage.setItem('user', JSON.stringify(mockUser))
    }

    function logout() {
        user.value = null
        isAuthenticated.value = false
        localStorage.removeItem('user')
        router.push('/login')
    }

    return { user, isAuthenticated, login, logout }
})
