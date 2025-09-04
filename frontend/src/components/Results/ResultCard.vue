<template>
  <div
    class="glass rounded-lg overflow-hidden hover:shadow-lg transition-all duration-200 cursor-pointer"
    :class="viewMode === 'list' ? 'flex' : 'block'"
    @click="$emit('view-details', result)"
  >
    <!-- Image Section -->
    <div
      :class="viewMode === 'list'
        ? 'w-32 h-32 flex-shrink-0'
        : 'aspect-square'
      "
      class="bg-gray-100 dark:bg-gray-800 relative overflow-hidden"
    >
      <img
        v-if="result.image_metadata?.filename"
        :src="getImagePreview()"
        :alt="result.image_metadata.filename"
        class="w-full h-full object-cover"
        @error="handleImageError"
      >
      
      <!-- Fallback Icon -->
      <div
        v-else
        class="w-full h-full flex items-center justify-center"
      >
        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>

      <!-- Processing Badge -->
      <div class="absolute top-2 right-2">
        <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100">
          {{ result.processing_time.toFixed(0) }}ms
        </span>
      </div>

      <!-- Prediction Count Badge -->
      <div class="absolute bottom-2 left-2">
        <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-800 dark:text-primary-100">
          {{ t('classification.results.predictionsCount', { count: result.predictions.length }) }}
        </span>
      </div>
    </div>

    <!-- Content Section -->
    <div class="p-4 flex-1">
      <!-- Header -->
      <div class="flex items-start justify-between mb-3">
        <div class="flex-1 min-w-0">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white truncate">
            {{ result.image_metadata?.filename || `Image ${index + 1}` }}
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {{ result.model_used }} • 
            <span v-if="result.image_metadata">
              {{ formatImageSize(result.image_metadata.dimensions) }}
            </span>
          </p>
        </div>
        
        <!-- Confidence Score -->
        <div class="text-right ml-4">
          <div class="text-lg font-bold text-gray-900 dark:text-white">
            {{ (topPrediction?.confidence * 100).toFixed(1) }}%
          </div>
          <div class="text-xs text-gray-600 dark:text-gray-400">{{ t('classification.results.highestConfidence') }}</div>
        </div>
      </div>

      <!-- Top Predictions -->
      <div class="space-y-2">
        <div
          v-for="(prediction, predIndex) in visiblePredictions"
          :key="predIndex"
          class="flex items-center justify-between"
        >
          <div class="flex-1 min-w-0 mr-3">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-gray-900 dark:text-white truncate">
                {{ translateClassName(prediction.class_name) }}
              </span>
              <span
                v-if="prediction.confidence >= 0.8"
                class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100"
              >
                {{ t('classification.results.highConfidence') }}
              </span>
            </div>
          </div>
          
          <!-- Confidence Bar -->
          <div class="flex items-center space-x-2">
            <div class="w-16 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div
                class="h-full rounded-full transition-all duration-300"
                :class="getConfidenceColor(prediction.confidence)"
                :style="{ width: `${prediction.confidence * 100}%` }"
              ></div>
            </div>
            <span class="text-sm font-medium text-gray-600 dark:text-gray-400 min-w-12 text-right">
              {{ (prediction.confidence * 100).toFixed(0) }}%
            </span>
          </div>
        </div>
        
        <!-- Show More Button -->
        <button
          v-if="result.predictions.length > maxVisiblePredictions"
          @click.stop="toggleShowAll"
          class="text-xs text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-colors"
        >
          {{ showAll 
            ? t('classification.results.showLess', { count: result.predictions.length - maxVisiblePredictions })
            : t('classification.results.showMore', { count: result.predictions.length - maxVisiblePredictions })
          }}
        </button>
      </div>

      <!-- Metadata (List view only) -->
      <div
        v-if="viewMode === 'list' && result.image_metadata"
        class="mt-4 pt-3 border-t border-gray-200 dark:border-gray-700"
      >
        <div class="grid grid-cols-3 gap-4 text-xs text-gray-600 dark:text-gray-400">
          <div>
            <span class="font-medium">{{ t('classification.results.size') }}:</span>
            {{ formatFileSize(result.image_metadata.size) }}
          </div>
          <div>
            <span class="font-medium">{{ t('classification.results.format') }}:</span>
            {{ result.image_metadata.format.toUpperCase() }}
          </div>
          <div>
            <span class="font-medium">{{ t('classification.results.threshold') }}:</span>
            {{ (result.threshold_applied || 0.5).toFixed(2) }}
          </div>
        </div>
      </div>

      <!-- Action Buttons (List view only) -->
      <div
        v-if="viewMode === 'list'"
        class="mt-4 flex items-center space-x-2"
      >
        <button
          @click.stop="$emit('view-details', result)"
          class="flex-1 px-3 py-2 text-xs font-medium text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20 rounded-md hover:bg-primary-100 dark:hover:bg-primary-900/40 transition-colors"
        >
          {{ t('classification.results.viewDetails') }}
        </button>
        <button
          @click.stop="downloadResult"
          class="px-3 py-2 text-xs font-medium text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { translateClassName } from '@/utils/labelTranslation'
import type { ClassificationResult } from '@/types/api'

interface Props {
  result: ClassificationResult
  index: number
  viewMode: 'grid' | 'list'
}

interface Emits {
  'view-details': [result: ClassificationResult]
}

const props = defineProps<Props>()
const emits = defineEmits<Emits>()

// Composables
const { t } = useI18n()

// i18n is now working correctly

// Local state
const showAll = ref(false)
const maxVisiblePredictions = ref(3)

// Computed
const topPrediction = computed(() => props.result.predictions[0])

const visiblePredictions = computed(() => {
  if (showAll.value || props.result.predictions.length <= maxVisiblePredictions.value) {
    return props.result.predictions
  }
  return props.result.predictions.slice(0, maxVisiblePredictions.value)
})

// Methods
const toggleShowAll = () => {
  showAll.value = !showAll.value
}

const getImagePreview = (): string => {
  // Use the image_url from the result if available
  if (props.result.image_url) {
    const fullUrl = `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${props.result.image_url}`
    return fullUrl
  }
  
  // Fallback: try to construct URL from filename and id
  if (props.result.id && props.result.image_metadata?.filename) {
    const extension = props.result.image_metadata.filename.split('.').pop()?.toLowerCase() || 'jpg'
    const constructedUrl = `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/uploads/${props.result.id}.${extension}`
    return constructedUrl
  }
  
  // Last resort: placeholder
  return '/api/placeholder-image.jpg'
}

const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
}

const getConfidenceColor = (confidence: number): string => {
  if (confidence >= 0.8) {
    return 'bg-green-500'
  } else if (confidence >= 0.6) {
    return 'bg-yellow-500'
  } else if (confidence >= 0.4) {
    return 'bg-orange-500'
  } else {
    return 'bg-red-500'
  }
}

const formatImageSize = (dimensions: [number, number]): string => {
  return `${dimensions[0]}×${dimensions[1]}`
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
    // Create a downloadable JSON of this specific result
    const data = {
      timestamp: new Date().toISOString(),
      filename: props.result.image_metadata?.filename,
      result: props.result
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json'
    })
    
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `classification-${props.result.image_metadata?.filename || `image-${props.index + 1}`}-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'success',
        title: t('classification.results.downloadCompleted'),
        message: t('classification.results.downloadMessage')
      }
    }))
    
  } catch (error) {
    console.error('Download failed:', error)
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'error',
        title: t('classification.results.downloadError'),
        message: t('classification.results.downloadErrorMessage')
      }
    }))
  }
}
</script>

<style scoped>
.glass {
  @apply bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700;
}
</style>