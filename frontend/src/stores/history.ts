import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import type { ClassificationHistory, ClassificationStats } from '@/types/api'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const useHistoryStore = defineStore('history', () => {
  // State
  const history = ref<ClassificationHistory[]>([])
  const stats = ref<ClassificationStats | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const totalRecords = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(20)

  // Computed
  const hasHistory = computed(() => history.value.length > 0)
  const totalPages = computed(() => Math.ceil(totalRecords.value / pageSize.value))
  
  const recentHistory = computed(() => {
    return history.value.slice(0, 5)
  })

  const monthlyHistory = computed(() => {
    const now = new Date()
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
    return history.value.filter(item => {
      const itemDate = new Date(item.created_at)
      return itemDate >= startOfMonth
    })
  })

  // Actions
  const fetchHistory = async (
    page: number = 1, 
    limit: number = 20,
    filters?: {
      model_name?: string
      date_from?: Date
      date_to?: Date
    }
  ) => {
    isLoading.value = true
    error.value = null
    
    try {
      const params: any = {
        skip: (page - 1) * limit,
        limit
      }
      
      if (filters?.model_name) {
        params.model_name = filters.model_name
      }
      
      if (filters?.date_from) {
        params.date_from = filters.date_from.toISOString()
      }
      
      if (filters?.date_to) {
        params.date_to = filters.date_to.toISOString()
      }
      
      const response = await axios.get(`${API_BASE_URL}/api/v1/history`, { params })
      
      history.value = response.data.items
      totalRecords.value = response.data.total
      currentPage.value = page
      pageSize.value = limit
      
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch history'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchStats = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await axios.get<ClassificationStats>(`${API_BASE_URL}/api/v1/stats`)
      stats.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch statistics'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getHistoryItem = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await axios.get<ClassificationHistory>(
        `${API_BASE_URL}/api/v1/history/${id}`
      )
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch history item'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteHistoryItem = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      await axios.delete(`${API_BASE_URL}/api/v1/history/${id}`)
      
      // Remove from local state
      history.value = history.value.filter(item => item.id !== id)
      totalRecords.value--
      
      // Refresh history if needed
      if (history.value.length === 0 && currentPage.value > 1) {
        await fetchHistory(currentPage.value - 1, pageSize.value)
      }
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete history item'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const bulkDeleteHistory = async (ids: number[]) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/history/bulk-delete`, {
        record_ids: ids
      })
      
      // Remove from local state
      history.value = history.value.filter(item => !ids.includes(item.id))
      totalRecords.value -= ids.length
      
      // Refresh history if needed
      if (history.value.length === 0 && currentPage.value > 1) {
        await fetchHistory(currentPage.value - 1, pageSize.value)
      }
      
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete history items'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const clearHistory = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const allIds = history.value.map(item => item.id)
      await bulkDeleteHistory(allIds)
      
      history.value = []
      totalRecords.value = 0
      currentPage.value = 1
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to clear history'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const exportHistory = async (format: 'json' | 'csv' | 'pdf' = 'json') => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/history/export`, {
        params: { format },
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `classification_history.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to export history'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const refreshHistory = async () => {
    await fetchHistory(currentPage.value, pageSize.value)
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    history,
    stats,
    isLoading,
    error,
    totalRecords,
    currentPage,
    pageSize,
    
    // Computed
    hasHistory,
    totalPages,
    recentHistory,
    monthlyHistory,
    
    // Actions
    fetchHistory,
    fetchStats,
    getHistoryItem,
    deleteHistoryItem,
    bulkDeleteHistory,
    clearHistory,
    exportHistory,
    refreshHistory,
    clearError
  }
})