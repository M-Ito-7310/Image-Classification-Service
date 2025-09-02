<template>
  <div class="optimized-upload-container">
    <!-- Performance Settings -->
    <div class="glass rounded-xl p-4 mb-6">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">
          パフォーマンス設定
        </h3>
        <button
          @click="showAdvanced = !showAdvanced"
          class="text-primary-600 hover:text-primary-700 text-sm"
        >
          {{ showAdvanced ? '詳細を非表示' : '詳細設定' }}
        </button>
      </div>
      
      <div v-if="showAdvanced" class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            画像最適化
          </label>
          <div class="flex items-center space-x-2">
            <input
              v-model="optimizationOptions.enableCompression"
              type="checkbox"
              class="rounded border-gray-300 dark:border-gray-600"
            >
            <span class="text-sm text-gray-600 dark:text-gray-400">圧縮を有効化</span>
          </div>
          <div class="flex items-center space-x-2 mt-2">
            <input
              v-model="optimizationOptions.enableResize"
              type="checkbox"
              class="rounded border-gray-300 dark:border-gray-600"
            >
            <span class="text-sm text-gray-600 dark:text-gray-400">リサイズを有効化</span>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            結果キャッシュ
          </label>
          <div class="flex items-center space-x-2">
            <input
              v-model="enableCache"
              type="checkbox"
              class="rounded border-gray-300 dark:border-gray-600"
            >
            <span class="text-sm text-gray-600 dark:text-gray-400">結果をキャッシュ</span>
          </div>
          <div class="text-xs text-gray-500 mt-1">
            ヒット率: {{ Math.round(cacheStats.hitRate * 100) }}%
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Area -->
    <div class="glass rounded-2xl p-6">
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
            画像をドラッグ&ドロップまたはクリックして選択
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-500 mb-4">
            対応形式: JPEG, PNG, WebP, BMP • 最適化により高速処理
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
            @click="$refs.fileInput.click()"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            ファイルを選択
          </button>
        </div>

        <!-- Selected Files with Optimization Info -->
        <div v-else class="text-left">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-medium text-gray-900 dark:text-white">
              選択されたファイル ({{ selectedFiles.length }})
            </h3>
            <div class="flex space-x-2">
              <button
                @click="optimizeAll"
                :disabled="optimizing || processing"
                class="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 disabled:opacity-50"
              >
                {{ optimizing ? '最適化中...' : '最適化' }}
              </button>
              <button
                @click="clearFiles"
                class="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
              >
                クリア
              </button>
            </div>
          </div>

          <!-- Optimization Progress -->
          <div v-if="optimizing" class="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="spinner-small"></div>
              <div class="flex-1">
                <div class="flex justify-between text-sm">
                  <span class="text-blue-800 dark:text-blue-200">
                    最適化中: {{ optimizationProgress.completed }}/{{ optimizationProgress.total }}
                  </span>
                  <span class="text-blue-600 dark:text-blue-400">
                    {{ Math.round((optimizationProgress.completed / optimizationProgress.total) * 100) }}%
                  </span>
                </div>
                <div class="w-full bg-blue-200 dark:bg-blue-800 rounded-full h-1.5 mt-1">
                  <div
                    class="bg-blue-600 h-1.5 rounded-full transition-all"
                    :style="{ width: `${(optimizationProgress.completed / optimizationProgress.total) * 100}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- File List -->
          <div class="space-y-2 max-h-64 overflow-y-auto">
            <div
              v-for="(fileInfo, index) in selectedFiles"
              :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
            >
              <div class="flex items-center space-x-3 flex-1">
                <div class="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded-lg flex-shrink-0 overflow-hidden">
                  <img
                    v-if="fileInfo.thumbnail"
                    :src="fileInfo.thumbnail"
                    :alt="fileInfo.file.name"
                    class="w-full h-full object-cover"
                  >
                </div>
                <div class="flex-1 min-w-0">
                  <p class="font-medium text-gray-900 dark:text-white text-sm truncate">
                    {{ fileInfo.file.name }}
                  </p>
                  <div class="flex items-center space-x-4 text-xs text-gray-500">
                    <span>{{ formatFileSize(fileInfo.file.size) }}</span>
                    <span v-if="fileInfo.optimized" class="text-green-600 dark:text-green-400">
                      {{ Math.round((1 - fileInfo.optimized.compressionRatio) * 100) }}% 削減
                    </span>
                    <span v-if="fileInfo.cached" class="text-blue-600 dark:text-blue-400">
                      キャッシュ済み
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="flex items-center space-x-2">
                <!-- Processing Status -->
                <div v-if="processingStatus[index]" class="flex items-center">
                  <div v-if="processingStatus[index] === 'processing'" class="spinner-small"></div>
                  <svg v-else-if="processingStatus[index] === 'completed'" class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <svg v-else-if="processingStatus[index] === 'cached'" class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
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

          <!-- Summary Stats -->
          <div v-if="optimizationSummary" class="mt-4 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <div class="flex justify-between items-center text-sm">
              <span class="text-green-800 dark:text-green-200">
                最適化完了: {{ formatFileSize(optimizationSummary.reductionBytes) }} 削減
              </span>
              <span class="text-green-600 dark:text-green-400">
                {{ Math.round(optimizationSummary.reductionPercentage) }}% 軽量化
              </span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="mt-6 flex justify-end space-x-4">
            <button
              @click="$refs.fileInput.click()"
              :disabled="processing"
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 
                     dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 disabled:opacity-50"
            >
              ファイルを追加
            </button>
            <button
              @click="processImages"
              :disabled="!canProcess || processing"
              class="px-6 py-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white rounded-lg
                     hover:from-primary-600 hover:to-secondary-600 disabled:opacity-50 disabled:cursor-not-allowed
                     flex items-center space-x-2"
            >
              <div v-if="processing" class="spinner-small"></div>
              <span>{{ processing ? '処理中...' : '分類開始' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Processing Progress -->
    <div v-if="processing" class="glass rounded-xl p-6 mt-6">
      <div class="flex items-center space-x-4">
        <div class="spinner"></div>
        <div class="flex-1">
          <h3 class="font-medium text-gray-900 dark:text-white mb-2">
            処理中: {{ processingProgress.completed }}/{{ processingProgress.total }}
          </h3>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              class="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full transition-all"
              :style="{ width: `${(processingProgress.completed / processingProgress.total) * 100}%` }"
            ></div>
          </div>
          <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mt-2">
            <span>{{ processingProgress.cached }} キャッシュヒット</span>
            <span>{{ Math.round((processingProgress.completed / processingProgress.total) * 100) }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Metrics -->
    <div v-if="performanceMetrics && selectedFiles.length > 0" class="glass rounded-xl p-4 mt-6">
      <h4 class="font-medium text-gray-900 dark:text-white mb-3">パフォーマンス指標</h4>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
        <div class="text-center">
          <div class="font-bold text-blue-600 dark:text-blue-400">
            {{ Math.round(performanceMetrics.optimization.averageTime) }}ms
          </div>
          <div class="text-gray-500">平均最適化時間</div>
        </div>
        <div class="text-center">
          <div class="font-bold text-green-600 dark:text-green-400">
            {{ formatFileSize(performanceMetrics.optimization.throughput) }}/s
          </div>
          <div class="text-gray-500">処理スループット</div>
        </div>
        <div class="text-center">
          <div class="font-bold text-purple-600 dark:text-purple-400">
            {{ Math.round(cacheStats.hitRate * 100) }}%
          </div>
          <div class="text-gray-500">キャッシュヒット率</div>
        </div>
        <div class="text-center">
          <div class="font-bold text-orange-600 dark:text-orange-400">
            {{ cacheStats.totalEntries }}
          </div>
          <div class="text-gray-500">キャッシュエントリ</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ImageOptimizer, ImagePreview, PerformanceMonitor, formatFileSize, validateImageFile } from '@/utils/imageOptimizer'
import { ResultCache } from '@/utils/resultCache'
import type { OptimizationOptions, OptimizedImage } from '@/utils/imageOptimizer'
import type { CacheStats } from '@/utils/resultCache'

interface FileInfo {
  file: File
  thumbnail?: string
  optimized?: OptimizedImage
  cached?: boolean
}

const emit = defineEmits<{
  uploadComplete: [results: any[]]
}>()

const authStore = useAuthStore()

// State
const selectedFiles = ref<FileInfo[]>([])
const optimizing = ref(false)
const processing = ref(false)
const isDragging = ref(false)
const showAdvanced = ref(false)
const enableCache = ref(true)

const optimizationOptions = ref<OptimizationOptions>({
  maxWidth: 1024,
  maxHeight: 1024,
  quality: 0.85,
  format: 'jpeg',
  enableResize: true,
  enableCompression: true
})

const optimizationProgress = ref({ completed: 0, total: 0 })
const processingProgress = ref({ completed: 0, total: 0, cached: 0 })
const processingStatus = ref<Record<number, 'processing' | 'completed' | 'cached' | 'error'>>({})
const optimizationSummary = ref<any>(null)
const performanceMetrics = ref<any>(null)
const cacheStats = ref<CacheStats>({
  totalEntries: 0,
  hitRate: 0,
  memoryUsage: 0,
  oldestEntry: Date.now(),
  newestEntry: Date.now()
})

// Computed
const canProcess = computed(() => {
  return selectedFiles.value.length > 0 && !optimizing.value
})

// Methods
const handleFileSelect = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files) {
    await addFiles(Array.from(input.files))
  }
}

const handleDrop = async (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = false
  
  if (event.dataTransfer?.files) {
    await addFiles(Array.from(event.dataTransfer.files))
  }
}

const addFiles = async (files: File[]) => {
  const validFiles: FileInfo[] = []
  
  for (const file of files) {
    const validation = validateImageFile(file)
    if (validation.valid) {
      try {
        const thumbnail = await ImageOptimizer.generateThumbnail(file, 100)
        const cached = await ResultCache.has(file, 'default')
        
        validFiles.push({
          file,
          thumbnail,
          cached
        })
      } catch (error) {
        console.error(`Failed to process ${file.name}:`, error)
      }
    } else {
      window.dispatchEvent(new CustomEvent('app:toast', {
        detail: {
          type: 'error',
          title: 'ファイルエラー',
          message: `${file.name}: ${validation.error}`
        }
      }))
    }
  }

  selectedFiles.value.push(...validFiles)
  updateCacheStats()
}

const removeFile = (index: number) => {
  const fileInfo = selectedFiles.value[index]
  if (fileInfo.thumbnail) {
    ImagePreview.cleanup(fileInfo.thumbnail)
  }
  selectedFiles.value.splice(index, 1)
  delete processingStatus.value[index]
}

const clearFiles = () => {
  selectedFiles.value.forEach(fileInfo => {
    if (fileInfo.thumbnail) {
      ImagePreview.cleanup(fileInfo.thumbnail)
    }
  })
  selectedFiles.value = []
  processingStatus.value = {}
  optimizationSummary.value = null
}

const optimizeAll = async () => {
  if (optimizing.value) return

  optimizing.value = true
  optimizationProgress.value = { completed: 0, total: selectedFiles.value.length }

  const endTiming = PerformanceMonitor.startTiming('optimization')

  try {
    const filesToOptimize = selectedFiles.value.map(fileInfo => fileInfo.file)
    
    const optimizedImages = await ImageOptimizer.optimizeImages(
      filesToOptimize,
      optimizationOptions.value,
      (completed, total) => {
        optimizationProgress.value = { completed, total }
      }
    )

    // Update file info with optimization results
    optimizedImages.forEach((optimized, index) => {
      selectedFiles.value[index].optimized = optimized
    })

    // Calculate summary
    optimizationSummary.value = ImageOptimizer.calculateSizeReduction(optimizedImages)
    
    const totalSize = optimizedImages.reduce((sum, img) => sum + img.originalSize, 0)
    endTiming(totalSize)

    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'success',
        title: '最適化完了',
        message: `${optimizedImages.length}個のファイルを最適化しました`
      }
    }))
  } catch (error) {
    console.error('Optimization error:', error)
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'error',
        title: '最適化エラー',
        message: '画像の最適化に失敗しました'
      }
    }))
  } finally {
    optimizing.value = false
    updatePerformanceMetrics()
  }
}

const processImages = async () => {
  if (!canProcess.value) return

  processing.value = true
  processingProgress.value = { completed: 0, total: selectedFiles.value.length, cached: 0 }
  processingStatus.value = {}

  const results: any[] = []
  const endTiming = PerformanceMonitor.startTiming('classification')

  try {
    for (let i = 0; i < selectedFiles.value.length; i++) {
      const fileInfo = selectedFiles.value[i]
      const fileToProcess = fileInfo.optimized?.file || fileInfo.file
      
      processingStatus.value[i] = 'processing'

      try {
        // Check cache first
        if (enableCache.value) {
          const cachedResult = await ResultCache.get(fileToProcess, 'default')
          if (cachedResult) {
            results.push(cachedResult)
            processingStatus.value[i] = 'cached'
            processingProgress.value.cached++
            processingProgress.value.completed++
            continue
          }
        }

        // Process image
        const formData = new FormData()
        formData.append('file', fileToProcess)

        const response = await fetch('/api/v1/classify', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
          },
          body: formData
        })

        if (response.ok) {
          const result = await response.json()
          results.push(result)
          
          // Cache result
          if (enableCache.value) {
            await ResultCache.set(fileToProcess, 'default', result)
          }
          
          processingStatus.value[i] = 'completed'
        } else {
          throw new Error('Classification failed')
        }
      } catch (error) {
        console.error(`Failed to process ${fileInfo.file.name}:`, error)
        processingStatus.value[i] = 'error'
      }

      processingProgress.value.completed++
    }

    endTiming()
    emit('uploadComplete', results)

    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'success',
        title: '処理完了',
        message: `${results.length}個の画像を処理しました`
      }
    }))
  } catch (error) {
    console.error('Processing error:', error)
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'error',
        title: '処理エラー',
        message: '画像の処理に失敗しました'
      }
    }))
  } finally {
    processing.value = false
    updatePerformanceMetrics()
    updateCacheStats()
  }
}

const updatePerformanceMetrics = () => {
  performanceMetrics.value = PerformanceMonitor.getMetrics()
}

const updateCacheStats = () => {
  cacheStats.value = ResultCache.getStats()
}

onMounted(() => {
  updatePerformanceMetrics()
  updateCacheStats()
})

onUnmounted(() => {
  clearFiles()
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