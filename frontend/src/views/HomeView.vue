<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800 py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Hero Section -->
      <div class="text-center mb-12">
        <div class="flex justify-center mb-6">
          <div class="p-4 bg-primary-100 dark:bg-primary-900/30 rounded-2xl">
            <svg class="w-16 h-16 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
          <span class="bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
            {{ t('home.title') }}
          </span>
          <br>
          {{ t('home.subtitle') }}
        </h1>
        
        <p class="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8">
          {{ t('home.description') }}
        </p>

        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-2xl mx-auto mb-12">
          <div class="glass rounded-lg p-4">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">99.2%</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">{{ t('home.stats.accuracy') }}</div>
          </div>
          <div class="glass rounded-lg p-4">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">&lt;500ms</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">{{ t('home.stats.speed') }}</div>
          </div>
          <div class="glass rounded-lg p-4">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">1000+</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">{{ t('home.stats.classes') }}</div>
          </div>
        </div>
      </div>

      <!-- Call to Action -->
      <div class="text-center mb-12">
        <RouterLink 
          to="/classify" 
          class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-primary-600 to-secondary-600 hover:from-primary-700 hover:to-secondary-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
        >
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          {{ t('home.startClassifying') }}
        </RouterLink>
      </div>

      <!-- Features Section -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        <!-- Feature 1: Easy Upload -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.upload.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.upload.description') }}
          </p>
        </div>

        <!-- Feature 2: AI Analysis -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-secondary-100 dark:bg-secondary-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-secondary-600 dark:text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.analysis.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.analysis.description') }}
          </p>
        </div>

        <!-- Feature 3: Detailed Results -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-success-100 dark:bg-success-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-success-600 dark:text-success-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2-2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.results.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.results.description') }}
          </p>
        </div>

        <!-- Feature 4: Multiple Formats -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-warning-100 dark:bg-warning-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-warning-600 dark:text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.formats.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.formats.description') }}
          </p>
        </div>

        <!-- Feature 5: Real-time Processing -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-info-100 dark:bg-info-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-info-600 dark:text-info-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.realtime.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.realtime.description') }}
          </p>
        </div>

        <!-- Feature 6: Export Options -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.export.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.export.description') }}
          </p>
        </div>

        <!-- Feature 7: Enterprise Collaboration -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.collaboration.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.collaboration.description') }}
          </p>
        </div>

        <!-- Feature 8: API Marketplace -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.marketplace.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.marketplace.description') }}
          </p>
        </div>

        <!-- Feature 9: Multi-modal Processing -->
        <div class="glass rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200">
          <div class="w-12 h-12 bg-rose-100 dark:bg-rose-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-rose-600 dark:text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ t('home.features.multimodal.title') }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            {{ t('home.features.multimodal.description') }}
          </p>
        </div>
      </div>

      <!-- Getting Started Guide -->
      <div v-if="!hasResults" class="glass rounded-2xl p-8 text-center mb-16">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          {{ t('home.howTo.title') }}
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="flex flex-col items-center">
            <div class="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mb-4">
              <span class="text-2xl font-bold text-primary-600 dark:text-primary-400">1</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {{ t('home.howTo.step1.title') }}
            </h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm">
              {{ t('home.howTo.step1.description') }}
            </p>
          </div>
          
          <div class="flex flex-col items-center">
            <div class="w-16 h-16 bg-secondary-100 dark:bg-secondary-900/30 rounded-full flex items-center justify-center mb-4">
              <span class="text-2xl font-bold text-secondary-600 dark:text-secondary-400">2</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {{ t('home.howTo.step2.title') }}
            </h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm">
              {{ t('home.howTo.step2.description') }}
            </p>
          </div>
          
          <div class="flex flex-col items-center">
            <div class="w-16 h-16 bg-success-100 dark:bg-success-900/30 rounded-full flex items-center justify-center mb-4">
              <span class="text-2xl font-bold text-success-600 dark:text-success-400">3</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {{ t('home.howTo.step3.title') }}
            </h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm">
              {{ t('home.howTo.step3.description') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Technical Specs -->
      <div v-if="!hasResults" class="glass rounded-2xl p-8 mb-16">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white text-center mb-8">
          {{ t('home.specs.title') }}
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="text-lg font-semibold text-gray-900 dark:text-white mb-2">{{ t('home.specs.formats') }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ t('home.specs.formatsValue') }}
            </div>
          </div>
          
          <div class="text-center">
            <div class="text-lg font-semibold text-gray-900 dark:text-white mb-2">{{ t('home.specs.maxSize') }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ t('home.specs.maxSizeValue') }}
            </div>
          </div>
          
          <div class="text-center">
            <div class="text-lg font-semibold text-gray-900 dark:text-white mb-2">{{ t('home.specs.concurrent') }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ t('home.specs.concurrentValue') }}
            </div>
          </div>
          
          <div class="text-center">
            <div class="text-lg font-semibold text-gray-900 dark:text-white mb-2">{{ t('home.specs.speed') }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ t('home.specs.speedValue') }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useClassificationStore } from '@/stores/classification'

// i18n
const { t } = useI18n()

// Classification store
const classificationStore = useClassificationStore()
const hasResults = computed(() => classificationStore.hasResults)
</script>

<style scoped>
.glass {
  @apply bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700;
}

/* Add smooth scrolling for the entire page */
html {
  scroll-behavior: smooth;
}

/* Gradient text animation */
.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Hover effects for feature cards */
.hover\:shadow-lg:hover {
  transform: translateY(-2px);
}
</style>
