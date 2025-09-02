import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import type { 
  User, 
  UserLogin, 
  UserRegister, 
  Token, 
  AuthResponse, 
  UserSession,
  ApiResponse 
} from '@/types/api'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<Token | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const isInitialized = ref(false)

  // Computed
  const isAuthenticated = computed(() => user.value !== null && token.value !== null)
  const isAdmin = computed(() => user.value?.is_admin || false)
  const hasValidToken = computed(() => {
    if (!token.value) return false
    
    try {
      const payload = JSON.parse(atob(token.value.access_token.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      return payload.exp > currentTime
    } catch {
      return false
    }
  })

  // Local Storage Keys
  const TOKEN_KEY = 'auth_token'
  const USER_KEY = 'auth_user'

  // Actions
  const setError = (message: string | null) => {
    error.value = message
  }

  const clearError = () => {
    error.value = null
  }

  const setLoading = (loading: boolean) => {
    isLoading.value = loading
  }

  const saveToStorage = () => {
    if (token.value) {
      localStorage.setItem(TOKEN_KEY, JSON.stringify(token.value))
    }
    if (user.value) {
      localStorage.setItem(USER_KEY, JSON.stringify(user.value))
    }
  }

  const loadFromStorage = () => {
    try {
      const storedToken = localStorage.getItem(TOKEN_KEY)
      const storedUser = localStorage.getItem(USER_KEY)
      
      if (storedToken) {
        token.value = JSON.parse(storedToken)
      }
      
      if (storedUser) {
        user.value = JSON.parse(storedUser)
      }
    } catch (error) {
      console.error('Error loading auth data from storage:', error)
      clearStorage()
    }
  }

  const clearStorage = () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  }

  const setAuthData = (authData: AuthResponse) => {
    user.value = authData.user
    token.value = authData.token
    saveToStorage()
    setupAxiosInterceptors()
    clearError()
  }

  const clearAuthData = () => {
    user.value = null
    token.value = null
    clearStorage()
    removeAxiosInterceptors()
  }

  // API Configuration
  const setupAxiosInterceptors = () => {
    if (!token.value) return

    // Request interceptor - add auth header
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value.access_token}`
    
    // Response interceptor - handle token refresh
    axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401 && token.value?.refresh_token) {
          try {
            await refreshToken()
            // Retry the original request
            const originalRequest = error.config
            originalRequest.headers['Authorization'] = `Bearer ${token.value?.access_token}`
            return axios.request(originalRequest)
          } catch (refreshError) {
            await logout()
            return Promise.reject(refreshError)
          }
        }
        return Promise.reject(error)
      }
    )
  }

  const removeAxiosInterceptors = () => {
    delete axios.defaults.headers.common['Authorization']
    axios.interceptors.response.clear()
  }

  const register = async (userData: UserRegister): Promise<AuthResponse> => {
    setLoading(true)
    clearError()
    
    try {
      const response = await axios.post<AuthResponse>(
        `${API_BASE_URL}/api/v1/auth/register`,
        userData
      )
      
      setAuthData(response.data)
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Registration failed'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials: UserLogin): Promise<AuthResponse> => {
    setLoading(true)
    clearError()
    
    try {
      const formData = new FormData()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)
      
      const response = await axios.post<AuthResponse>(
        `${API_BASE_URL}/api/v1/auth/login`,
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      )
      
      setAuthData(response.data)
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Login failed'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  const logout = async (): Promise<void> => {
    setLoading(true)
    
    try {
      if (token.value?.refresh_token) {
        await axios.post(`${API_BASE_URL}/api/v1/auth/logout`, {
          refresh_token: token.value.refresh_token
        })
      }
    } catch (error) {
      console.error('Logout request failed:', error)
    } finally {
      clearAuthData()
      setLoading(false)
    }
  }

  const refreshToken = async (): Promise<Token> => {
    if (!token.value?.refresh_token) {
      throw new Error('No refresh token available')
    }
    
    try {
      const response = await axios.post<Token>(
        `${API_BASE_URL}/api/v1/auth/refresh`,
        {
          refresh_token: token.value.refresh_token
        }
      )
      
      token.value = response.data
      saveToStorage()
      setupAxiosInterceptors()
      
      return response.data
    } catch (error: any) {
      clearAuthData()
      throw new Error('Token refresh failed')
    }
  }

  const updateProfile = async (profileData: Partial<User>): Promise<User> => {
    setLoading(true)
    clearError()
    
    try {
      const response = await axios.put<User>(
        `${API_BASE_URL}/api/v1/auth/me`,
        profileData
      )
      
      user.value = response.data
      saveToStorage()
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Profile update failed'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  const changePassword = async (currentPassword: string, newPassword: string): Promise<void> => {
    setLoading(true)
    clearError()
    
    try {
      await axios.post(`${API_BASE_URL}/api/v1/auth/change-password`, {
        current_password: currentPassword,
        new_password: newPassword
      })
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Password change failed'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  const getCurrentUser = async (): Promise<User> => {
    try {
      const response = await axios.get<User>(`${API_BASE_URL}/api/v1/auth/me`)
      user.value = response.data
      saveToStorage()
      return response.data
    } catch (error: any) {
      clearAuthData()
      throw new Error('Failed to get current user')
    }
  }

  const getUserSessions = async (): Promise<UserSession[]> => {
    try {
      const response = await axios.get<UserSession[]>(`${API_BASE_URL}/api/v1/auth/sessions`)
      return response.data
    } catch (error: any) {
      throw new Error('Failed to get user sessions')
    }
  }

  const revokeSession = async (sessionId: number): Promise<void> => {
    try {
      await axios.delete(`${API_BASE_URL}/api/v1/auth/sessions/${sessionId}`)
    } catch (error: any) {
      throw new Error('Failed to revoke session')
    }
  }

  // Initialize auth state
  const initialize = async () => {
    if (isInitialized.value) return

    loadFromStorage()
    
    if (token.value && hasValidToken.value) {
      setupAxiosInterceptors()
      
      // Verify token is still valid by fetching current user
      try {
        await getCurrentUser()
      } catch (error) {
        clearAuthData()
      }
    } else {
      clearAuthData()
    }
    
    isInitialized.value = true
  }

  // Auto-refresh token before expiry
  const startTokenRefreshTimer = () => {
    if (!token.value) return

    try {
      const payload = JSON.parse(atob(token.value.access_token.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      const timeUntilExpiry = payload.exp - currentTime
      
      // Refresh token 5 minutes before expiry
      const refreshTime = Math.max(0, timeUntilExpiry - 300) * 1000
      
      setTimeout(async () => {
        if (isAuthenticated.value && token.value?.refresh_token) {
          try {
            await refreshToken()
            startTokenRefreshTimer() // Schedule next refresh
          } catch (error) {
            await logout()
          }
        }
      }, refreshTime)
    } catch (error) {
      console.error('Error parsing token for refresh timer:', error)
    }
  }

  // Format user display name
  const getDisplayName = (userObj?: User): string => {
    const targetUser = userObj || user.value
    if (!targetUser) return ''
    
    return targetUser.full_name || targetUser.username || targetUser.email
  }

  return {
    // State
    user,
    token,
    isLoading,
    error,
    isInitialized,

    // Computed
    isAuthenticated,
    isAdmin,
    hasValidToken,

    // Actions
    register,
    login,
    logout,
    refreshToken,
    updateProfile,
    changePassword,
    getCurrentUser,
    getUserSessions,
    revokeSession,
    initialize,
    startTokenRefreshTimer,
    setError,
    clearError,
    getDisplayName
  }
})