/**
 * 用户Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface User {
  id: number
  username: string
  role: 'admin' | 'annotator' | 'viewer'
  created_at: string
}

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)

  const setCurrentUser = (user: User | null) => {
    currentUser.value = user
  }

  return {
    currentUser,
    setCurrentUser
  }
})
