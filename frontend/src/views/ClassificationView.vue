<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ t('classification.title') }}
            </h1>
            <p class="text-gray-600 dark:text-gray-400 mt-2">
              {{ t('classification.subtitle') }}
            </p>
          </div>
          
          <!-- How to Use Link -->
          <button
            @click="showGuide = true"
            class="flex items-center space-x-2 text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ t('classification.guide.howToUse') }}</span>
          </button>
        </div>
      </div>

      <!-- Upload Section -->
      <div class="mb-8">
        <ImageUpload @upload-complete="handleUploadComplete" />
      </div>

      <!-- Results Section -->
      <div v-if="hasResults">
        <ClassificationResults />
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="max-w-md mx-auto">
          <div class="mb-6">
            <svg class="mx-auto w-24 h-24 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('classification.emptyState.title') }}
          </h2>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            {{ t('classification.emptyState.description') }}
          </p>
          <div class="text-sm text-gray-500 dark:text-gray-400">
            {{ t('classification.emptyState.supportedFormats') }}
          </div>
        </div>
      </div>
    </div>

    <!-- How to Use Guide Modal -->
    <HowToGuide
      :is-visible="showGuide"
      @close="showGuide = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useClassificationStore } from '@/stores/classification'
import { ImageUpload } from '@/components/Upload'
import { ClassificationResults } from '@/components/Results'
import { HowToGuide } from '@/components/Guide'
import type { ClassificationResult } from '@/types/api'

// Stores and i18n
const { t } = useI18n()
const classificationStore = useClassificationStore()

// State
const showGuide = ref(false)

// Computed
const hasResults = computed(() => classificationStore.hasResults)

// Methods
const handleUploadComplete = (results: ClassificationResult[]) => {
  // Results are handled by the classification store
}
</script>