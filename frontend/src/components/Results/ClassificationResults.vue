<template>
  <div v-if="hasResults" class="space-y-6">
    <!-- Results Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
          分類結果
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mt-1">
          {{ results.length }}個の画像を分析 • {{ totalPredictions }}個の予測
        </p>
      </div>
      
      <div class="flex items-center space-x-3">
        <!-- View Toggle -->
        <div class="flex bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
          <button
            @click="viewMode = 'grid'"
            class="px-3 py-2 text-sm font-medium rounded-md transition-colors"
            :class="viewMode === 'grid'
              ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
              : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            "
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
          </button>
          <button
            @click="viewMode = 'list'"
            class="px-3 py-2 text-sm font-medium rounded-md transition-colors"
            :class="viewMode === 'list'
              ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
              : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            "
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>
          </button>
        </div>

        <!-- Export Button -->
        <div class="relative" ref="exportDropdown">
          <button
            @click="showExportMenu = !showExportMenu"
            class="btn btn-secondary"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            エクスポート
          </button>
          
          <!-- Export Menu -->
          <Transition
            name="dropdown"
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <div
              v-if="showExportMenu"
              class="absolute right-0 mt-2 w-48 rounded-md shadow-lg glass border border-gray-200 dark:border-gray-600 z-10"
            >
              <div class="py-1">
                <button
                  @click="exportResults('json')"
                  class="block w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  JSON形式でエクスポート
                </button>
                <button
                  @click="exportResults('csv')"
                  class="block w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  CSV形式でエクスポート
                </button>
              </div>
            </div>
          </Transition>
        </div>

        <!-- Clear Results -->
        <button
          @click="clearResults"
          class="btn btn-outline text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
        >
          結果をクリア
        </button>
      </div>
    </div>

    <!-- Statistics Bar -->
    <div class="glass rounded-lg p-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
        <div>
          <div class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ averageConfidence.toFixed(1) }}%
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">平均信頼度</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ averageProcessingTime.toFixed(0) }}ms
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">平均処理時間</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ uniqueClasses.length }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">検出クラス数</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ highConfidenceCount }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">高信頼度結果</div>
        </div>
      </div>
    </div>

    <!-- Results Grid/List -->
    <div
      :class="viewMode === 'grid'
        ? 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6'
        : 'space-y-4'
      "
    >
      <ResultCard
        v-for="(result, index) in results"
        :key="index"
        :result="result"
        :index="index"
        :view-mode="viewMode"
        @view-details="showResultDetails"
      />
    </div>

    <!-- Result Details Modal -->
    <ResultModal
      v-if="selectedResult"
      :result="selectedResult"
      :show="showModal"
      @close="closeResultDetails"
    />

    <!-- Empty State (fallback) -->
    <div v-if="results.length === 0" class="text-center py-12">
      <svg class="mx-auto w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        結果がありません
      </h3>
      <p class="text-gray-600 dark:text-gray-400">
        画像をアップロードして分類を開始してください
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useClassificationStore } from '@/stores/classification'
import { useErrorStore } from '@/stores/error'
import { classificationApi } from '@/services/classificationApi'
import ResultCard from './ResultCard.vue'
import ResultModal from './ResultModal.vue'
import type { ClassificationResult } from '@/types/api'

// Stores
const classificationStore = useClassificationStore()
const errorStore = useErrorStore()

// Local state
const viewMode = ref<'grid' | 'list'>('grid')
const showExportMenu = ref(false)
const exportDropdown = ref<HTMLElement>()
const selectedResult = ref<ClassificationResult | null>(null)
const showModal = ref(false)

// Computed from store
const results = computed(() => classificationStore.currentResults)
const hasResults = computed(() => classificationStore.hasResults)
const totalPredictions = computed(() => classificationStore.totalPredictions)

// Statistics
const averageConfidence = computed(() => {
  if (results.value.length === 0) return 0
  
  const totalConfidence = results.value.reduce((sum, result) => {
    const avgConfidence = result.predictions.reduce((pSum, pred) => pSum + pred.confidence, 0) / result.predictions.length
    return sum + avgConfidence
  }, 0)
  
  return (totalConfidence / results.value.length) * 100
})

const averageProcessingTime = computed(() => {
  if (results.value.length === 0) return 0
  return results.value.reduce((sum, result) => sum + result.processing_time, 0) / results.value.length
})

const uniqueClasses = computed(() => {
  const classes = new Set<string>()
  results.value.forEach(result => {
    result.predictions.forEach(pred => {
      classes.add(pred.class_name)
    })
  })
  return Array.from(classes)
})

const highConfidenceCount = computed(() => {
  return results.value.reduce((count, result) => {
    return count + result.predictions.filter(pred => pred.confidence >= 0.8).length
  }, 0)
})

// Methods
const clearResults = () => {
  classificationStore.clearCurrentResults()
  
  window.dispatchEvent(new CustomEvent('app:toast', {
    detail: {
      type: 'info',
      title: '結果をクリア',
      message: '分類結果をクリアしました'
    }
  }))
}

const exportResults = async (format: 'json' | 'csv') => {
  showExportMenu.value = false
  
  try {
    const blob = await classificationApi.exportResults(results.value, format)
    
    // Create download link
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = classificationApi.generateExportFilename(format)
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'success',
        title: 'エクスポート完了',
        message: `${format.toUpperCase()}形式でエクスポートしました`
      }
    }))
    
  } catch (error) {
    errorStore.handleHttpError(error as any, 'Export results')
  }
}

const showResultDetails = (result: ClassificationResult) => {
  selectedResult.value = result
  showModal.value = true
}

const closeResultDetails = () => {
  selectedResult.value = null
  showModal.value = false
}

// Close export menu when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  if (exportDropdown.value && !exportDropdown.value.contains(event.target as Node)) {
    showExportMenu.value = false
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Watch for export menu changes
watch(showExportMenu, (newValue) => {
  if (newValue) {
    // Close other dropdowns if needed
  }
})
</script>

<style scoped>
.btn {
  @apply inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200;
}

.btn-secondary {
  @apply text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 focus:ring-gray-500;
}

.btn-outline {
  @apply border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-transparent hover:bg-gray-50 dark:hover:bg-gray-800 focus:ring-gray-500;
}

.glass {
  @apply bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.1s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>