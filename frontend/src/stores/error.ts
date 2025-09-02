import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { HttpError, ValidationError } from '@/types/api'

export interface AppError {
  id: string
  type: 'api' | 'validation' | 'file' | 'network' | 'system'
  severity: 'low' | 'medium' | 'high' | 'critical'
  title: string
  message: string
  details?: any
  timestamp: Date
  resolved: boolean
  actions?: ErrorAction[]
}

export interface ErrorAction {
  label: string
  action: () => void | Promise<void>
  variant?: 'primary' | 'secondary' | 'danger'
}

export const useErrorStore = defineStore('error', () => {
  // State
  const errors = ref<AppError[]>([])
  const currentError = ref<AppError | null>(null)
  const maxErrors = ref(50) // Limit stored errors to prevent memory issues

  // Computed
  const hasErrors = computed(() => errors.value.length > 0)
  const unresolvedErrors = computed(() => errors.value.filter(error => !error.resolved))
  const criticalErrors = computed(() => errors.value.filter(error => error.severity === 'critical'))
  const recentErrors = computed(() => 
    errors.value.slice(0, 10).sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
  )

  // Generate unique error ID
  const generateErrorId = (): string => {
    return `error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  // Add error
  const addError = (errorData: Omit<AppError, 'id' | 'timestamp' | 'resolved'>) => {
    const error: AppError = {
      ...errorData,
      id: generateErrorId(),
      timestamp: new Date(),
      resolved: false
    }

    errors.value.unshift(error)
    
    // Limit number of stored errors
    if (errors.value.length > maxErrors.value) {
      errors.value = errors.value.slice(0, maxErrors.value)
    }

    return error
  }

  // Handle HTTP errors
  const handleHttpError = (httpError: HttpError, context = '') => {
    const error = addError({
      type: 'api',
      severity: httpError.status >= 500 ? 'high' : 'medium',
      title: 'APIエラー',
      message: httpError.message || `HTTP ${httpError.status}: ${httpError.statusText}`,
      details: {
        status: httpError.status,
        statusText: httpError.statusText,
        data: httpError.data,
        context
      },
      actions: getHttpErrorActions(httpError)
    })

    return error
  }

  // Handle validation errors
  const handleValidationError = (validationError: ValidationError, context = '') => {
    const error = addError({
      type: 'validation',
      severity: 'medium',
      title: '入力エラー',
      message: validationError.message,
      details: {
        field: validationError.field,
        code: validationError.code,
        context
      }
    })

    return error
  }

  // Handle file errors
  const handleFileError = (message: string, filename?: string) => {
    const error = addError({
      type: 'file',
      severity: 'medium',
      title: 'ファイルエラー',
      message,
      details: { filename },
      actions: [
        {
          label: 'ファイルを再選択',
          action: () => {
            // This would typically trigger file selection
            const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
            fileInput?.click()
          }
        }
      ]
    })

    return error
  }

  // Handle network errors
  const handleNetworkError = (message = 'ネットワークに接続できません') => {
    const error = addError({
      type: 'network',
      severity: 'high',
      title: 'ネットワークエラー',
      message,
      actions: [
        {
          label: '再試行',
          action: async () => {
            // This would typically trigger a retry
            window.location.reload()
          },
          variant: 'primary'
        },
        {
          label: '接続状態を確認',
          action: () => {
            window.open('https://www.google.com', '_blank')
          },
          variant: 'secondary'
        }
      ]
    })

    return error
  }

  // Handle system errors
  const handleSystemError = (message: string, details?: any) => {
    const error = addError({
      type: 'system',
      severity: 'critical',
      title: 'システムエラー',
      message,
      details,
      actions: [
        {
          label: 'ページを再読み込み',
          action: () => window.location.reload(),
          variant: 'primary'
        },
        {
          label: 'サポートに連絡',
          action: () => {
            const subject = encodeURIComponent('システムエラーの報告')
            const body = encodeURIComponent(`エラーID: ${error.id}\nメッセージ: ${message}\n詳細: ${JSON.stringify(details, null, 2)}`)
            window.open(`mailto:support@example.com?subject=${subject}&body=${body}`)
          },
          variant: 'secondary'
        }
      ]
    })

    return error
  }

  // Get actions for HTTP errors
  const getHttpErrorActions = (httpError: HttpError): ErrorAction[] => {
    const actions: ErrorAction[] = []

    // Common retry action
    if (httpError.status >= 500 || httpError.status === 0) {
      actions.push({
        label: '再試行',
        action: () => {
          // This would typically trigger a retry of the failed request
          console.log('Retrying request...')
        },
        variant: 'primary'
      })
    }

    // Authentication errors
    if (httpError.status === 401) {
      actions.push({
        label: '再ログイン',
        action: () => {
          // Clear auth and redirect to login
          localStorage.removeItem('authToken')
          // window.location.href = '/login'
        },
        variant: 'primary'
      })
    }

    // Rate limiting
    if (httpError.status === 429) {
      actions.push({
        label: 'しばらく待つ',
        action: () => {
          setTimeout(() => {
            console.log('Rate limit cooldown complete')
          }, 60000) // Wait 1 minute
        }
      })
    }

    return actions
  }

  // Mark error as resolved
  const resolveError = (errorId: string) => {
    const error = errors.value.find(e => e.id === errorId)
    if (error) {
      error.resolved = true
    }
  }

  // Remove error
  const removeError = (errorId: string) => {
    const index = errors.value.findIndex(e => e.id === errorId)
    if (index > -1) {
      errors.value.splice(index, 1)
    }
  }

  // Clear resolved errors
  const clearResolvedErrors = () => {
    errors.value = errors.value.filter(error => !error.resolved)
  }

  // Clear all errors
  const clearAllErrors = () => {
    errors.value = []
    currentError.value = null
  }

  // Show error details
  const showError = (errorId: string) => {
    const error = errors.value.find(e => e.id === errorId)
    if (error) {
      currentError.value = error
    }
  }

  // Hide error details
  const hideError = () => {
    currentError.value = null
  }

  // Get errors by type
  const getErrorsByType = (type: AppError['type']) => {
    return errors.value.filter(error => error.type === type)
  }

  // Get errors by severity
  const getErrorsBySeverity = (severity: AppError['severity']) => {
    return errors.value.filter(error => error.severity === severity)
  }

  // Error statistics
  const getErrorStats = () => {
    const total = errors.value.length
    const resolved = errors.value.filter(e => e.resolved).length
    const byType = {
      api: errors.value.filter(e => e.type === 'api').length,
      validation: errors.value.filter(e => e.type === 'validation').length,
      file: errors.value.filter(e => e.type === 'file').length,
      network: errors.value.filter(e => e.type === 'network').length,
      system: errors.value.filter(e => e.type === 'system').length
    }
    const bySeverity = {
      low: errors.value.filter(e => e.severity === 'low').length,
      medium: errors.value.filter(e => e.severity === 'medium').length,
      high: errors.value.filter(e => e.severity === 'high').length,
      critical: errors.value.filter(e => e.severity === 'critical').length
    }

    return {
      total,
      resolved,
      unresolved: total - resolved,
      byType,
      bySeverity
    }
  }

  // Export error log
  const exportErrorLog = () => {
    const exportData = {
      timestamp: new Date().toISOString(),
      errors: errors.value.map(error => ({
        ...error,
        timestamp: error.timestamp.toISOString()
      })),
      statistics: getErrorStats()
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: 'application/json'
    })

    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `error-log-${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return {
    // State
    errors,
    currentError,
    maxErrors,

    // Computed
    hasErrors,
    unresolvedErrors,
    criticalErrors,
    recentErrors,

    // Actions
    addError,
    handleHttpError,
    handleValidationError,
    handleFileError,
    handleNetworkError,
    handleSystemError,
    resolveError,
    removeError,
    clearResolvedErrors,
    clearAllErrors,
    showError,
    hideError,
    getErrorsByType,
    getErrorsBySeverity,
    getErrorStats,
    exportErrorLog
  }
})