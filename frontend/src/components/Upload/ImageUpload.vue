<template>
  <div class="space-y-6">
    <!-- Upload Area -->
    <div
      @drop="handleDrop"
      @dragover="handleDragOver"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      class="relative border-2 border-dashed rounded-xl p-8 transition-all duration-200 cursor-pointer"
      :class="[
        isDragging
          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 scale-105'
          : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500 hover:bg-gray-50 dark:hover:bg-gray-800/50'
      ]"
      @click="triggerFileInput"
    >
      <!-- Upload Icon and Text -->
      <div class="text-center">
        <div class="mx-auto w-16 h-16 mb-4">
          <svg
            class="w-full h-full transition-colors"
            :class="isDragging ? 'text-primary-500' : 'text-gray-400'"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>
        
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          {{ isDragging ? t('classification.upload.dragActive') : t('classification.upload.title') }}
        </h3>
        
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          {{ isDragging ? t('classification.upload.dragActive') : t('classification.upload.description') }}
        </p>
        
        <div class="text-sm text-gray-500 dark:text-gray-400">
          <p>{{ t('classification.upload.formats') }}</p>
          <p>{{ t('classification.upload.maxSize') }}</p>
        </div>
      </div>
      
      <!-- Hidden File Input -->
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleFileSelect"
      >
      
      <!-- Upload Progress Overlay -->
      <Transition
        name="fade"
        enter-active-class="transition-opacity duration-300"
        leave-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isUploading"
          class="absolute inset-0 bg-white/90 dark:bg-gray-900/90 rounded-xl flex items-center justify-center"
        >
          <div class="text-center">
            <div class="spinner mb-4"></div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">
              {{ t('classification.upload.uploading', { progress: uploadProgress }) }}
            </p>
            <div class="w-48 h-2 bg-gray-200 dark:bg-gray-700 rounded-full mt-2">
              <div
                class="h-full bg-primary-500 rounded-full transition-all duration-300"
                :style="{ width: `${uploadProgress}%` }"
              ></div>
            </div>
          </div>
        </div>
      </Transition>
    </div>

    <!-- File List -->
    <div v-if="hasFiles" class="space-y-4">
      <div class="flex items-center justify-between">
        <h4 class="text-lg font-semibold text-gray-900 dark:text-white">
          {{ t('classification.upload.selectedFile') }}
        </h4>
        <button
          @click="clearAllFiles"
          class="text-sm text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
        >
          {{ t('classification.upload.removeAll') }}
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="(file, index) in files"
          :key="`${file.name}-${file.size}`"
          class="glass rounded-lg p-4 relative group"
        >
          <!-- Image Preview -->
          <div class="aspect-square mb-3 bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden">
            <img
              :src="getFilePreview(file)"
              :alt="file.name"
              class="w-full h-full object-cover"
              @load="handleImageLoad"
              @error="handleImageError"
            >
          </div>

          <!-- File Info -->
          <div class="space-y-1">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white truncate" :title="file.name">
              {{ file.name }}
            </h5>
            <p class="text-xs text-gray-600 dark:text-gray-400">
              {{ formatFileSize(file.size) }} • {{ file.type.split('/')[1].toUpperCase() }}
            </p>
          </div>

          <!-- File Actions -->
          <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              @click="removeFile(index)"
              class="p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
              :title="t('common.delete')"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Upload Summary -->
      <div class="glass rounded-lg p-4">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-600 dark:text-gray-400">
            {{ t('classification.upload.totalSize') }}: {{ formatFileSize(totalFileSize) }}
          </div>
          <button
            v-if="canUpload && !isUploading"
            @click="startUpload"
            class="btn btn-primary"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            {{ t('classification.upload.startUpload') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Upload Options -->
    <div v-if="hasFiles" class="glass rounded-lg p-4">
      <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        {{ t('classification.upload.options') }}
      </h4>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Model Selection -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ t('classification.upload.model') }}
          </label>
          <select
            v-model="selectedModel"
            class="input-field"
            @change="updateUploadOptions({ model: selectedModel })"
          >
            <option value="default">デフォルト</option>
            <option v-for="model in availableModels" :key="model.name" :value="model.name">
              {{ model.description || model.name }}
            </option>
          </select>
        </div>

        <!-- Confidence Threshold -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ t('classification.upload.confidenceThreshold') }}: {{ confidenceThreshold }}
          </label>
          <input
            v-model.number="confidenceThreshold"
            type="range"
            min="0"
            max="1"
            step="0.05"
            class="w-full"
            @input="updateUploadOptions({ threshold: confidenceThreshold })"
          >
        </div>

        <!-- Max Results -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ t('classification.upload.maxResults') }}
          </label>
          <input
            v-model.number="maxResults"
            type="number"
            min="1"
            max="20"
            class="input-field"
            @change="updateUploadOptions({ max_results: maxResults })"
          >
        </div>

        <!-- Image Enhancement -->
        <div class="space-y-2">
          <label class="flex items-center space-x-2">
            <input
              v-model="enhanceImage"
              type="checkbox"
              class="checkbox"
              @change="updateUploadOptions({ enhance_image: enhanceImage })"
            >
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ t('classification.upload.enhanceImages') }}
            </span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUploadStore } from '@/stores/upload'
import { useClassificationStore } from '@/stores/classification'
import { useErrorStore } from '@/stores/error'
import { classificationApi } from '@/services/classificationApi'

// Stores and i18n
const { t } = useI18n()
const uploadStore = useUploadStore()
const classificationStore = useClassificationStore()
const errorStore = useErrorStore()

// Template refs
const fileInput = ref<HTMLInputElement>()

// Local state
const selectedModel = ref('default')
const confidenceThreshold = ref(0.5)
const maxResults = ref(5)
const enhanceImage = ref(false)

// Computed from stores
const files = computed(() => uploadStore.files)
const hasFiles = computed(() => uploadStore.hasFiles)
const canUpload = computed(() => uploadStore.canUpload)
const isUploading = computed(() => uploadStore.isUploading)
const isDragging = computed(() => uploadStore.isDragging)
const uploadProgress = computed(() => uploadStore.uploadProgress)
const totalFileSize = computed(() => uploadStore.totalFileSize)
const availableModels = computed(() => classificationStore.availableModels)

// Constants
const maxFileSize = ref(10 * 1024 * 1024) // 10MB

// Drag and drop handlers
const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
}

const handleDragEnter = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  uploadStore.setDragging(true)
}

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  
  // Only stop dragging if we're leaving the drop zone completely
  if (e.currentTarget && e.relatedTarget && 
      !(e.currentTarget as Element).contains(e.relatedTarget as Node)) {
    uploadStore.setDragging(false)
  }
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  uploadStore.setDragging(false)

  const droppedFiles = e.dataTransfer?.files
  if (droppedFiles && droppedFiles.length > 0) {
    // Only accept the first file since we removed batch processing
    addFiles([droppedFiles[0]])
  }
}

// File handling
const triggerFileInput = () => {
  if (!isUploading.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    // Only accept the first file since we removed batch processing
    addFiles([target.files[0]])
    target.value = '' // Reset input to allow selecting same files again
  }
}

const addFiles = (fileList: FileList) => {
  const result = uploadStore.addFiles(fileList)
  
  // Show feedback
  if (result.added > 0) {
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'success',
        title: 'ファイル追加',
        message: `${result.added}個のファイルを追加しました`
      }
    }))
  }
  
  if (result.invalid > 0) {
    errorStore.handleFileError(
      t('classification.upload.unsupportedFilesError', { count: result.invalid })
    )
  }
  
  if (result.duplicates > 0) {
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'warning',
        title: t('common.warning'),
        message: t('classification.upload.duplicatesSkipped', { count: result.duplicates })
      }
    }))
  }
}

const removeFile = (index: number) => {
  uploadStore.removeFile(index)
}

const clearAllFiles = () => {
  uploadStore.clearFiles()
}

// Upload functionality
const startUpload = async () => {
  if (!canUpload.value) return

  try {
    uploadStore.setUploading(true)
    classificationStore.setProcessing(true, t('classification.upload.analyzingImages', { count: files.value.length }))

    // Get upload options
    const options = {
      model: selectedModel.value,
      threshold: confidenceThreshold.value,
      max_results: maxResults.value,
      enhance_image: enhanceImage.value
    }

    // Single file upload only
    const results = [await classificationApi.classifyImage(
      files.value[0],
      options,
      (progress) => uploadStore.setUploadProgress(progress)
    )]

    // Store results
    uploadStore.setResults(results)
    classificationStore.setCurrentResults(results)

    // Emit success event
    emits('uploadComplete', results)

  } catch (error) {
    console.error('Upload failed:', error)
    errorStore.handleHttpError(error as any, 'Image upload')
  } finally {
    uploadStore.setUploading(false)
    classificationStore.setProcessing(false)
  }
}

// Image preview
const getFilePreview = (file: File): string => {
  return URL.createObjectURL(file)
}

const handleImageLoad = (e: Event) => {
  // Cleanup object URL after loading
  const img = e.target as HTMLImageElement
  if (img.src.startsWith('blob:')) {
    // URL.revokeObjectURL(img.src) // Don't revoke immediately, may cause display issues
  }
}

const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
}

// Options update
const updateUploadOptions = uploadStore.updateUploadOptions

// File size formatting
const formatFileSize = uploadStore.formatFileSize

// Events
const emits = defineEmits<{
  uploadComplete: [results: any[]]
}>()

// Lifecycle
onMounted(async () => {
  // Load available models
  try {
    const modelsResponse = await classificationApi.getModels()
    classificationStore.setAvailableModels(modelsResponse.available_models)
  } catch (error) {
    console.warn('Failed to load models:', error)
  }

  // Prevent default drag behaviors on document
  const preventDefaults = (e: Event) => {
    e.preventDefault()
    e.stopPropagation()
  }

  document.addEventListener('dragover', preventDefaults)
  document.addEventListener('drop', preventDefaults)
})

onUnmounted(() => {
  // Cleanup object URLs
  files.value.forEach(file => {
    const preview = getFilePreview(file)
    if (preview.startsWith('blob:')) {
      URL.revokeObjectURL(preview)
    }
  })

  // Remove document event listeners
  const preventDefaults = (e: Event) => {
    e.preventDefault()
    e.stopPropagation()
  }

  document.removeEventListener('dragover', preventDefaults)
  document.removeEventListener('drop', preventDefaults)
})
</script>

<style scoped>
.spinner {
  @apply w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin;
}

.checkbox {
  @apply w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600;
}

.input-field {
  @apply block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500;
}

.btn {
  @apply inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors;
}

.btn-primary {
  @apply text-white bg-primary-600 hover:bg-primary-700 focus:ring-primary-500;
}

.glass {
  @apply bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-200 dark:border-gray-700;
}
</style>