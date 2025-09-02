import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ClassificationResult, UploadOptions } from '@/types/api'

export const useUploadStore = defineStore('upload', () => {
  // State
  const files = ref<File[]>([])
  const uploadProgress = ref(0)
  const isUploading = ref(false)
  const isDragging = ref(false)
  const results = ref<ClassificationResult[]>([])
  const uploadOptions = ref<UploadOptions>({
    model: 'default',
    threshold: 0.5,
    max_results: 5,
    enhance_image: false
  })

  // Computed
  const hasFiles = computed(() => files.value.length > 0)
  const canUpload = computed(() => hasFiles.value && !isUploading.value)
  const totalFileSize = computed(() => 
    files.value.reduce((total, file) => total + file.size, 0)
  )

  // Actions
  const addFiles = (newFiles: FileList | File[]) => {
    const fileArray = Array.from(newFiles)
    
    // Validate and filter files
    const validFiles = fileArray.filter(file => {
      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/bmp']
      const maxSize = 10 * 1024 * 1024 // 10MB
      
      return allowedTypes.includes(file.type) && file.size <= maxSize && file.size > 0
    })

    // Remove duplicates based on name and size
    const existingFiles = new Set(files.value.map(f => `${f.name}-${f.size}`))
    const uniqueNewFiles = validFiles.filter(f => !existingFiles.has(`${f.name}-${f.size}`))
    
    files.value.push(...uniqueNewFiles)
    
    // Return validation results
    return {
      added: uniqueNewFiles.length,
      invalid: fileArray.length - validFiles.length,
      duplicates: validFiles.length - uniqueNewFiles.length
    }
  }

  const removeFile = (index: number) => {
    files.value.splice(index, 1)
  }

  const clearFiles = () => {
    files.value = []
    results.value = []
    uploadProgress.value = 0
  }

  const setDragging = (dragging: boolean) => {
    isDragging.value = dragging
  }

  const setUploadProgress = (progress: number) => {
    uploadProgress.value = Math.max(0, Math.min(100, progress))
  }

  const setUploading = (uploading: boolean) => {
    isUploading.value = uploading
    if (!uploading) {
      uploadProgress.value = 0
    }
  }

  const setResults = (newResults: ClassificationResult[]) => {
    results.value = newResults
  }

  const addResult = (result: ClassificationResult) => {
    results.value.push(result)
  }

  const updateUploadOptions = (options: Partial<UploadOptions>) => {
    uploadOptions.value = { ...uploadOptions.value, ...options }
  }

  const resetUploadOptions = () => {
    uploadOptions.value = {
      model: 'default',
      threshold: 0.5,
      max_results: 5,
      enhance_image: false
    }
  }

  // File validation helpers
  const validateFile = (file: File) => {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/bmp']
    const maxSize = 10 * 1024 * 1024 // 10MB

    const errors: string[] = []

    if (!allowedTypes.includes(file.type)) {
      errors.push(`サポートされていないファイル形式です: ${file.type}`)
    }

    if (file.size > maxSize) {
      errors.push(`ファイルサイズが大きすぎます: ${(file.size / 1024 / 1024).toFixed(2)}MB`)
    }

    if (file.size === 0) {
      errors.push('空のファイルは処理できません')
    }

    return {
      valid: errors.length === 0,
      errors
    }
  }

  const validateAllFiles = () => {
    const validationResults = files.value.map(file => ({
      file,
      ...validateFile(file)
    }))

    return {
      valid: validationResults.every(result => result.valid),
      results: validationResults
    }
  }

  // Format file size for display
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return {
    // State
    files,
    uploadProgress,
    isUploading,
    isDragging,
    results,
    uploadOptions,

    // Computed
    hasFiles,
    canUpload,
    totalFileSize,

    // Actions
    addFiles,
    removeFile,
    clearFiles,
    setDragging,
    setUploadProgress,
    setUploading,
    setResults,
    addResult,
    updateUploadOptions,
    resetUploadOptions,
    validateFile,
    validateAllFiles,
    formatFileSize
  }
})