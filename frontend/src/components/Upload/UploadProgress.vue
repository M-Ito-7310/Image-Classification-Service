<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="glass rounded-2xl p-8 max-w-md w-full mx-4">
      <!-- Progress Header -->
      <div class="text-center mb-6">
        <div class="mx-auto w-16 h-16 mb-4 relative">
          <div class="spinner"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
        </div>
        
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          {{ title }}
        </h3>
        
        <p class="text-gray-600 dark:text-gray-400">
          {{ message }}
        </p>
      </div>

      <!-- Progress Bar -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            進行状況
          </span>
          <span class="text-sm font-semibold text-primary-600 dark:text-primary-400">
            {{ progress }}%
          </span>
        </div>
        
        <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full transition-all duration-500 ease-out"
            :style="{ width: `${progress}%` }"
          >
            <div class="h-full bg-white bg-opacity-25 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>

      <!-- File Details -->
      <div v-if="fileDetails" class="space-y-3 mb-6">
        <div class="flex items-center justify-between text-sm">
          <span class="text-gray-600 dark:text-gray-400">現在のファイル:</span>
          <span class="font-medium text-gray-900 dark:text-white truncate max-w-32">
            {{ fileDetails.currentFile }}
          </span>
        </div>
        
        <div class="flex items-center justify-between text-sm">
          <span class="text-gray-600 dark:text-gray-400">ファイル数:</span>
          <span class="font-medium text-gray-900 dark:text-white">
            {{ fileDetails.currentIndex + 1 }} / {{ fileDetails.totalFiles }}
          </span>
        </div>
        
        <div v-if="fileDetails.totalSize > 0" class="flex items-center justify-between text-sm">
          <span class="text-gray-600 dark:text-gray-400">アップロード済み:</span>
          <span class="font-medium text-gray-900 dark:text-white">
            {{ formatFileSize(fileDetails.uploadedSize) }} / {{ formatFileSize(fileDetails.totalSize) }}
          </span>
        </div>
      </div>

      <!-- Time Estimates -->
      <div v-if="timeEstimates" class="grid grid-cols-2 gap-4 mb-6">
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ formatTime(timeEstimates.elapsed) }}
          </div>
          <div class="text-xs text-gray-600 dark:text-gray-400">経過時間</div>
        </div>
        
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ formatTime(timeEstimates.remaining) }}
          </div>
          <div class="text-xs text-gray-600 dark:text-gray-400">残り時間</div>
        </div>
      </div>

      <!-- Status Messages -->
      <div v-if="statusMessages.length > 0" class="space-y-2 mb-6">
        <div class="text-sm font-medium text-gray-700 dark:text-gray-300">
          処理状況:
        </div>
        <div class="max-h-24 overflow-y-auto space-y-1">
          <div
            v-for="(status, index) in statusMessages.slice(-3)"
            :key="index"
            class="text-xs text-gray-600 dark:text-gray-400 flex items-center space-x-2"
          >
            <div class="w-1.5 h-1.5 rounded-full bg-primary-500"></div>
            <span>{{ status }}</span>
          </div>
        </div>
      </div>

      <!-- Cancel Button -->
      <div v-if="allowCancel" class="flex justify-center">
        <button
          @click="handleCancel"
          class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
        >
          キャンセル
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

export interface FileDetails {
  currentFile: string
  currentIndex: number
  totalFiles: number
  uploadedSize: number
  totalSize: number
}

export interface TimeEstimates {
  elapsed: number // seconds
  remaining: number // seconds
}

interface Props {
  show: boolean
  progress: number
  title?: string
  message?: string
  fileDetails?: FileDetails
  timeEstimates?: TimeEstimates
  statusMessages?: string[]
  allowCancel?: boolean
}

interface Emits {
  cancel: []
}

const props = withDefaults(defineProps<Props>(), {
  title: 'アップロード中',
  message: 'ファイルを処理しています...',
  statusMessages: () => [],
  allowCancel: false
})

const emits = defineEmits<Emits>()

// Progress validation
const validatedProgress = computed(() => {
  return Math.max(0, Math.min(100, props.progress))
})

// Format file size
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// Format time duration
const formatTime = (seconds: number): string => {
  if (seconds < 0 || !isFinite(seconds)) return '--:--'
  
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

// Handle cancel
const handleCancel = () => {
  emits('cancel')
}

// Watch for progress changes and update animation
const progress = computed(() => props.progress)

watch(progress, (newProgress) => {
  // Add any progress-related side effects here
  if (newProgress === 100) {
    // Handle completion
    setTimeout(() => {
      // Auto-hide after completion (if needed)
    }, 1000)
  }
})
</script>

<style scoped>
.spinner {
  @apply w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin;
}

.glass {
  @apply bg-white/95 dark:bg-gray-800/95 backdrop-blur-md border border-gray-200 dark:border-gray-700 shadow-2xl;
}

/* Custom scrollbar for status messages */
.max-h-24::-webkit-scrollbar {
  width: 4px;
}

.max-h-24::-webkit-scrollbar-track {
  @apply bg-gray-100 dark:bg-gray-700 rounded;
}

.max-h-24::-webkit-scrollbar-thumb {
  @apply bg-gray-400 dark:bg-gray-500 rounded;
}

.max-h-24::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-500 dark:bg-gray-400;
}

/* Progress bar pulse animation */
@keyframes progress-pulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

.animate-pulse {
  animation: progress-pulse 1.5s ease-in-out infinite;
}
</style>