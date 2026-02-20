import { ref, computed } from 'vue'

export const useAuth = () => {
  const token = ref<string | null>(null)
  const user = ref<any>(null)

  if (process.client) {
    token.value = localStorage.getItem('auth_token')
  }

  const isAuthenticated = computed(() => !!token.value)

  const login = async (email: string, password: string) => {
    try {
      const config = useRuntimeConfig()
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)

      const response = await $fetch<{ access_token: string; token_type: string }>(
        `${config.public.apiBase}/api/auth/login`,
        {
          method: 'POST',
          body: formData
        }
      )

      token.value = response.access_token
      if (process.client) {
        localStorage.setItem('auth_token', response.access_token)
      }

      // Get user info
      await fetchUser()
      
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message || 'Ошибка входа' }
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    if (process.client) {
      localStorage.removeItem('auth_token')
    }
    navigateTo('/login')
  }

  const fetchUser = async () => {
    if (!token.value) return

    try {
      const config = useRuntimeConfig()
      const response = await $fetch(`${config.public.apiBase}/api/auth/me`, {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })
      user.value = response
    } catch (error) {
      logout()
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    fetchUser
  }
}

