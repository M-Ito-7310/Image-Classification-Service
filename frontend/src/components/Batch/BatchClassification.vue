<template>
  <div class="batch-classification-container">
    <!-- Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        {{ t('classification.batch.title') }}
      </h2>
      <p class="text-gray-600 dark:text-gray-300">
        複数の画像を一度に分類できます（最大10ファイル）
      </p>
    </div>

    <!-- File Selection -->
    <div class="glass rounded-2xl p-6 mb-6">
      <div
        @drop="handleDrop"
        @dragover.prevent
        @dragenter.prevent
        class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center
               hover:border-primary-500 dark:hover:border-primary-400 transition-colors"
        :class="{ 'border-primary-500 bg-primary-50 dark:bg-primary-900/20': isDragging }"
      >
        <div v-if="selectedFiles.length === 0">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p class="text-gray-600 dark:text-gray-400 mb-2">
            {{ t('classification.batch.selectFiles') }}
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-500 mb-4">
            対応形式: JPEG, PNG, WebP, BMP • 最大10MB/ファイル
          </p>
          <input
            ref="fileInput"
            type="file"
            @change="handleFileSelect"
            accept="image/*"
            multiple
            class="hidden"
          >
          <button
            type="button"
            @click="$refs.fileInput.click()"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            ファイルを選択
          </button>
        </div>

        <!-- Selected Files List -->
        <div v-else class="text-left">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-medium text-gray-900 dark:text-white">
              選択されたファイル ({{ selectedFiles.length }}/10)
            </h3>
            <button
              @click="clearFiles"
              class="text-red-600 hover:text-red-700 text-sm"
            >
              すべて削除
            </button>
          </div>
          
          <div class="space-y-2 max-h-64 overflow-y-auto">
            <div
              v-for="(file, index) in selectedFiles"
              :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
            >
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gray-200 dark:bg-gray-700 rounded-lg flex-shrink-0 overflow-hidden">
                  <img
                    v-if="file.preview"
                    :src="file.preview"
                    :alt="file.name"
                    class="w-full h-full object-cover"
                  >
                </div>
                <div>
                  <p class="font-medium text-gray-900 dark:text-white text-sm">
                    {{ file.name }}
                  </p>
                  <p class="text-xs text-gray-500">
                    {{ formatFileSize(file.size) }}
                  </p>
                </div>
              </div>
              
              <div class="flex items-center space-x-2">
                <!-- Processing Status -->
                <div v-if="processingStatus[index]" class="flex items-center space-x-2">
                  <div v-if="processingStatus[index] === 'processing'" class="spinner-small"></div>
                  <svg v-else-if="processingStatus[index] === 'completed'" class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <svg v-else-if="processingStatus[index] === 'error'" class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                
                <button
                  @click="removeFile(index)"
                  :disabled="processing"
                  class="p-1 text-red-500 hover:text-red-700 disabled:opacity-50"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          
          <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div class="flex justify-between items-center">
              <div class="text-sm text-gray-600 dark:text-gray-400">
                総サイズ: {{ formatFileSize(totalSize) }}
              </div>
              <button
                @click="$refs.fileInput.click()"
                :disabled="selectedFiles.length >= 10 || processing"
                class="text-primary-600 hover:text-primary-700 text-sm disabled:opacity-50"
              >
                ファイルを追加
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Classification Options -->
      <div v-if="selectedFiles.length > 0" class="mb-6">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
          分類オプション
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              使用モデル
            </label>
            <select
              v-model="options.model"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option value="default">デフォルトモデル</option>
              <option v-for="model in customModels" :key="model.model_id" :value="model.model_id">
                {{ model.name }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              信頼度閾値
            </label>
            <input
              v-model.number="options.confidenceThreshold"
              type="range"
              min="0.1"
              max="0.9"
              step="0.1"
              class="w-full"
            >
            <div class="text-sm text-gray-500 text-center mt-1">
              {{ options.confidenceThreshold }}
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              最大結果数
            </label>
            <select
              v-model.number="options.maxResults"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            >
              <option :value="1">1</option>
              <option :value="3">3</option>
              <option :value="5">5</option>
              <option :value="10">10</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Process Button -->
      <div v-if="selectedFiles.length > 0 && !processing" class="mb-6">
        <button
          @click="processBatch"
          class="w-full px-6 py-3 bg-gradient-to-r from-primary-500 to-secondary-500 text-white rounded-lg
                 hover:from-primary-600 hover:to-secondary-600 flex items-center justify-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span>バッチ処理を開始 ({{ selectedFiles.length }}ファイル)</span>
        </button>
      </div>

      <!-- Processing Progress -->
      <div v-if="processing" class="glass rounded-xl p-6 mb-6">
        <div class="flex items-center space-x-4">
          <div class="spinner"></div>
          <div class="flex-1">
            <h3 class="font-medium text-gray-900 dark:text-white mb-2">
              {{ t('classification.batch.processing', { current: currentProcessing, total: selectedFiles.length }) }}
            </h3>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                class="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${progress}%` }"
              ></div>
            </div>
            <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mt-2">
              <span>{{ currentProcessing }} / {{ selectedFiles.length }}</span>
              <span>{{ Math.round(progress) }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Batch Results -->
      <div v-if="batchResults && !processing" class="glass rounded-xl p-6">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{ t('classification.batch.results') }}
          </h3>
          <div class="flex space-x-2">
            <button
              @click="exportResults"
              class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              結果をエクスポート
            </button>
            <button
              @click="clearResults"
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
            >
              クリア
            </button>
          </div>
        </div>

        <!-- Summary -->
        <div class="grid grid-cols-3 gap-4 mb-6">
          <div class="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <div class="text-2xl font-bold text-green-600 dark:text-green-400">
              {{ batchResults.successful_classifications }}
            </div>
            <div class="text-sm text-green-600 dark:text-green-400">
              {{ t('classification.batch.completed') }}
            </div>
          </div>
          <div class="text-center p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
            <div class="text-2xl font-bold text-red-600 dark:text-red-400">
              {{ batchResults.failed_classifications }}
            </div>
            <div class="text-sm text-red-600 dark:text-red-400">
              {{ t('classification.batch.failed') }}
            </div>
          </div>
          <div class="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {{ batchResults.total_files }}
            </div>
            <div class="text-sm text-blue-600 dark:text-blue-400">
              総ファイル数
            </div>
          </div>
        </div>

        <!-- Results Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="(result, index) in batchResults.results"
            :key="index"
            class="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
          >
            <div class="flex items-start space-x-3">
              <div class="w-16 h-16 bg-gray-200 dark:bg-gray-700 rounded-lg flex-shrink-0 overflow-hidden">
                <img
                  v-if="result.image_url"
                  :src="result.image_url"
                  :alt="result.filename"
                  class="w-full h-full object-cover"
                >
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="font-medium text-gray-900 dark:text-white text-sm truncate">
                  {{ result.filename }}
                </h4>
                <div class="mt-2 space-y-1">
                  <div
                    v-for="(prediction, predIndex) in result.predictions.slice(0, 3)"
                    :key="predIndex"
                    class="flex justify-between items-center"
                  >
                    <span class="text-sm text-gray-600 dark:text-gray-400 truncate">
                      {{ prediction }}
                    </span>
                    <span class="text-sm font-medium text-gray-900 dark:text-white ml-2">
                      {{ Math.round(result.confidence_scores[predIndex] * 100) }}%
                    </span>
                  </div>
                </div>
                <div class="mt-2 text-xs text-gray-500">
                  処理時間: {{ result.processing_time }}ms
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Errors -->
        <div v-if="batchResults.errors && batchResults.errors.length > 0" class="mt-6">
          <h4 class="font-medium text-red-600 dark:text-red-400 mb-3">
            処理エラー ({{ batchResults.errors.length }}件)
          </h4>
          <div class="space-y-2">
            <div
              v-for="(error, index) in batchResults.errors"
              :key="index"
              class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
            >
              <div class="flex justify-between items-start">
                <div>
                  <p class="font-medium text-red-800 dark:text-red-200 text-sm">
                    {{ error.filename }}
                  </p>
                  <p class="text-sm text-red-700 dark:text-red-300">
                    {{ error.error }}
                  </p>
                </div>
                <span class="text-xs text-red-600 dark:text-red-400">
                  {{ error.status_code }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

interface FileWithPreview extends File {
  preview?: string
}

interface BatchResult {
  batch_id: string
  total_files: number
  successful_classifications: number
  failed_classifications: number
  results: Array<{
    id: string
    filename: string
    predictions: string[]
    confidence_scores: number[]
    processing_time: number
    model_used: string
    image_url: string
  }>
  errors: Array<{
    filename: string
    error: string
    status_code: number
  }>
  timestamp: string
}

const { t } = useI18n()
const authStore = useAuthStore()

const selectedFiles = ref<FileWithPreview[]>([])
const processing = ref(false)
const currentProcessing = ref(0)
const isDragging = ref(false)
const processingStatus = ref<Record<number, 'processing' | 'completed' | 'error'>>({})
const batchResults = ref<BatchResult | null>(null)
const customModels = ref<Array<{ model_id: string; name: string }>>([])

const options = ref({
  model: 'default',
  confidenceThreshold: 0.5,
  maxResults: 5
})

const totalSize = computed(() => {
  return selectedFiles.value.reduce((sum, file) => sum + file.size, 0)
})

const progress = computed(() => {
  if (selectedFiles.value.length === 0) return 0
  return (currentProcessing.value / selectedFiles.value.length) * 100
})

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files) {
    addFiles(Array.from(input.files))
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = false
  
  if (event.dataTransfer?.files) {
    addFiles(Array.from(event.dataTransfer.files))
  }
}

const addFiles = (files: File[]) => {
  const newFiles = files.filter(file => {
    if (!file.type.startsWith('image/')) return false
    if (file.size > 10 * 1024 * 1024) return false
    return !selectedFiles.value.some(existing => 
      existing.name === file.name && existing.size === file.size
    )
  }).slice(0, 10 - selectedFiles.value.length)

  newFiles.forEach(file => {
    const fileWithPreview = file as FileWithPreview
    
    const reader = new FileReader()
    reader.onload = (e) => {
      fileWithPreview.preview = e.target?.result as string
    }
    reader.readAsDataURL(file)
    
    selectedFiles.value.push(fileWithPreview)
  })
}

const removeFile = (index: number) => {
  selectedFiles.value.splice(index, 1)
  delete processingStatus.value[index]
}

const clearFiles = () => {
  selectedFiles.value = []
  processingStatus.value = {}
  batchResults.value = null
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const processBatch = async () => {
  if (selectedFiles.value.length === 0) return
  
  processing.value = true
  currentProcessing.value = 0
  processingStatus.value = {}
  batchResults.value = null

  try {
    const formData = new FormData()
    
    selectedFiles.value.forEach((file, index) => {
      formData.append('files', file)
      processingStatus.value[index] = 'processing'
    })

    formData.append('model', options.value.model)
    formData.append('confidence_threshold', options.value.confidenceThreshold.toString())
    formData.append('max_results', options.value.maxResults.toString())

    const response = await fetch('/api/v1/classify/batch', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
      body: formData
    })

    if (response.ok) {
      const result = await response.json()
      batchResults.value = result
      
      selectedFiles.value.forEach((_, index) => {
        processingStatus.value[index] = 'completed'
      })
      
      currentProcessing.value = selectedFiles.value.length

      window.dispatchEvent(new CustomEvent('app:toast', {
        detail: {
          type: 'success',
          title: 'バッチ処理完了',
          message: `${result.successful_classifications}件の画像を正常に分類しました`
        }
      }))
    } else {
      throw new Error('Batch processing failed')
    }
  } catch (error) {
    selectedFiles.value.forEach((_, index) => {
      processingStatus.value[index] = 'error'
    })

    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'error',
        title: 'バッチ処理エラー',
        message: error instanceof Error ? error.message : 'バッチ処理に失敗しました'
      }
    }))
  } finally {
    processing.value = false
  }
}

const exportResults = () => {
  if (!batchResults.value) return

  const data = {
    batch_id: batchResults.value.batch_id,
    timestamp: batchResults.value.timestamp,
    summary: {
      total_files: batchResults.value.total_files,
      successful: batchResults.value.successful_classifications,
      failed: batchResults.value.failed_classifications
    },
    results: batchResults.value.results,
    errors: batchResults.value.errors
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `batch-results-${batchResults.value.batch_id}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const clearResults = () => {
  batchResults.value = null
  selectedFiles.value = []
  processingStatus.value = {}
  currentProcessing.value = 0
}

const loadCustomModels = async () => {
  try {
    const response = await fetch('/api/v1/models/custom', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      }
    })
    
    if (response.ok) {
      const models = await response.json()
      customModels.value = models.filter((model: any) => model.status === 'active')
    }
  } catch (error) {
    console.error('Failed to load custom models:', error)
  }
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    loadCustomModels()
  }
})
</script>

<style scoped>
.spinner {
  @apply w-6 h-6 border-2 border-primary-600 border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

.spinner-small {
  @apply w-4 h-4 border-2 border-current border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>