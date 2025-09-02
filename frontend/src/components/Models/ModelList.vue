<template>
  <div class="model-list-container">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {{ t('models.list.title') }}
        </h2>
        <p class="text-gray-600 dark:text-gray-300">
          {{ t('models.list.description') }}
        </p>
      </div>
      <RouterLink
        to="/models/upload"
        class="px-4 py-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white rounded-lg
               hover:from-primary-600 hover:to-secondary-600 flex items-center space-x-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        <span>{{ t('models.list.upload') }}</span>
      </RouterLink>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="glass rounded-xl p-8 text-center">
      <div class="spinner mx-auto mb-4"></div>
      <p class="text-gray-600 dark:text-gray-400">
        {{ t('models.list.loading') }}
      </p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="glass rounded-xl p-6 border border-red-200 dark:border-red-800">
      <div class="flex items-center space-x-3 text-red-600 dark:text-red-400">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="font-medium">{{ t('models.list.error.title') }}</h3>
          <p class="text-sm">{{ error }}</p>
        </div>
      </div>
      <button
        @click="loadModels"
        class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
      >
        {{ t('models.list.retry') }}
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="models.length === 0" class="glass rounded-xl p-8 text-center">
      <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
        {{ t('models.list.empty.title') }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        {{ t('models.list.empty.description') }}
      </p>
      <RouterLink
        to="/models/upload"
        class="inline-flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        <span>{{ t('models.list.upload') }}</span>
      </RouterLink>
    </div>

    <!-- Models Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div
        v-for="model in models"
        :key="model.model_id"
        class="glass rounded-xl p-6 hover:shadow-lg transition-all"
      >
        <!-- Status Badge -->
        <div class="flex justify-between items-start mb-4">
          <div>
            <span
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="getStatusClass(model.status)"
            >
              {{ t(`models.status.${model.status}`) }}
            </span>
          </div>
          <div class="flex space-x-2">
            <button
              v-if="model.status === 'uploaded'"
              @click="validateModel(model.model_id)"
              :disabled="validating[model.model_id]"
              class="p-2 text-blue-600 hover:text-blue-700 disabled:opacity-50"
              :title="t('models.list.validate')"
            >
              <div v-if="validating[model.model_id]" class="spinner-small"></div>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
            <button
              @click="deleteModel(model.model_id, model.name)"
              :disabled="deleting[model.model_id]"
              class="p-2 text-red-600 hover:text-red-700 disabled:opacity-50"
              :title="t('models.list.delete')"
            >
              <div v-if="deleting[model.model_id]" class="spinner-small"></div>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Model Info -->
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">
            {{ model.name }}
          </h3>
          <p v-if="model.description" class="text-sm text-gray-600 dark:text-gray-400 mb-2">
            {{ model.description }}
          </p>
          <div class="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
            <span class="flex items-center space-x-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              <span>{{ model.model_type === 'tensorflow' ? 'TensorFlow' : 'PyTorch' }}</span>
            </span>
            <span class="flex items-center space-x-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              <span>{{ formatFileSize(model.file_size) }}</span>
            </span>
          </div>
        </div>

        <!-- Classes -->
        <div class="mb-4">
          <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('models.list.classes') }} ({{ model.classes.length }})
          </h4>
          <div class="flex flex-wrap gap-1">
            <span
              v-for="(cls, index) in model.classes.slice(0, 5)"
              :key="index"
              class="inline-block px-2 py-1 bg-gray-100 dark:bg-gray-700 text-xs text-gray-700 dark:text-gray-300 rounded"
            >
              {{ cls }}
            </span>
            <span
              v-if="model.classes.length > 5"
              class="inline-block px-2 py-1 bg-gray-200 dark:bg-gray-600 text-xs text-gray-600 dark:text-gray-400 rounded"
            >
              +{{ model.classes.length - 5 }}
            </span>
          </div>
        </div>

        <!-- Validation Error -->
        <div v-if="model.validation_error" class="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div class="flex items-start space-x-2">
            <svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h5 class="text-sm font-medium text-red-800 dark:text-red-200">
                {{ t('models.list.validationError') }}
              </h5>
              <p class="text-sm text-red-700 dark:text-red-300">
                {{ model.validation_error }}
              </p>
            </div>
          </div>
        </div>

        <!-- Upload Date -->
        <div class="text-xs text-gray-500 dark:text-gray-400">
          {{ t('models.list.uploadedOn') }}: {{ formatDate(model.created_at) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Types
interface CustomModel {
  model_id: string
  name: string
  description?: string
  model_type: string
  classes: string[]
  status: string
  file_size: number
  created_at: string
  validation_error?: string
}

// Composables
const { t, locale } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

// Reactive state
const models = ref<CustomModel[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const validating = ref<Record<string, boolean>>({})
const deleting = ref<Record<string, boolean>>({})

// Methods
const loadModels = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await fetch('/api/v1/models/custom', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      }
    })

    if (response.ok) {
      models.value = await response.json()
    } else {
      throw new Error('Failed to load models')
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error'
  } finally {
    loading.value = false
  }
}

const validateModel = async (modelId: string) => {
  validating.value[modelId] = true

  try {
    const response = await fetch(`/api/v1/models/${modelId}/validate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      }
    })

    if (response.ok) {
      // Reload models to get updated status
      await loadModels()
      
      window.dispatchEvent(new CustomEvent('app:toast', {
        detail: {
          type: 'success',
          title: t('models.list.validation.success.title'),
          message: t('models.list.validation.success.message')
        }
      }))
    } else {
      const error = await response.json()
      throw new Error(error.detail || 'Validation failed')
    }
  } catch (err) {
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'error',
        title: t('models.list.validation.error.title'),
        message: err instanceof Error ? err.message : t('models.list.validation.error.message')
      }
    }))
  } finally {
    validating.value[modelId] = false
  }
}

const deleteModel = async (modelId: string, modelName: string) => {
  if (!confirm(t('models.list.delete.confirm', { name: modelName }))) {
    return
  }

  deleting.value[modelId] = true

  try {
    const response = await fetch(`/api/v1/models/${modelId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      }
    })

    if (response.ok) {
      models.value = models.value.filter(m => m.model_id !== modelId)
      
      window.dispatchEvent(new CustomEvent('app:toast', {
        detail: {
          type: 'success',
          title: t('models.list.delete.success.title'),
          message: t('models.list.delete.success.message', { name: modelName })
        }
      }))
    } else {
      const error = await response.json()
      throw new Error(error.detail || 'Delete failed')
    }
  } catch (err) {
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'error',
        title: t('models.list.delete.error.title'),
        message: err instanceof Error ? err.message : t('models.list.delete.error.message')
      }
    }))
  } finally {
    deleting.value[modelId] = false
  }
}

const getStatusClass = (status: string): string => {
  const classes = {
    uploaded: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300',
    active: 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300',
    error: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300',
    validating: 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300'
  }
  return classes[status as keyof typeof classes] || classes.uploaded
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

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

// Lifecycle
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  loadModels()
})
</script>

<style scoped>
.spinner {
  @apply w-6 h-6 border-2 border-primary-600 border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

.spinner-small {
  @apply w-4 h-4 border-2 border-current border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>