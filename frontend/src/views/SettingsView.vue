<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          {{ t('settings.title') }}
        </h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          {{ t('settings.subtitle') }}
        </p>
      </div>

      <div class="space-y-8">
        <!-- Appearance Settings -->
        <div class="glass rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            {{ t('settings.appearance.title') }}
          </h2>
          
          <div class="space-y-4">
            <!-- Theme Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {{ t('settings.appearance.theme') }}
              </label>
              <div class="grid grid-cols-2 gap-3">
                <button
                  v-for="theme in themeOptions"
                  :key="theme.value"
                  @click="updateSetting('theme', theme.value)"
                  class="flex items-center justify-center px-4 py-3 text-sm font-medium rounded-lg border-2 transition-colors"
                  :class="settings.theme === theme.value
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300'
                    : 'border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600'
                  "
                >
                  <svg v-if="theme.value === 'light'" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                  <svg v-else-if="theme.value === 'dark'" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                  {{ theme.label }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Model Settings -->
        <div class="glass rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            {{ t('settings.classification.title') }}
          </h2>
          
          <div class="space-y-4">
            <!-- Default Model -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {{ t('settings.classification.defaultModel') }}
              </label>
              <select
                v-model="settings.defaultModel"
                @change="updateModelDefaults({ defaultModel: settings.defaultModel })"
                class="input-field"
              >
                <option value="default">{{ t('settings.classification.options.default') }}</option>
                <option
                  v-for="model in availableModels"
                  :key="model.name"
                  :value="model.name"
                >
                  {{ model.description || model.name }}
                </option>
              </select>
            </div>

            <!-- Default Threshold -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {{ t('settings.classification.defaultThreshold') }}: {{ settings.defaultThreshold.toFixed(2) }}
              </label>
              <input
                v-model.number="settings.defaultThreshold"
                type="range"
                min="0"
                max="1"
                step="0.05"
                class="w-full"
                @input="updateModelDefaults({ defaultThreshold: settings.defaultThreshold })"
              >
              <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                <span>0.00</span>
                <span>0.50</span>
                <span>1.00</span>
              </div>
            </div>

            <!-- Default Max Results -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {{ t('settings.classification.defaultMaxResults') }}
              </label>
              <input
                v-model.number="settings.defaultMaxResults"
                type="number"
                min="1"
                max="20"
                class="input-field"
                @change="updateModelDefaults({ defaultMaxResults: settings.defaultMaxResults })"
              >
            </div>

            <!-- Image Enhancement -->
            <div>
              <label class="flex items-center space-x-3">
                <input
                  v-model="settings.enableImageEnhancement"
                  type="checkbox"
                  class="checkbox"
                  @change="updateModelDefaults({ enableImageEnhancement: settings.enableImageEnhancement })"
                >
                <div>
                  <div class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ t('settings.classification.enableImageEnhancement') }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">
                    {{ t('settings.classification.enhancementDescription') }}
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- UI Settings -->
        <div class="glass rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            {{ t('settings.ui.title') }}
          </h2>
          
          <div class="space-y-4">
            <!-- Show Advanced Options -->
            <div>
              <label class="flex items-center space-x-3">
                <input
                  v-model="settings.showAdvancedOptions"
                  type="checkbox"
                  class="checkbox"
                  @change="updateUIPreferences({ showAdvancedOptions: settings.showAdvancedOptions })"
                >
                <div>
                  <div class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ t('settings.ui.showAdvancedOptions') }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">
                    {{ t('settings.ui.advancedDescription') }}
                  </div>
                </div>
              </label>
            </div>

            <!-- Show Processing Details -->
            <div>
              <label class="flex items-center space-x-3">
                <input
                  v-model="settings.showProcessingDetails"
                  type="checkbox"
                  class="checkbox"
                  @change="updateUIPreferences({ showProcessingDetails: settings.showProcessingDetails })"
                >
                <div>
                  <div class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ t('settings.ui.showProcessingDetails') }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">
                    {{ t('settings.ui.processingDescription') }}
                  </div>
                </div>
              </label>
            </div>

            <!-- Enable Notifications -->
            <div>
              <label class="flex items-center space-x-3">
                <input
                  v-model="settings.enableNotifications"
                  type="checkbox"
                  class="checkbox"
                  @change="updateUIPreferences({ enableNotifications: settings.enableNotifications })"
                >
                <div>
                  <div class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ t('settings.ui.enableNotifications') }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">
                    {{ t('settings.ui.notificationsDescription') }}
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- History Settings -->
        <div class="glass rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            {{ t('settings.history.title') }}
          </h2>
          
          <div class="space-y-4">
            <!-- Save History -->
            <div>
              <label class="flex items-center space-x-3">
                <input
                  v-model="settings.saveHistory"
                  type="checkbox"
                  class="checkbox"
                  @change="updateHistoryPreferences({ saveHistory: settings.saveHistory })"
                >
                <div>
                  <div class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ t('settings.history.saveHistory') }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">
                    {{ t('settings.history.saveDescription') }}
                  </div>
                </div>
              </label>
            </div>

            <!-- Max History Items -->
            <div v-if="settings.saveHistory">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {{ t('settings.history.maxHistoryItems') }}
              </label>
              <input
                v-model.number="settings.maxHistoryItems"
                type="number"
                min="0"
                max="1000"
                class="input-field"
                @change="updateHistoryPreferences({ maxHistoryItems: settings.maxHistoryItems })"
              >
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {{ t('settings.history.unlimitedNote') }}
              </p>
            </div>
          </div>
        </div>

        <!-- Data Management -->
        <div class="glass rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            {{ t('settings.dataManagement.title') }}
          </h2>
          
          <div class="space-y-4">
            <!-- Auto Save -->
            <div>
              <label class="flex items-center space-x-3">
                <input
                  v-model="settings.autoSave"
                  type="checkbox"
                  class="checkbox"
                  @change="updateSetting('autoSave', settings.autoSave)"
                >
                <div>
                  <div class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ t('settings.dataManagement.autoSave') }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">
                    {{ t('settings.dataManagement.autoSaveDescription') }}
                  </div>
                </div>
              </label>
            </div>

            <!-- Export/Import Buttons -->
            <div class="flex items-center space-x-4 pt-4">
              <button
                @click="exportSettings"
                class="btn btn-secondary"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {{ t('settings.dataManagement.exportSettings') }}
              </button>
              
              <button
                @click="triggerImport"
                class="btn btn-secondary"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                {{ t('settings.dataManagement.importSettings') }}
              </button>
              
              <input
                ref="importFileInput"
                type="file"
                accept=".json"
                class="hidden"
                @change="handleImport"
              >
            </div>
          </div>
        </div>

        <!-- Reset Settings -->
        <div class="glass rounded-lg p-6 border-red-200 dark:border-red-800">
          <h2 class="text-xl font-semibold text-red-700 dark:text-red-400 mb-4">
            {{ t('settings.reset.title') }}
          </h2>
          
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
            {{ t('settings.reset.description') }}
          </p>
          
          <button
            @click="confirmReset"
            class="btn bg-red-600 hover:bg-red-700 text-white focus:ring-red-500"
          >
            {{ t('settings.reset.button') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSettingsStore } from '@/stores/settings'
import { useClassificationStore } from '@/stores/classification'
import { useErrorStore } from '@/stores/error'
import type { Theme } from '@/stores/settings'

// Stores and i18n
const { t } = useI18n()
const settingsStore = useSettingsStore()
const classificationStore = useClassificationStore()
const errorStore = useErrorStore()

// Template refs
const importFileInput = ref<HTMLInputElement>()

// Computed
const settings = computed(() => settingsStore.settings)
const availableModels = computed(() => classificationStore.availableModels)

// Theme options
const themeOptions = computed(() => [
  {
    value: 'light' as Theme,
    label: t('settings.appearance.themes.light')
  },
  {
    value: 'dark' as Theme,
    label: t('settings.appearance.themes.dark')
  }
])


// Methods
const updateSetting = settingsStore.updateSetting
const updateModelDefaults = settingsStore.updateModelDefaults
const updateUIPreferences = settingsStore.updateUIPreferences
const updateHistoryPreferences = settingsStore.updateHistoryPreferences

const exportSettings = () => {
  settingsStore.exportSettings()
}

const triggerImport = () => {
  importFileInput.value?.click()
}

const handleImport = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  try {
    await settingsStore.importSettings(file)
    
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'success',
        title: t('settings.messages.importComplete'),
        message: t('settings.messages.importSuccess')
      }
    }))
  } catch (error) {
    console.error('Settings import failed:', error)
    errorStore.handleSystemError(t('settings.messages.importFailed'))
  }
  
  // Reset file input
  target.value = ''
}

const confirmReset = () => {
  if (confirm(t('settings.reset.confirm'))) {
    settingsStore.resetSettings()
    
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'info',
        title: t('settings.messages.resetComplete'),
        message: t('settings.messages.resetSuccess')
      }
    }))
  }
}
</script>

<style scoped>
.glass {
  @apply bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700;
}

.input-field {
  @apply block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500;
}

.checkbox {
  @apply w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600;
}

.btn {
  @apply inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors;
}

.btn-secondary {
  @apply text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 focus:ring-gray-500;
}

/* Custom range input styling */
input[type="range"] {
  @apply w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer;
}

input[type="range"]::-webkit-slider-thumb {
  @apply appearance-none w-4 h-4 bg-primary-600 rounded-full cursor-pointer;
}

input[type="range"]::-moz-range-thumb {
  @apply w-4 h-4 bg-primary-600 rounded-full cursor-pointer border-0;
}
</style>