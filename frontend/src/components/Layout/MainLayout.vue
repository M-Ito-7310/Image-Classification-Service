<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 dark-transition">
    <!-- Header -->
    <AppHeader />

    <!-- Main Content -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <AppFooter />

    <!-- Loading Overlay -->
    <Transition
      name="fade"
      enter-active-class="transition-opacity duration-300"
      leave-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div v-if="isLoading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="glass rounded-2xl p-8 flex items-center space-x-4">
          <div class="spinner"></div>
          <div class="text-white">
            <p class="font-medium">処理中...</p>
            <p v-if="loadingMessage" class="text-sm text-gray-300">{{ loadingMessage }}</p>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Toast Notifications -->
    <div class="fixed bottom-4 right-4 space-y-2 z-40">
      <TransitionGroup
        name="toast"
        enter-active-class="transition-all duration-300 ease-out"
        leave-active-class="transition-all duration-200 ease-in"
        enter-from-class="transform translate-x-full opacity-0"
        leave-to-class="transform translate-x-full opacity-0"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="glass rounded-lg p-4 max-w-sm shadow-lg"
          :class="{
            'border-l-4 border-success-500': toast.type === 'success',
            'border-l-4 border-error-500': toast.type === 'error',
            'border-l-4 border-warning-500': toast.type === 'warning',
            'border-l-4 border-primary-500': toast.type === 'info'
          }"
        >
          <div class="flex items-start space-x-3">
            <!-- Icon -->
            <div class="flex-shrink-0">
              <svg v-if="toast.type === 'success'" class="w-5 h-5 text-success-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
              <svg v-else-if="toast.type === 'error'" class="w-5 h-5 text-error-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <svg v-else-if="toast.type === 'warning'" class="w-5 h-5 text-warning-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="w-5 h-5 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white">
                {{ toast.title }}
              </p>
              <p v-if="toast.message" class="text-sm text-gray-600 dark:text-gray-300">
                {{ toast.message }}
              </p>
            </div>

            <!-- Close Button -->
            <button
              @click="removeToast(toast.id)"
              class="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'

interface Toast {
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

const isLoading = ref(false)
const loadingMessage = ref('')
const toasts = ref<Toast[]>([])
let toastCounter = 0

const showLoading = (message = '') => {
  isLoading.value = true
  loadingMessage.value = message
}

const hideLoading = () => {
  isLoading.value = false
  loadingMessage.value = ''
}

const showToast = (toast: Omit<Toast, 'id'>) => {
  const newToast: Toast = {
    id: ++toastCounter,
    duration: 5000,
    ...toast
  }
  
  toasts.value.push(newToast)
  
  // Auto remove toast after duration
  setTimeout(() => {
    removeToast(newToast.id)
  }, newToast.duration)
}

const removeToast = (id: number) => {
  const index = toasts.value.findIndex(toast => toast.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

// Global event listeners for loading and toasts
const handleGlobalLoading = (event: Event) => {
  const customEvent = event as CustomEvent
  if (customEvent.detail.show) {
    showLoading(customEvent.detail.message)
  } else {
    hideLoading()
  }
}

const handleGlobalToast = (event: Event) => {
  const customEvent = event as CustomEvent
  showToast(customEvent.detail)
}

onMounted(() => {
  window.addEventListener('app:loading', handleGlobalLoading)
  window.addEventListener('app:toast', handleGlobalToast)
})

onUnmounted(() => {
  window.removeEventListener('app:loading', handleGlobalLoading)
  window.removeEventListener('app:toast', handleGlobalToast)
})

// Expose methods globally
defineExpose({
  showLoading,
  hideLoading,
  showToast,
  removeToast
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>