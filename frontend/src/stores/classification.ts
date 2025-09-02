import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ClassificationResult, ModelInfo, ClassificationHistory } from '@/types/api'

export const useClassificationStore = defineStore('classification', () => {
  // State
  const availableModels = ref<ModelInfo[]>([])
  const selectedModel = ref<string>('default')
  const currentResults = ref<ClassificationResult[]>([])
  const history = ref<ClassificationHistory[]>([])
  const isProcessing = ref(false)
  const processingMessage = ref('')
  const lastProcessingTime = ref(0)
  const confidenceThreshold = ref(0.5)
  const maxResults = ref(5)

  // Computed
  const hasResults = computed(() => currentResults.value.length > 0)
  const hasHistory = computed(() => history.value.length > 0)
  const activeModel = computed(() => 
    availableModels.value.find(model => model.name === selectedModel.value)
  )
  const totalPredictions = computed(() => 
    currentResults.value.reduce((total, result) => total + result.predictions.length, 0)
  )
  const averageProcessingTime = computed(() => {
    if (currentResults.value.length === 0) return 0
    const totalTime = currentResults.value.reduce((sum, result) => sum + result.processing_time, 0)
    return totalTime / currentResults.value.length
  })

  // Model management
  const setAvailableModels = (models: ModelInfo[]) => {
    availableModels.value = models
    
    // Auto-select default model if available
    if (models.length > 0 && !selectedModel.value) {
      const defaultModel = models.find(m => m.name === 'default') || models[0]
      selectedModel.value = defaultModel.name
    }
  }

  const selectModel = (modelName: string) => {
    const model = availableModels.value.find(m => m.name === modelName)
    if (model && model.status === 'active') {
      selectedModel.value = modelName
    }
  }

  const getModelInfo = (modelName: string) => {
    return availableModels.value.find(model => model.name === modelName)
  }

  // Results management
  const setCurrentResults = (results: ClassificationResult[]) => {
    currentResults.value = results
  }

  const addResult = (result: ClassificationResult) => {
    currentResults.value.push(result)
  }

  const clearCurrentResults = () => {
    currentResults.value = []
  }

  const updateResultMetadata = (index: number, metadata: Partial<ClassificationResult>) => {
    if (index >= 0 && index < currentResults.value.length) {
      currentResults.value[index] = { ...currentResults.value[index], ...metadata }
    }
  }

  // Processing state
  const setProcessing = (processing: boolean, message = '') => {
    isProcessing.value = processing
    processingMessage.value = message
  }

  const setProcessingTime = (time: number) => {
    lastProcessingTime.value = time
  }

  // Configuration
  const updateConfiguration = (config: {
    threshold?: number
    maxResults?: number
    model?: string
  }) => {
    if (config.threshold !== undefined) {
      confidenceThreshold.value = Math.max(0, Math.min(1, config.threshold))
    }
    if (config.maxResults !== undefined) {
      maxResults.value = Math.max(1, Math.min(20, config.maxResults))
    }
    if (config.model !== undefined) {
      selectModel(config.model)
    }
  }

  const resetConfiguration = () => {
    confidenceThreshold.value = 0.5
    maxResults.value = 5
    selectedModel.value = 'default'
  }

  // History management
  const setHistory = (historyItems: ClassificationHistory[]) => {
    history.value = historyItems
  }

  const addToHistory = (historyItem: ClassificationHistory) => {
    history.value.unshift(historyItem) // Add to beginning for recent-first order
  }

  const removeFromHistory = (id: string) => {
    const index = history.value.findIndex(item => item.id === id)
    if (index > -1) {
      history.value.splice(index, 1)
    }
  }

  const clearHistory = () => {
    history.value = []
  }

  const getHistoryItem = (id: string) => {
    return history.value.find(item => item.id === id)
  }

  // Statistics and analytics
  const getModelStats = () => {
    return availableModels.value.map(model => ({
      name: model.name,
      description: model.description,
      status: model.status,
      accuracy: model.accuracy,
      inference_time: model.inference_time,
      usage_count: history.value.filter(item => item.model_used === model.name).length
    }))
  }

  const getResultsByModel = (modelName: string) => {
    return history.value.filter(item => item.model_used === modelName)
  }

  const getRecentResults = (limit = 10) => {
    return history.value.slice(0, limit)
  }

  // Prediction filtering and sorting
  const filterPredictionsByConfidence = (results: ClassificationResult[], minConfidence = 0.5) => {
    return results.map(result => ({
      ...result,
      predictions: result.predictions.filter(pred => pred.confidence >= minConfidence)
    })).filter(result => result.predictions.length > 0)
  }

  const sortPredictionsByConfidence = (results: ClassificationResult[]) => {
    return results.map(result => ({
      ...result,
      predictions: [...result.predictions].sort((a, b) => b.confidence - a.confidence)
    }))
  }

  const getTopPredictions = (results: ClassificationResult[], topN = 5) => {
    return results.map(result => ({
      ...result,
      predictions: result.predictions.slice(0, topN)
    }))
  }

  // Export functionality
  const prepareExportData = (format: 'json' | 'csv' = 'json') => {
    if (format === 'json') {
      return {
        timestamp: new Date().toISOString(),
        configuration: {
          model: selectedModel.value,
          threshold: confidenceThreshold.value,
          max_results: maxResults.value
        },
        results: currentResults.value,
        statistics: {
          total_results: currentResults.value.length,
          total_predictions: totalPredictions.value,
          average_processing_time: averageProcessingTime.value
        }
      }
    }
    
    // CSV format preparation
    const csvData: Array<Record<string, any>> = []
    currentResults.value.forEach((result, resultIndex) => {
      result.predictions.forEach((prediction, predIndex) => {
        csvData.push({
          result_index: resultIndex + 1,
          prediction_index: predIndex + 1,
          class_name: prediction.class_name,
          confidence: prediction.confidence,
          class_id: prediction.class_id,
          model_used: result.model_used,
          processing_time: result.processing_time,
          filename: result.image_metadata?.filename || `image_${resultIndex + 1}`
        })
      })
    })
    
    return csvData
  }

  return {
    // State
    availableModels,
    selectedModel,
    currentResults,
    history,
    isProcessing,
    processingMessage,
    lastProcessingTime,
    confidenceThreshold,
    maxResults,

    // Computed
    hasResults,
    hasHistory,
    activeModel,
    totalPredictions,
    averageProcessingTime,

    // Actions
    setAvailableModels,
    selectModel,
    getModelInfo,
    setCurrentResults,
    addResult,
    clearCurrentResults,
    updateResultMetadata,
    setProcessing,
    setProcessingTime,
    updateConfiguration,
    resetConfiguration,
    setHistory,
    addToHistory,
    removeFromHistory,
    clearHistory,
    getHistoryItem,
    getModelStats,
    getResultsByModel,
    getRecentResults,
    filterPredictionsByConfidence,
    sortPredictionsByConfidence,
    getTopPredictions,
    prepareExportData
  }
})