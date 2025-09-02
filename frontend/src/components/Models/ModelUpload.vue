<template>
  <div class="model-upload-container">
    <!-- Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        {{ t('models.upload.title') }}
      </h2>
      <p class="text-gray-600 dark:text-gray-300">
        {{ t('models.upload.description') }}
      </p>
    </div>

    <!-- Upload Form -->
    <div class="glass rounded-2xl p-6 mb-6">
      <form @submit.prevent="handleUpload" class="space-y-6">
        <!-- Model Name -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('models.upload.form.name') }}
          </label>
          <input
            v-model="form.name"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg 
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                   focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            :placeholder="t('models.upload.form.namePlaceholder')"
          >
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('models.upload.form.description') }}
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg 
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                   focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            :placeholder="t('models.upload.form.descriptionPlaceholder')"
          ></textarea>
        </div>

        <!-- Model Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('models.upload.form.type') }}
          </label>
          <select
            v-model="form.modelType"
            required
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg 
                   bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                   focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">{{ t('models.upload.form.selectType') }}</option>
            <option value="tensorflow">TensorFlow (.h5, .hdf5)</option>
            <option value="pytorch">PyTorch (.pth, .pt)</option>
          </select>
        </div>

        <!-- Classes -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('models.upload.form.classes') }}
          </label>
          <div class="space-y-3">
            <div
              v-for="(className, index) in form.classes"
              :key="index"
              class="flex items-center space-x-2"
            >
              <input
                v-model="form.classes[index]"
                type="text"
                required
                class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                       bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                       focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                :placeholder="t('models.upload.form.classPlaceholder', { index: index + 1 })"
              >
              <button
                v-if="form.classes.length > 1"
                type="button"
                @click="removeClass(index)"
                class="p-2 text-red-500 hover:text-red-700"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <button
              type="button"
              @click="addClass"
              class="flex items-center space-x-2 text-primary-600 hover:text-primary-700"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <span>{{ t('models.upload.form.addClass') }}</span>
            </button>
          </div>
        </div>

        <!-- File Upload -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('models.upload.form.file') }}
          </label>
          <div
            @drop="handleDrop"
            @dragover.prevent
            @dragenter.prevent
            class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center
                   hover:border-primary-500 dark:hover:border-primary-400 transition-colors"
            :class="{ 'border-primary-500 bg-primary-50 dark:bg-primary-900/20': isDragging }"
          >
            <div v-if="!selectedFile">
              <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="text-gray-600 dark:text-gray-400 mb-2">
                {{ t('models.upload.form.dropFile') }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-500">
                {{ t('models.upload.form.fileFormats') }}
              </p>
              <input
                ref="fileInput"
                type="file"
                @change="handleFileSelect"
                accept=".h5,.hdf5,.pb,.pth,.pt"
                class="hidden"
              >
              <button
                type="button"
                @click="$refs.fileInput.click()"
                class="mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                {{ t('models.upload.form.selectFile') }}
              </button>
            </div>
            <div v-else class="text-left">
              <div class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-900 dark:text-white">
                    {{ selectedFile.name }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ formatFileSize(selectedFile.size) }}
                  </p>
                </div>
                <button
                  type="button"
                  @click="removeFile"
                  class="p-2 text-red-500 hover:text-red-700"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="resetForm"
            class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50
                   dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
          >
            {{ t('models.upload.form.reset') }}
          </button>
          <button
            type="submit"
            :disabled="!canSubmit || uploading"
            class="px-6 py-3 bg-gradient-to-r from-primary-500 to-secondary-500 text-white rounded-lg
                   hover:from-primary-600 hover:to-secondary-600 disabled:opacity-50 disabled:cursor-not-allowed
                   flex items-center space-x-2"
          >
            <div v-if="uploading" class="spinner-small"></div>
            <span>
              {{ uploading ? t('models.upload.form.uploading') : t('models.upload.form.upload') }}
            </span>
          </button>
        </div>
      </form>
    </div>

    <!-- Upload Progress -->
    <div v-if="uploading" class="glass rounded-xl p-4 mb-6">
      <div class="flex items-center space-x-3">
        <div class="spinner"></div>
        <div>
          <p class="font-medium text-gray-900 dark:text-white">
            {{ t('models.upload.progress.uploading') }}
          </p>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ t('models.upload.progress.description') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Composables
const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

// Reactive state
const form = ref({
  name: '',
  description: '',
  modelType: '',
  classes: ['']
})

const selectedFile = ref<File | null>(null)
const uploading = ref(false)
const isDragging = ref(false)

// Computed
const canSubmit = computed(() => {
  return form.value.name && 
         form.value.modelType && 
         selectedFile.value &&
         form.value.classes.length > 0 &&
         form.value.classes.every(cls => cls.trim())
})

// Methods
const addClass = () => {
  form.value.classes.push('')
}

const removeClass = (index: number) => {
  if (form.value.classes.length > 1) {
    form.value.classes.splice(index, 1)
  }
}

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    selectedFile.value = input.files[0]
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = false
  
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    selectedFile.value = event.dataTransfer.files[0]
  }
}

const removeFile = () => {
  selectedFile.value = null
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const resetForm = () => {
  form.value = {
    name: '',
    description: '',
    modelType: '',
    classes: ['']
  }
  selectedFile.value = null
}

const handleUpload = async () => {
  if (!canSubmit.value) return
  
  uploading.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value!)
    formData.append('name', form.value.name)
    formData.append('model_type', form.value.modelType)
    formData.append('classes', JSON.stringify(form.value.classes.filter(cls => cls.trim())))
    
    if (form.value.description) {
      formData.append('description', form.value.description)
    }

    const response = await fetch('/api/v1/models/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
      },
      body: formData
    })

    if (response.ok) {
      const result = await response.json()
      
      // Show success message
      window.dispatchEvent(new CustomEvent('app:toast', {
        detail: {
          type: 'success',
          title: t('models.upload.success.title'),
          message: t('models.upload.success.message', { name: form.value.name })
        }
      }))
      
      // Reset form
      resetForm()
      
      // Navigate to models list
      router.push('/models')
    } else {
      const error = await response.json()
      throw new Error(error.detail || 'Upload failed')
    }
  } catch (error) {
    console.error('Model upload error:', error)
    
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'error',
        title: t('models.upload.error.title'),
        message: error instanceof Error ? error.message : t('models.upload.error.message')
      }
    }))
  } finally {
    uploading.value = false
  }
}

// Check authentication on mount
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
  }
})
</script>

<style scoped>
.spinner-small {
  @apply w-4 h-4 border-2 border-white border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

.spinner {
  @apply w-6 h-6 border-2 border-primary-600 border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>