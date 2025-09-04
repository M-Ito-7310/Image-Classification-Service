import { apiService, dispatchApiError, dispatchLoading } from './api'
import i18n from '@/i18n'
import type {
  ClassificationResult,
  ModelsResponse,
  HealthCheck,
  UploadOptions,
  ApiResponse,
  HttpError,
  ClassificationHistory,
  HistoryResponse
} from '@/types/api'

/**
 * Image Classification API Service
 */
class ClassificationApiService {
  // Health Check
  async checkHealth(): Promise<HealthCheck> {
    try {
      const response = await apiService.get<HealthCheck>('/api/v1/health')
      return response
    } catch (error) {
      const httpError = error as HttpError
      dispatchApiError(httpError)
      throw error
    }
  }

  // Get available models
  async getModels(): Promise<ModelsResponse> {
    try {
      dispatchLoading(true, 'モデル情報を取得中...')
      const response = await apiService.get<ModelsResponse>('/api/v1/models')
      return response
    } catch (error) {
      const httpError = error as HttpError
      dispatchApiError(httpError)
      throw error
    } finally {
      dispatchLoading(false)
    }
  }

  // Get specific model info
  async getModel(modelName: string): Promise<any> {
    try {
      const response = await apiService.get(`/api/v1/models/${modelName}`)
      return response
    } catch (error) {
      const httpError = error as HttpError
      dispatchApiError(httpError)
      throw error
    }
  }

  // Classify single image
  async classifyImage(
    file: File,
    options: UploadOptions = {},
    onProgress?: (progress: number) => void
  ): Promise<ClassificationResult> {
    try {
      // Validate file
      this.validateImageFile(file)
      
      dispatchLoading(true, '画像を分析中...')
      
      const uploadOptions = {
        model: options.model || 'default',
        threshold: options.threshold || 0.5,
        max_results: options.max_results || 5,
        enhance_image: options.enhance_image || false,
        language: options.language || i18n.global.locale.value as 'ja' | 'en',
      }

      const response = await apiService.uploadFile<ClassificationResult>(
        '/api/v1/classify',
        file,
        uploadOptions,
        onProgress
      )

      // Dispatch success toast
      window.dispatchEvent(new CustomEvent('app:toast', {
        detail: {
          type: 'success',
          title: '分類完了',
          message: `${response.predictions.length}個の予測結果を取得しました`
        }
      }))

      return response
    } catch (error) {
      const httpError = error as HttpError
      
      // Enhanced error messages for classification
      if (httpError.status === 400) {
        httpError.message = '画像ファイルの形式が無効です。JPEG、PNG、WebP、BMPファイルを選択してください。'
      } else if (httpError.status === 413) {
        httpError.message = 'ファイルサイズが大きすぎます。10MB以下のファイルを選択してください。'
      } else if (httpError.status === 422) {
        httpError.message = '画像の処理中にエラーが発生しました。別の画像をお試しください。'
      } else if (httpError.status === 500) {
        httpError.message = 'サーバーエラーが発生しました。しばらく時間をおいて再試行してください。'
      }
      
      dispatchApiError(httpError)
      throw error
    } finally {
      dispatchLoading(false)
    }
  }


  // Get classification history (for future implementation)
  async getHistory(limit = 20, offset = 0): Promise<HistoryResponse> {
    try {
      const response = await apiService.get<HistoryResponse>(`/api/v1/history?limit=${limit}&offset=${offset}`)
      return response
    } catch (error) {
      const httpError = error as HttpError
      dispatchApiError(httpError)
      throw error
    }
  }

  // Get specific classification result (for future implementation)
  async getHistoryItem(id: string): Promise<ClassificationHistory> {
    try {
      const response = await apiService.get<ClassificationHistory>(`/api/v1/history/${id}`)
      return response
    } catch (error) {
      const httpError = error as HttpError
      dispatchApiError(httpError)
      throw error
    }
  }

  // Delete classification from history (for future implementation)
  async deleteHistoryItem(id: string): Promise<void> {
    try {
      await apiService.delete(`/api/v1/history/${id}`)
      
      window.dispatchEvent(new CustomEvent('app:toast', {
        detail: {
          type: 'success',
          title: '削除完了',
          message: '分類履歴を削除しました'
        }
      }))
    } catch (error) {
      const httpError = error as HttpError
      dispatchApiError(httpError)
      throw error
    }
  }

  // Export classification results
  async exportResults(results: ClassificationResult[], format: 'json' | 'csv' = 'json'): Promise<Blob> {
    try {
      const response = await apiService.post('/api/v1/export', {
        results,
        format
      }, {
        responseType: 'blob'
      })
      
      return new Blob([response as any], {
        type: format === 'json' ? 'application/json' : 'text/csv'
      })
    } catch (error) {
      const httpError = error as HttpError
      dispatchApiError(httpError)
      throw error
    }
  }

  // Validate image file
  private validateImageFile(file: File): void {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/bmp']
    const maxSize = 10 * 1024 * 1024 // 10MB

    if (!allowedTypes.includes(file.type)) {
      throw new Error(`サポートされていないファイル形式です: ${file.type}`)
    }

    if (file.size > maxSize) {
      throw new Error(`ファイルサイズが大きすぎます: ${(file.size / 1024 / 1024).toFixed(2)}MB`)
    }

    if (file.size === 0) {
      throw new Error('空のファイルは処理できません')
    }
  }

  // Get supported file types
  getSupportedFileTypes(): string[] {
    return ['.jpg', '.jpeg', '.png', '.webp', '.bmp']
  }

  // Get max file size
  getMaxFileSize(): number {
    return 10 * 1024 * 1024 // 10MB
  }

  // Format file size for display
  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  // Generate download filename
  generateExportFilename(format: 'json' | 'csv'): string {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    return `classification-results-${timestamp}.${format}`
  }
}

// Export singleton instance
export const classificationApi = new ClassificationApiService()
export default classificationApi