<template>
  <Teleport to="body">
    <Transition
      name="modal"
      enter-active-class="transition-opacity duration-300"
      leave-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click="handleBackdropClick">
        <div
          class="glass rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden"
          @click.stop
        >
          <!-- Header -->
          <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
            <div class="flex-1 min-w-0">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white truncate">
                {{ result.image_metadata?.filename || 'Classification Result' }}
              </h2>
              <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {{ result.model_used }} • {{ result.processing_time.toFixed(0) }}ms • {{ result.predictions.length }}個の予測
              </p>
            </div>
            
            <button
              @click="$emit('close')"
              class="ml-4 p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Content -->
          <div class="overflow-y-auto" style="max-height: calc(90vh - 140px)">
            <div class="p-6">
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Image and Metadata -->
                <div class="space-y-4">
                  <!-- Image Preview -->
                  <div class="aspect-square bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden relative">
                    <img
                      v-if="result.image_metadata?.filename"
                      :src="getImagePreview()"
                      :alt="result.image_metadata.filename"
                      class="w-full h-full object-contain"
                      @error="handleImageError"
                    >
                    
                    <!-- Fallback -->
                    <div
                      v-else
                      class="w-full h-full flex items-center justify-center"
                    >
                      <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>

                    <!-- Processing Info Overlay -->
                    <div class="absolute top-4 right-4">
                      <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100">
                        {{ result.processing_time.toFixed(0) }}ms
                      </span>
                    </div>
                  </div>

                  <!-- Image Metadata -->
                  <div v-if="result.image_metadata" class="glass rounded-lg p-4">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                      画像情報
                    </h3>
                    
                    <dl class="grid grid-cols-2 gap-3 text-sm">
                      <div>
                        <dt class="font-medium text-gray-600 dark:text-gray-400">ファイル名</dt>
                        <dd class="text-gray-900 dark:text-white truncate" :title="result.image_metadata.filename">
                          {{ result.image_metadata.filename }}
                        </dd>
                      </div>
                      
                      <div>
                        <dt class="font-medium text-gray-600 dark:text-gray-400">サイズ</dt>
                        <dd class="text-gray-900 dark:text-white">
                          {{ formatFileSize(result.image_metadata.size) }}
                        </dd>
                      </div>
                      
                      <div>
                        <dt class="font-medium text-gray-600 dark:text-gray-400">形式</dt>
                        <dd class="text-gray-900 dark:text-white">
                          {{ result.image_metadata.format.toUpperCase() }}
                        </dd>
                      </div>
                      
                      <div>
                        <dt class="font-medium text-gray-600 dark:text-gray-400">解像度</dt>
                        <dd class="text-gray-900 dark:text-white">
                          {{ result.image_metadata.dimensions[0] }}×{{ result.image_metadata.dimensions[1] }}
                        </dd>
                      </div>
                      
                      <div v-if="result.threshold_applied">
                        <dt class="font-medium text-gray-600 dark:text-gray-400">信頼度閾値</dt>
                        <dd class="text-gray-900 dark:text-white">
                          {{ result.threshold_applied.toFixed(2) }}
                        </dd>
                      </div>
                      
                      <div>
                        <dt class="font-medium text-gray-600 dark:text-gray-400">使用モデル</dt>
                        <dd class="text-gray-900 dark:text-white">
                          {{ result.model_used }}
                        </dd>
                      </div>
                    </dl>
                  </div>
                </div>

                <!-- Predictions -->
                <div class="space-y-4">
                  <div class="flex items-center justify-between">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                      分類結果 ({{ result.predictions.length }})
                    </h3>
                    
                    <!-- Sort Options -->
                    <select
                      v-model="sortBy"
                      class="text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <option value="confidence">信頼度順</option>
                      <option value="name">クラス名順</option>
                    </select>
                  </div>

                  <!-- Predictions List -->
                  <div class="space-y-2 max-h-96 overflow-y-auto">
                    <div
                      v-for="(prediction, index) in sortedPredictions"
                      :key="index"
                      class="glass rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                    >
                      <div class="flex items-start justify-between mb-2">
                        <div class="flex-1 min-w-0">
                          <h4 class="text-base font-semibold text-gray-900 dark:text-white truncate">
                            {{ translateClassName(prediction.class_name) }}
                          </h4>
                          <p class="text-sm text-gray-600 dark:text-gray-400">
                            クラスID: {{ prediction.class_id }}
                          </p>
                        </div>
                        
                        <div class="text-right ml-4">
                          <div class="text-lg font-bold text-gray-900 dark:text-white">
                            {{ (prediction.confidence * 100).toFixed(2) }}%
                          </div>
                          <div
                            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                            :class="getConfidenceBadgeClass(prediction.confidence)"
                          >
                            {{ getConfidenceLabel(prediction.confidence) }}
                          </div>
                        </div>
                      </div>
                      
                      <!-- Confidence Bar -->
                      <div class="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                        <div
                          class="h-full rounded-full transition-all duration-300"
                          :class="getConfidenceBarClass(prediction.confidence)"
                          :style="{ width: `${prediction.confidence * 100}%` }"
                        ></div>
                      </div>
                    </div>
                  </div>

                  <!-- Confidence Distribution Chart -->
                  <div class="glass rounded-lg p-4">
                    <h4 class="text-base font-semibold text-gray-900 dark:text-white mb-3">
                      信頼度分布
                    </h4>
                    
                    <div class="space-y-2">
                      <div
                        v-for="range in confidenceRanges"
                        :key="range.label"
                        class="flex items-center justify-between"
                      >
                        <span class="text-sm text-gray-600 dark:text-gray-400">
                          {{ range.label }}
                        </span>
                        <div class="flex items-center space-x-2 flex-1 ml-4">
                          <div class="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
                            <div
                              class="h-full bg-primary-500 rounded-full transition-all duration-300"
                              :style="{ width: `${range.percentage}%` }"
                            ></div>
                          </div>
                          <span class="text-sm font-medium text-gray-900 dark:text-white min-w-12 text-right">
                            {{ range.count }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="flex items-center justify-between p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
            <div class="text-sm text-gray-600 dark:text-gray-400">
              最高信頼度: {{ (maxConfidence * 100).toFixed(2) }}% • 
              平均信頼度: {{ (avgConfidence * 100).toFixed(2) }}%
            </div>
            
            <div class="flex items-center space-x-3">
              <button
                @click="downloadResult"
                class="btn btn-secondary"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                ダウンロード
              </button>
              <button
                @click="$emit('close')"
                class="btn btn-primary"
              >
                閉じる
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { translateClassName } from '@/utils/labelTranslation'
import type { ClassificationResult } from '@/types/api'

interface Props {
  result: ClassificationResult
  show: boolean
}

interface Emits {
  close: []
}

const props = defineProps<Props>()
const emits = defineEmits<Emits>()

// Local state
const sortBy = ref<'confidence' | 'name'>('confidence')

// Computed
const sortedPredictions = computed(() => {
  const predictions = [...props.result.predictions]
  
  if (sortBy.value === 'confidence') {
    return predictions.sort((a, b) => b.confidence - a.confidence)
  } else {
    return predictions.sort((a, b) => translateClassName(a.class_name).localeCompare(translateClassName(b.class_name)))
  }
})

const maxConfidence = computed(() => {
  return Math.max(...props.result.predictions.map(p => p.confidence))
})

const avgConfidence = computed(() => {
  const total = props.result.predictions.reduce((sum, p) => sum + p.confidence, 0)
  return total / props.result.predictions.length
})

const confidenceRanges = computed(() => {
  const ranges = [
    { label: '90-100%', min: 0.9, max: 1.0 },
    { label: '80-89%', min: 0.8, max: 0.89 },
    { label: '70-79%', min: 0.7, max: 0.79 },
    { label: '60-69%', min: 0.6, max: 0.69 },
    { label: '50-59%', min: 0.5, max: 0.59 },
    { label: '0-49%', min: 0.0, max: 0.49 }
  ]
  
  const total = props.result.predictions.length
  
  return ranges.map(range => {
    const count = props.result.predictions.filter(p => 
      p.confidence >= range.min && p.confidence <= range.max
    ).length
    
    return {
      ...range,
      count,
      percentage: total > 0 ? (count / total) * 100 : 0
    }
  }).filter(range => range.count > 0)
})

// Methods
const handleBackdropClick = (e: MouseEvent) => {
  if (e.target === e.currentTarget) {
    emits('close')
  }
}

const getImagePreview = (): string => {
  // Use the image_url from the result if available
  if (props.result.image_url) {
    // Construct full URL with API base
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${props.result.image_url}`
  }
  
  // Fallback: try to construct URL from filename and id
  if (props.result.id && props.result.image_metadata?.filename) {
    const extension = props.result.image_metadata.filename.split('.').pop()?.toLowerCase() || 'jpg'
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/uploads/${props.result.id}.${extension}`
  }
  
  // Last resort: placeholder
  return '/api/placeholder-image.jpg'
}

const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
}

const getConfidenceLabel = (confidence: number): string => {
  if (confidence >= 0.9) return '非常に高い'
  if (confidence >= 0.8) return '高い'
  if (confidence >= 0.6) return '中程度'
  if (confidence >= 0.4) return '低い'
  return '非常に低い'
}

const getConfidenceBadgeClass = (confidence: number): string => {
  if (confidence >= 0.8) {
    return 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100'
  } else if (confidence >= 0.6) {
    return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100'
  } else if (confidence >= 0.4) {
    return 'bg-orange-100 text-orange-800 dark:bg-orange-800 dark:text-orange-100'
  } else {
    return 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100'
  }
}

const getConfidenceBarClass = (confidence: number): string => {
  if (confidence >= 0.8) return 'bg-green-500'
  if (confidence >= 0.6) return 'bg-yellow-500'
  if (confidence >= 0.4) return 'bg-orange-500'
  return 'bg-red-500'
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const downloadResult = async () => {
  try {
    const data = {
      timestamp: new Date().toISOString(),
      filename: props.result.image_metadata?.filename,
      result: props.result,
      statistics: {
        max_confidence: maxConfidence.value,
        avg_confidence: avgConfidence.value,
        confidence_distribution: confidenceRanges.value
      }
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json'
    })
    
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `classification-detail-${props.result.image_metadata?.filename || Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'success',
        title: 'ダウンロード完了',
        message: '詳細結果をダウンロードしました'
      }
    }))
    
  } catch (error) {
    console.error('Download failed:', error)
  }
}
</script>

<style scoped>
.glass {
  @apply bg-white/90 dark:bg-gray-800/90 backdrop-blur-md border border-gray-200 dark:border-gray-700;
}

.btn {
  @apply inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors;
}

.btn-primary {
  @apply text-white bg-primary-600 hover:bg-primary-700 focus:ring-primary-500;
}

.btn-secondary {
  @apply text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 focus:ring-gray-500;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  @apply bg-gray-100 dark:bg-gray-700 rounded;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  @apply bg-gray-400 dark:bg-gray-500 rounded;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-500 dark:bg-gray-400;
}
</style>