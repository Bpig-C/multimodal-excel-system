import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginRequest } from '@/types'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)

  // Actions
  const login = async (username: string, password: string) => {
    const loginData: LoginRequest = { username, password }
    const response = await authApi.login(loginData)
    
    token.value = response.access_token
    user.value = response.user
    
    // 保存到localStorage
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))
  }

  const logout = () => {
    token.value = null
    user.value = null
    
    // 清除localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const loadUserFromStorage = () => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }

  const getAuthHeader = () => {
    return token.value ? { Authorization: `Bearer ${token.value}` } : {}
  }

  // 初始化时加载用户信息
  loadUserFromStorage()

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    loadUserFromStorage,
    getAuthHeader
  }
})
