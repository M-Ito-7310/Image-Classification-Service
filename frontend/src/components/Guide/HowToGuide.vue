<template>
  <div v-if="isVisible" class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- Backdrop -->
    <div 
      class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm"
      @click="closeGuide"
    ></div>
    
    <!-- Modal -->
    <div class="relative bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-4xl w-full mx-4 overflow-hidden">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">
            {{ t('classification.guide.title') }}
          </h2>
        </div>
        
        <!-- Step Indicator -->
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-500 dark:text-gray-400">
            {{ currentStep + 1 }} / {{ totalSteps }}
          </span>
        </div>
        
        <!-- Close Button -->
        <button
          @click="closeGuide"
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- Content -->
      <div class="p-8">
        <div class="min-h-[400px]">
          <!-- Step 1: Upload -->
          <div v-if="currentStep === 0" class="text-center">
            <div class="w-20 h-20 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {{ t('classification.guide.steps.upload.title') }}
            </h3>
            <p class="text-gray-600 dark:text-gray-400 text-lg mb-6">
              {{ t('classification.guide.steps.upload.description') }}
            </p>
            <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-6 text-left">
              <ul class="space-y-3">
                <li class="flex items-start space-x-3">
                  <div class="w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span class="text-white text-xs font-bold">1</span>
                  </div>
                  <span class="text-gray-700 dark:text-gray-300">{{ t('classification.guide.steps.upload.method1') }}</span>
                </li>
                <li class="flex items-start space-x-3">
                  <div class="w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span class="text-white text-xs font-bold">2</span>
                  </div>
                  <span class="text-gray-700 dark:text-gray-300">{{ t('classification.guide.steps.upload.method2') }}</span>
                </li>
                <li class="flex items-start space-x-3">
                  <div class="w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span class="text-white text-xs font-bold">3</span>
                  </div>
                  <span class="text-gray-700 dark:text-gray-300">{{ t('classification.guide.steps.upload.method3') }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Step 2: Options -->
          <div v-if="currentStep === 1" class="text-center">
            <div class="w-20 h-20 bg-secondary-100 dark:bg-secondary-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-secondary-600 dark:text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {{ t('classification.guide.steps.options.title') }}
            </h3>
            <p class="text-gray-600 dark:text-gray-400 text-lg mb-6">
              {{ t('classification.guide.steps.options.description') }}
            </p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">{{ t('classification.guide.steps.options.model') }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.options.modelDesc') }}</p>
              </div>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">{{ t('classification.guide.steps.options.confidence') }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.options.confidenceDesc') }}</p>
              </div>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">{{ t('classification.guide.steps.options.maxResults') }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.options.maxResultsDesc') }}</p>
              </div>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">{{ t('classification.guide.steps.options.preprocessing') }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.options.preprocessingDesc') }}</p>
              </div>
            </div>
          </div>

          <!-- Step 3: Results -->
          <div v-if="currentStep === 2" class="text-center">
            <div class="w-20 h-20 bg-success-100 dark:bg-success-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2-2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {{ t('classification.guide.steps.results.title') }}
            </h3>
            <p class="text-gray-600 dark:text-gray-400 text-lg mb-6">
              {{ t('classification.guide.steps.results.description') }}
            </p>
            <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-6 text-left">
              <ul class="space-y-4">
                <li class="flex items-start space-x-3">
                  <div class="w-8 h-8 bg-success-500 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4" />
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-semibold text-gray-900 dark:text-white">{{ t('classification.guide.steps.results.confidence') }}</h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.results.confidenceDesc') }}</p>
                  </div>
                </li>
                <li class="flex items-start space-x-3">
                  <div class="w-8 h-8 bg-success-500 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-semibold text-gray-900 dark:text-white">{{ t('classification.guide.steps.results.ranking') }}</h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.results.rankingDesc') }}</p>
                  </div>
                </li>
                <li class="flex items-start space-x-3">
                  <div class="w-8 h-8 bg-success-500 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-semibold text-gray-900 dark:text-white">{{ t('classification.guide.steps.results.metadata') }}</h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.results.metadataDesc') }}</p>
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Step 4: Export -->
          <div v-if="currentStep === 3" class="text-center">
            <div class="w-20 h-20 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-10 h-10 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {{ t('classification.guide.steps.export.title') }}
            </h3>
            <p class="text-gray-600 dark:text-gray-400 text-lg mb-6">
              {{ t('classification.guide.steps.export.description') }}
            </p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">JSON</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.export.jsonDesc') }}</p>
              </div>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                <div class="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0V4a2 2 0 012-2h14a2 2 0 012 2v16a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">CSV</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.export.csvDesc') }}</p>
              </div>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <svg class="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2v0a2 2 0 01-2-2V9a2 2 0 00-2-2H8z" />
                  </svg>
                </div>
                <h4 class="font-semibold text-gray-900 dark:text-white mb-2">{{ t('classification.guide.steps.export.reportTitle') }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ t('classification.guide.steps.export.reportDesc') }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Navigation -->
      <div class="flex items-center justify-between p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
        <!-- Previous Button -->
        <button
          @click="previousStep"
          :disabled="currentStep === 0"
          class="flex items-center space-x-2 px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          <span>{{ t('classification.guide.navigation.previous') }}</span>
        </button>
        
        <!-- Step Dots -->
        <div class="flex items-center space-x-2">
          <button
            v-for="step in totalSteps"
            :key="step"
            @click="goToStep(step - 1)"
            class="w-3 h-3 rounded-full transition-colors"
            :class="step - 1 === currentStep 
              ? 'bg-primary-500' 
              : 'bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500'"
          ></button>
        </div>
        
        <!-- Next/Done Button -->
        <button
          @click="nextStep"
          class="flex items-center space-x-2 px-6 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors"
        >
          <span>{{ isLastStep ? t('classification.guide.navigation.done') : t('classification.guide.navigation.next') }}</span>
          <svg v-if="!isLastStep" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

// Props
interface Props {
  isVisible: boolean
}

interface Emits {
  (e: 'close'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// i18n
const { t } = useI18n()

// State
const currentStep = ref(0)
const totalSteps = 4

// Computed
const isLastStep = computed(() => currentStep.value === totalSteps - 1)

// Methods
const closeGuide = () => {
  emit('close')
  currentStep.value = 0
}

const nextStep = () => {
  if (isLastStep.value) {
    closeGuide()
  } else {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const goToStep = (step: number) => {
  currentStep.value = step
}

// Keyboard navigation
const handleKeydown = (event: KeyboardEvent) => {
  if (!props.isVisible) return
  
  if (event.key === 'Escape') {
    closeGuide()
  } else if (event.key === 'ArrowRight') {
    nextStep()
  } else if (event.key === 'ArrowLeft') {
    previousStep()
  }
}

// Add keyboard listeners
if (typeof window !== 'undefined') {
  window.addEventListener('keydown', handleKeydown)
}
</script>

<style scoped>
/* Animation for modal entrance */
.fixed {
  animation: modalEnter 0.3s ease-out;
}

@keyframes modalEnter {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Custom scrollbar for modal content */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgb(243, 244, 246);
}

.dark .overflow-y-auto::-webkit-scrollbar-track {
  background: rgb(31, 41, 55);
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgb(156, 163, 175);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgb(107, 114, 128);
}
</style>