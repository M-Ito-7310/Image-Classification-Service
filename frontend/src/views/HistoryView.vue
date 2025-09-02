<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            {{ t('history.title') }}
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            {{ t('history.subtitle') }}
          </p>
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Search -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              type="text"
:placeholder="t('history.searchPlaceholder')"
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md leading-5 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
            >
          </div>
          
          <!-- Clear History -->
          <button
            v-if="hasHistory"
            @click="clearHistory"
            class="btn btn-outline text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
          >
            {{ t('history.clearHistory') }}
          </button>
        </div>
      </div>

      <!-- Stats Bar -->
      <div v-if="hasHistory" class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="glass rounded-lg p-4 text-center">
          <div class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ history.length }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">{{ t('history.stats.totalClassifications') }}</div>
        </div>
        <div class="glass rounded-lg p-4 text-center">
          <div class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ totalPredictions }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">{{ t('history.stats.totalPredictions') }}</div>
        </div>
        <div class="glass rounded-lg p-4 text-center">
          <div class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ averageProcessingTime.toFixed(0) }}ms
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">{{ t('history.stats.averageProcessingTime') }}</div>
        </div>
        <div class="glass rounded-lg p-4 text-center">
          <div class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ uniqueModels.length }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">{{ t('history.stats.uniqueModels') }}</div>
        </div>
      </div>

      <!-- History List -->
      <div v-if="hasHistory" class="space-y-4">
        <div
          v-for="item in filteredHistory"
          :key="item.id"
          class="glass rounded-lg p-6 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between">
            <!-- History Item Info -->
            <div class="flex-1">
              <div class="flex items-center space-x-4 mb-4">
                <!-- Thumbnail placeholder -->
                <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                  <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                
                <div class="flex-1 min-w-0">
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white truncate">
                    {{ item.filename }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {{ formatDate(item.created_at) }} • 
                    {{ item.model_used }} • 
                    {{ item.processing_time.toFixed(0) }}ms
                  </p>
                </div>
              </div>

              <!-- Predictions Preview -->
              <div class="space-y-2">
                <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {{ t('history.results.title') }} ({{ t('history.results.count', { count: item.predictions.length }) }})
                </h4>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="(prediction, index) in item.predictions.slice(0, 3)"
                    :key="index"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getConfidenceBadgeClass(prediction.confidence)"
                  >
                    {{ prediction.class_name }}
                    <span class="ml-1 font-semibold">
                      {{ (prediction.confidence * 100).toFixed(0) }}%
                    </span>
                  </span>
                  <span
                    v-if="item.predictions.length > 3"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
                  >
                    +{{ t('history.results.count', { count: item.predictions.length - 3 }) }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center space-x-2 ml-4">
              <button
                @click="viewHistoryItem(item)"
                class="btn btn-sm btn-secondary"
              >
                {{ t('history.actions.details') }}
              </button>
              <button
                @click="downloadHistoryItem(item)"
                class="btn btn-sm btn-outline"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </button>
              <button
                @click="removeHistoryItem(item.id)"
                class="btn btn-sm btn-outline text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="max-w-md mx-auto">
          <div class="mb-6">
            <svg class="mx-auto w-24 h-24 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('history.empty') }}
          </h2>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            {{ t('history.emptySubtitle') }}
          </p>
          <router-link
            to="/"
            class="btn btn-primary"
          >
            {{ t('history.classifyNow') }}
          </router-link>
        </div>
      </div>

      <!-- History Item Modal -->
      <ResultModal
        v-if="selectedHistoryItem"
        :result="historyItemToResult(selectedHistoryItem)"
        :show="showHistoryModal"
        @close="closeHistoryModal"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useClassificationStore } from '@/stores/classification'
import { useErrorStore } from '@/stores/error'
import { classificationApi } from '@/services/classificationApi'
import { ResultModal } from '@/components/Results'
import type { ClassificationHistory, ClassificationResult } from '@/types/api'

// Stores and i18n
const { t, locale } = useI18n()
const classificationStore = useClassificationStore()
const errorStore = useErrorStore()

// Local state
const searchQuery = ref('')
const selectedHistoryItem = ref<ClassificationHistory | null>(null)
const showHistoryModal = ref(false)

// Computed
const history = computed(() => classificationStore.history)
const hasHistory = computed(() => classificationStore.hasHistory)

const filteredHistory = computed(() => {
  if (!searchQuery.value) return history.value
  
  const query = searchQuery.value.toLowerCase()
  return history.value.filter(item => 
    item.filename.toLowerCase().includes(query) ||
    item.model_used.toLowerCase().includes(query) ||
    item.predictions.some(p => p.class_name.toLowerCase().includes(query))
  )
})

const totalPredictions = computed(() => 
  history.value.reduce((sum, item) => sum + item.predictions.length, 0)
)

const averageProcessingTime = computed(() => {
  if (history.value.length === 0) return 0
  const total = history.value.reduce((sum, item) => sum + item.processing_time, 0)
  return total / history.value.length
})

const uniqueModels = computed(() => {
  const models = new Set(history.value.map(item => item.model_used))
  return Array.from(models)
})

// Methods
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString(locale.value === 'ja' ? 'ja-JP' : 'en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
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

const viewHistoryItem = (item: ClassificationHistory) => {
  selectedHistoryItem.value = item
  showHistoryModal.value = true
}

const closeHistoryModal = () => {
  selectedHistoryItem.value = null
  showHistoryModal.value = false
}

const historyItemToResult = (item: ClassificationHistory): ClassificationResult => {
  return {
    predictions: item.predictions,
    processing_time: item.processing_time,
    model_used: item.model_used,
    image_metadata: {
      filename: item.filename,
      size: 0,
      format: '',
      dimensions: [0, 0]
    }
  }
}

const downloadHistoryItem = async (item: ClassificationHistory) => {
  try {
    const data = {
      timestamp: new Date().toISOString(),
      history_item: item,
      exported_from: 'history'
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json'
    })
    
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `history-${item.filename}-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'success',
        title: t('history.messages.downloadComplete'),
        message: t('history.messages.downloadSuccess')
      }
    }))
    
  } catch (error) {
    console.error('Download failed:', error)
    errorStore.handleSystemError(t('errors.processing'))
  }
}

const removeHistoryItem = async (id: string) => {
  try {
    await classificationApi.deleteHistoryItem(id)
    classificationStore.removeFromHistory(id)
  } catch (error) {
    console.error('Delete failed:', error)
    errorStore.handleHttpError(error as any, 'Delete history item')
  }
}

const clearHistory = () => {
  if (confirm(t('history.messages.clearConfirm'))) {
    classificationStore.clearHistory()
    
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'info',
        title: t('history.messages.historyCleared'),
        message: t('history.messages.allHistoryDeleted')
      }
    }))
  }
}
</script>

<style scoped>
.glass {
  @apply bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700;
}

.btn {
  @apply inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors;
}

.btn-sm {
  @apply px-2 py-1 text-xs;
}

.btn-primary {
  @apply text-white bg-primary-600 hover:bg-primary-700 focus:ring-primary-500;
}

.btn-secondary {
  @apply text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 focus:ring-gray-500;
}

.btn-outline {
  @apply border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-transparent hover:bg-gray-50 dark:hover:bg-gray-800 focus:ring-gray-500;
}
</style>