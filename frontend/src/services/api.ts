import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import type { ApiResponse, HttpError } from '@/types/api'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_TIMEOUT = 30000 // 30 seconds

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add authentication token if available
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Add request timestamp for debugging
    ;(config as any).metadata = { startTime: Date.now() }
    
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Calculate request duration
    const duration = Date.now() - ((response.config as any).metadata?.startTime || 0)
    console.log(`[API] ${response.status} ${response.config.url} (${duration}ms)`)
    
    return response
  },
  (error: AxiosError) => {
    const duration = Date.now() - ((error.config as any)?.metadata?.startTime || 0)
    console.error(`[API] ${error.response?.status || 'Network Error'} ${error.config?.url} (${duration}ms)`, error)
    
    // Transform axios error to our HttpError type
    const httpError: HttpError = new Error(error.message) as HttpError
    httpError.status = error.response?.status || 0
    httpError.statusText = error.response?.statusText || 'Network Error'
    httpError.data = error.response?.data
    
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Unauthorized - remove token and redirect to login
      localStorage.removeItem('authToken')
      // window.location.href = '/login' // Uncomment when auth is implemented
    } else if (error.response?.status === 413) {
      // Payload too large
      httpError.message = 'ファイルサイズが大きすぎます。10MB以下のファイルを選択してください。'
    } else if (error.response?.status === 429) {
      // Too many requests
      httpError.message = 'リクエストが多すぎます。しばらくお待ちください。'
    } else if (!error.response) {
      // Network error
      httpError.message = 'ネットワークエラーが発生しました。接続を確認してください。'
    }
    
    return Promise.reject(httpError)
  }
)

// API Helper Functions
class ApiService {
  private client: AxiosInstance

  constructor() {
    this.client = apiClient
  }

  // Generic GET request
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.get<T>(url, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  // Generic POST request
  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.post<T>(url, data, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  // File upload with progress
  async uploadFile<T>(
    url: string,
    file: File,
    options: Record<string, any> = {},
    onProgress?: (progress: number) => void
  ): Promise<T> {
    const formData = new FormData()
    formData.append('file', file)
    
    // Add additional options as form fields
    Object.entries(options).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        formData.append(key, value.toString())
      }
    })

    try {
      const response = await this.client.post<T>(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total && onProgress) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            onProgress(progress)
          }
        },
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  // Multiple file upload
  async uploadFiles<T>(
    url: string,
    files: File[],
    options: Record<string, any> = {},
    onProgress?: (progress: number) => void
  ): Promise<T> {
    const formData = new FormData()
    
    files.forEach((file, index) => {
      formData.append(`files`, file)
    })
    
    // Add additional options
    Object.entries(options).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        formData.append(key, value.toString())
      }
    })

    try {
      const response = await this.client.post<T>(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total && onProgress) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            onProgress(progress)
          }
        },
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  // Generic PUT request
  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.put<T>(url, data, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  // Generic DELETE request
  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.client.delete<T>(url, config)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  // Error handler
  private handleError(error: any): HttpError {
    if (error instanceof Error && 'status' in error) {
      return error as HttpError
    }
    
    // Fallback error
    const httpError: HttpError = new Error('An unexpected error occurred') as HttpError
    httpError.status = 500
    httpError.statusText = 'Internal Server Error'
    return httpError
  }

  // Health check with timeout
  async healthCheck(timeout = 5000): Promise<boolean> {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), timeout)
      
      await this.client.get('/api/v1/health', {
        signal: controller.signal,
      })
      
      clearTimeout(timeoutId)
      return true
    } catch (error) {
      return false
    }
  }

  // Get base URL
  getBaseUrl(): string {
    return API_BASE_URL
  }

  // Set auth token
  setAuthToken(token: string): void {
    localStorage.setItem('authToken', token)
    this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }

  // Clear auth token
  clearAuthToken(): void {
    localStorage.removeItem('authToken')
    delete this.client.defaults.headers.common['Authorization']
  }
}

// Export singleton instance
export const apiService = new ApiService()
export default apiService

// Global error event dispatcher
export const dispatchApiError = (error: HttpError) => {
  window.dispatchEvent(new CustomEvent('app:toast', {
    detail: {
      type: 'error',
      title: 'APIエラー',
      message: error.message
    }
  }))
}

// Global loading event dispatcher
export const dispatchLoading = (show: boolean, message = '') => {
  window.dispatchEvent(new CustomEvent('app:loading', {
    detail: { show, message }
  }))
}