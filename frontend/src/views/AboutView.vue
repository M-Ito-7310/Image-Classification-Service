<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="w-[90%] mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="text-center mb-12">
        <div class="flex justify-center mb-6">
          <div class="p-4 bg-primary-100 dark:bg-primary-900/30 rounded-2xl">
            <svg class="w-16 h-16 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          {{ t('about.title') }}
        </h1>
        
        <p class="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          {{ t('about.subtitle') }}
        </p>
      </div>

      <div class="space-y-8">
        <!-- Overview Section -->
        <div class="glass rounded-2xl p-8">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            {{ t('about.overview.title') }}
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                {{ t('about.overview.highAccuracy.title') }}
              </h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                {{ t('about.overview.highAccuracy.description') }}
              </p>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                {{ t('about.overview.realtime.title') }}
              </h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                {{ t('about.overview.realtime.description') }}
              </p>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                {{ t('about.overview.formats.title') }}
              </h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                {{ t('about.overview.formats.description') }}
              </p>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                {{ t('about.overview.batch.title') }}
              </h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                {{ t('about.overview.batch.description') }}
              </p>
            </div>
          </div>
        </div>

        <!-- Technology Stack -->
        <div class="glass rounded-2xl p-8">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            {{ t('about.techStack.title') }}
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-[90%] mx-auto">
            <!-- Frontend -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <svg class="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                {{ t('about.techStack.frontend') }}
              </h3>
              <div class="space-y-2">
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-24 flex-shrink-0">Vue.js 3</span>
                  <span>{{ t('about.techStack.vue') }}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-24 flex-shrink-0">TypeScript</span>
                  <span>{{ t('about.techStack.typescript') }}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-24 flex-shrink-0">Tailwind CSS</span>
                  <span>{{ t('about.techStack.tailwind') }}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-24 flex-shrink-0">Pinia</span>
                  <span>{{ t('about.techStack.pinia') }}</span>
                </div>
              </div>
            </div>

            <!-- Backend -->
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2" />
                </svg>
                {{ t('about.techStack.backend') }}
              </h3>
              <div class="space-y-2">
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-24 flex-shrink-0">FastAPI</span>
                  <span>{{ t('about.techStack.fastapi') }}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-24 flex-shrink-0">Python</span>
                  <span>{{ t('about.techStack.python') }}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-24 flex-shrink-0">TensorFlow</span>
                  <span>{{ t('about.techStack.tensorflow') }}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <span class="w-24 flex-shrink-0">Docker</span>
                  <span>{{ t('about.techStack.docker') }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Metrics -->
        <div class="glass rounded-2xl p-8">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            {{ t('about.performance.title') }}
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="text-center">
              <div class="text-3xl font-bold text-primary-600 dark:text-primary-400 mb-2">
                99.2%
              </div>
              <div class="text-sm font-medium text-gray-900 dark:text-white mb-1">
                {{ t('about.performance.accuracy') }}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">
                Top-1 Accuracy
              </div>
            </div>

            <div class="text-center">
              <div class="text-3xl font-bold text-secondary-600 dark:text-secondary-400 mb-2">
                &lt;500ms
              </div>
              <div class="text-sm font-medium text-gray-900 dark:text-white mb-1">
                {{ t('about.performance.processingTime') }}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">
                {{ t('about.performance.timeNote') }}
              </div>
            </div>

            <div class="text-center">
              <div class="text-3xl font-bold text-success-600 dark:text-success-400 mb-2">
                1000+
              </div>
              <div class="text-sm font-medium text-gray-900 dark:text-white mb-1">
                {{ t('about.performance.supportedClasses') }}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">
                {{ t('about.performance.classesNote') }}
              </div>
            </div>

            <div class="text-center">
              <div class="text-3xl font-bold text-warning-600 dark:text-warning-400 mb-2">
                10MB
              </div>
              <div class="text-sm font-medium text-gray-900 dark:text-white mb-1">
                {{ t('about.performance.maxFileSize') }}
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">
                {{ t('about.performance.fileSizeNote') }}
              </div>
            </div>
          </div>
        </div>

        <!-- Contact Section -->
        <div class="glass rounded-2xl p-8">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
            {{ t('about.contact.title') }}
          </h2>
          
          <div class="text-center">
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              {{ t('about.contact.description') }}
            </p>
            
            <div class="flex justify-center space-x-6">
              <a
                href="mailto:support@example.com"
                class="inline-flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.476a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                {{ t('about.contact.email') }}
              </a>
              
              <a
                href="https://github.com/example/image-classification-service/issues"
                class="inline-flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
                target="_blank"
                rel="noopener noreferrer"
              >
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                {{ t('about.contact.github') }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.glass {
  @apply bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700;
}
</style>
