<template>
  <footer class="bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
    <div class="container-custom py-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Brand Section -->
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-gray-900 dark:text-white">{{ t('common.appName') }}</h2>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ t('nav.classify') }}・{{ t('footer.subtitle') }}</p>
            </div>
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400 max-w-md">
            {{ t('footer.description') }}
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
            {{ t('footer.quickLinks') }}
          </h3>
          <ul class="space-y-2">
            <li>
              <RouterLink to="/" class="text-sm text-gray-600 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 transition-colors">
                {{ t('nav.home') }}
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/classify" class="text-sm text-gray-600 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 transition-colors">
                {{ t('nav.classify') }}
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/history" class="text-sm text-gray-600 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 transition-colors">
                {{ t('nav.history') }}
              </RouterLink>
            </li>
            <li>
              <a href="/docs" target="_blank" class="text-sm text-gray-600 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 transition-colors">
                {{ t('footer.apiDocs') }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Technology -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4">
            {{ t('footer.techStack') }}
          </h3>
          <ul class="space-y-2">
            <li class="text-sm text-gray-600 dark:text-gray-400">Vue.js 3 + TypeScript</li>
            <li class="text-sm text-gray-600 dark:text-gray-400">Python FastAPI</li>
            <li class="text-sm text-gray-600 dark:text-gray-400">TensorFlow / PyTorch</li>
            <li class="text-sm text-gray-600 dark:text-gray-400">Docker & PostgreSQL</li>
          </ul>
        </div>
      </div>

      <!-- Bottom Section -->
      <div class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800">
        <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div class="flex items-center space-x-6">
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ t('footer.copyright') }}
            </p>
            <div class="flex items-center space-x-4">
              <!-- GitHub Link -->
              <a
                href="https://github.com/M-Ito-7310/image-classification-service"
                target="_blank"
                rel="noopener noreferrer"
                class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                aria-label="GitHub"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
            </div>
          </div>

          <!-- Status Badges -->
          <div class="flex items-center space-x-3">
            <span class="badge badge-success">{{ t('footer.developmentPhase') }}</span>
            <span class="badge badge-primary">v1.0.0</span>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>