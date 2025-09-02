/**
 * Image optimization utilities for performance enhancement
 */

export interface OptimizedImage {
  file: File
  originalSize: number
  optimizedSize: number
  compressionRatio: number
  width: number
  height: number
}

export interface OptimizationOptions {
  maxWidth?: number
  maxHeight?: number
  quality?: number
  format?: 'jpeg' | 'webp' | 'png'
  enableResize?: boolean
  enableCompression?: boolean
}

export class ImageOptimizer {
  private static readonly DEFAULT_OPTIONS: Required<OptimizationOptions> = {
    maxWidth: 1024,
    maxHeight: 1024,
    quality: 0.85,
    format: 'jpeg',
    enableResize: true,
    enableCompression: true
  }

  /**
   * Optimize a single image file
   */
  static async optimizeImage(
    file: File, 
    options: OptimizationOptions = {}
  ): Promise<OptimizedImage> {
    const opts = { ...this.DEFAULT_OPTIONS, ...options }
    
    // Skip optimization for small files or if disabled
    if (file.size < 100 * 1024 || (!opts.enableResize && !opts.enableCompression)) {
      return {
        file,
        originalSize: file.size,
        optimizedSize: file.size,
        compressionRatio: 1,
        width: 0,
        height: 0
      }
    }

    return new Promise((resolve, reject) => {
      const img = new Image()
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')

      if (!ctx) {
        reject(new Error('Canvas context not available'))
        return
      }

      img.onload = () => {
        try {
          let { width, height } = img

          // Resize if needed
          if (opts.enableResize && (width > opts.maxWidth || height > opts.maxHeight)) {
            const ratio = Math.min(opts.maxWidth / width, opts.maxHeight / height)
            width = Math.round(width * ratio)
            height = Math.round(height * ratio)
          }

          canvas.width = width
          canvas.height = height

          // Draw and compress
          ctx.drawImage(img, 0, 0, width, height)
          
          canvas.toBlob(
            (blob) => {
              if (!blob) {
                reject(new Error('Failed to compress image'))
                return
              }

              const optimizedFile = new File([blob], file.name, {
                type: blob.type,
                lastModified: file.lastModified
              })

              resolve({
                file: optimizedFile,
                originalSize: file.size,
                optimizedSize: blob.size,
                compressionRatio: blob.size / file.size,
                width,
                height
              })
            },
            `image/${opts.format}`,
            opts.enableCompression ? opts.quality : 1.0
          )
        } catch (error) {
          reject(error)
        }
      }

      img.onerror = () => reject(new Error('Failed to load image'))
      img.src = URL.createObjectURL(file)
    })
  }

  /**
   * Optimize multiple images concurrently
   */
  static async optimizeImages(
    files: File[],
    options: OptimizationOptions = {},
    onProgress?: (completed: number, total: number) => void
  ): Promise<OptimizedImage[]> {
    const results: OptimizedImage[] = []
    let completed = 0

    const promises = files.map(async (file) => {
      try {
        const result = await this.optimizeImage(file, options)
        completed++
        onProgress?.(completed, files.length)
        return result
      } catch (error) {
        console.error(`Failed to optimize ${file.name}:`, error)
        completed++
        onProgress?.(completed, files.length)
        // Return original file if optimization fails
        return {
          file,
          originalSize: file.size,
          optimizedSize: file.size,
          compressionRatio: 1,
          width: 0,
          height: 0
        }
      }
    })

    return Promise.all(promises)
  }

  /**
   * Generate image thumbnail for preview
   */
  static async generateThumbnail(file: File, size: number = 150): Promise<string> {
    return new Promise((resolve, reject) => {
      const img = new Image()
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')

      if (!ctx) {
        reject(new Error('Canvas context not available'))
        return
      }

      img.onload = () => {
        const { width, height } = img
        const ratio = Math.min(size / width, size / height)
        const newWidth = width * ratio
        const newHeight = height * ratio

        canvas.width = newWidth
        canvas.height = newHeight
        
        ctx.drawImage(img, 0, 0, newWidth, newHeight)
        resolve(canvas.toDataURL('image/jpeg', 0.8))
      }

      img.onerror = () => reject(new Error('Failed to load image'))
      img.src = URL.createObjectURL(file)
    })
  }

  /**
   * Check if WebP format is supported
   */
  static isWebPSupported(): boolean {
    const canvas = document.createElement('canvas')
    canvas.width = 1
    canvas.height = 1
    return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0
  }

  /**
   * Get optimal format for the browser
   */
  static getOptimalFormat(): 'webp' | 'jpeg' {
    return this.isWebPSupported() ? 'webp' : 'jpeg'
  }

  /**
   * Calculate total size reduction
   */
  static calculateSizeReduction(optimizedImages: OptimizedImage[]): {
    originalTotal: number
    optimizedTotal: number
    reductionBytes: number
    reductionPercentage: number
  } {
    const originalTotal = optimizedImages.reduce((sum, img) => sum + img.originalSize, 0)
    const optimizedTotal = optimizedImages.reduce((sum, img) => sum + img.optimizedSize, 0)
    const reductionBytes = originalTotal - optimizedTotal
    const reductionPercentage = originalTotal > 0 ? (reductionBytes / originalTotal) * 100 : 0

    return {
      originalTotal,
      optimizedTotal,
      reductionBytes,
      reductionPercentage
    }
  }
}

/**
 * Format file size for display
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Validate image file
 */
export function validateImageFile(file: File): { valid: boolean; error?: string } {
  // Check if it's an image
  if (!file.type.startsWith('image/')) {
    return { valid: false, error: 'ファイルは画像である必要があります' }
  }

  // Check file size (10MB limit)
  const maxSize = 10 * 1024 * 1024
  if (file.size > maxSize) {
    return { valid: false, error: `ファイルサイズは${formatFileSize(maxSize)}以下である必要があります` }
  }

  // Check supported formats
  const supportedFormats = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp']
  if (!supportedFormats.includes(file.type)) {
    return { valid: false, error: '対応していない画像形式です' }
  }

  return { valid: true }
}

/**
 * Create image preview URL with automatic cleanup
 */
export class ImagePreview {
  private static previewUrls = new Set<string>()

  static create(file: File): string {
    const url = URL.createObjectURL(file)
    this.previewUrls.add(url)
    return url
  }

  static cleanup(url?: string): void {
    if (url && this.previewUrls.has(url)) {
      URL.revokeObjectURL(url)
      this.previewUrls.delete(url)
    }
  }

  static cleanupAll(): void {
    this.previewUrls.forEach(url => URL.revokeObjectURL(url))
    this.previewUrls.clear()
  }
}

/**
 * Image processing performance monitor
 */
export class PerformanceMonitor {
  private static metrics: Array<{
    operation: string
    duration: number
    fileSize: number
    timestamp: number
  }> = []

  static startTiming(operation: string): () => void {
    const start = performance.now()
    
    return (fileSize: number = 0) => {
      const duration = performance.now() - start
      this.metrics.push({
        operation,
        duration,
        fileSize,
        timestamp: Date.now()
      })

      // Keep only last 100 metrics
      if (this.metrics.length > 100) {
        this.metrics = this.metrics.slice(-100)
      }
    }
  }

  static getAverageTime(operation: string): number {
    const operationMetrics = this.metrics.filter(m => m.operation === operation)
    if (operationMetrics.length === 0) return 0
    
    const total = operationMetrics.reduce((sum, m) => sum + m.duration, 0)
    return total / operationMetrics.length
  }

  static getThroughput(operation: string): number {
    const operationMetrics = this.metrics.filter(m => m.operation === operation)
    if (operationMetrics.length === 0) return 0
    
    const totalSize = operationMetrics.reduce((sum, m) => sum + m.fileSize, 0)
    const totalTime = operationMetrics.reduce((sum, m) => sum + m.duration, 0)
    
    return totalSize / (totalTime / 1000) // bytes per second
  }

  static getMetrics() {
    return {
      optimization: {
        averageTime: this.getAverageTime('optimization'),
        throughput: this.getThroughput('optimization')
      },
      classification: {
        averageTime: this.getAverageTime('classification'),
        throughput: this.getThroughput('classification')
      },
      total: this.metrics.length
    }
  }
}