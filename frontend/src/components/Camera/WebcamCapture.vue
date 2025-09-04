<template>
  <div class="webcam-capture-container">
    <!-- Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        ウェブカメラ分類
      </h2>
      <p class="text-gray-600 dark:text-gray-300">
        ウェブカメラで撮影した画像をリアルタイムで分類できます
      </p>
    </div>

    <!-- Camera Setup -->
    <div v-if="!cameraReady && !error" class="glass rounded-2xl p-8 text-center">
      <div class="spinner mx-auto mb-4"></div>
      <p class="text-gray-600 dark:text-gray-400">
        カメラを準備中...
      </p>
      <p class="text-sm text-gray-500 dark:text-gray-500 mt-2">
        ブラウザがカメラアクセスの許可を求める場合があります
      </p>
    </div>

    <!-- Camera Error -->
    <div v-else-if="error" class="glass rounded-xl p-6 border border-red-200 dark:border-red-800">
      <div class="flex items-center space-x-3 text-red-600 dark:text-red-400">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="font-medium">カメラエラー</h3>
          <p class="text-sm">{{ error }}</p>
        </div>
      </div>
      <button
        @click="initializeCamera"
        class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
      >
        再試行
      </button>
    </div>

    <!-- Camera Interface -->
    <div v-else-if="cameraReady" class="glass rounded-2xl p-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Camera Preview -->
        <div class="relative">
          <div class="aspect-w-4 aspect-h-3 bg-black rounded-lg overflow-hidden">
            <video
              ref="videoElement"
              autoplay
              playsinline
              muted
              class="w-full h-full object-cover"
            ></video>
            
            <!-- Capture Overlay -->
            <div v-if="capturing" class="absolute inset-0 bg-white/20 flex items-center justify-center">
              <div class="w-16 h-16 border-4 border-white rounded-full animate-ping"></div>
            </div>
          </div>
          
          <!-- Camera Controls -->
          <div class="mt-4 flex justify-center space-x-4">
            <button
              @click="captureImage"
              :disabled="capturing || classifying"
              class="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 
                     disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>{{ capturing ? '撮影中...' : '撮影' }}</span>
            </button>
            
            <button
              @click="toggleAutoCapture"
              :class="[
                'px-4 py-3 rounded-lg flex items-center space-x-2 transition-colors',
                autoCapture 
                  ? 'bg-green-600 text-white hover:bg-green-700' 
                  : 'bg-gray-600 text-white hover:bg-gray-700'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>{{ autoCapture ? '自動撮影停止' : '自動撮影開始' }}</span>
            </button>
          </div>

          <!-- Auto Capture Settings -->
          <div v-if="autoCapture" class="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-blue-800 dark:text-blue-200">
                撮影間隔
              </span>
              <select
                v-model.number="autoCaptureInterval"
                @change="restartAutoCapture"
                class="px-2 py-1 text-sm border border-blue-300 dark:border-blue-600 rounded bg-white dark:bg-gray-800"
              >
                <option :value="1000">1秒</option>
                <option :value="2000">2秒</option>
                <option :value="3000">3秒</option>
                <option :value="5000">5秒</option>
              </select>
            </div>
            <div class="mt-2 text-xs text-blue-700 dark:text-blue-300">
              次回撮影まで: {{ Math.ceil(countdown / 1000) }}秒
            </div>
          </div>
        </div>

        <!-- Results Panel -->
        <div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
            {{ $t('classification.results.title') }}
          </h3>
          
          <!-- Classification in Progress -->
          <div v-if="classifying" class="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="spinner-small"></div>
              <span class="text-blue-800 dark:text-blue-200">分類中...</span>
            </div>
          </div>

          <!-- Latest Results -->
          <div v-else-if="latestResult" class="space-y-4">
            <!-- Captured Image -->
            <div class="relative">
              <img
                :src="latestResult.imageUrl"
                alt="Captured"
                class="w-full h-48 object-cover rounded-lg"
              >
              <div class="absolute top-2 right-2 px-2 py-1 bg-black/70 text-white text-xs rounded">
                {{ formatDate(latestResult.timestamp) }}
              </div>
            </div>

            <!-- Classification Results -->
            <div class="space-y-2">
              <div
                v-for="(prediction, index) in latestResult.predictions.slice(0, 5)"
                :key="index"
                class="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <span class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ prediction }}
                </span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      class="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
                      :style="{ width: `${latestResult.confidence_scores[index] * 100}%` }"
                    ></div>
                  </div>
                  <span class="text-sm font-medium text-gray-600 dark:text-gray-400 w-12 text-right">
                    {{ Math.round(latestResult.confidence_scores[index] * 100) }}%
                  </span>
                </div>
              </div>
            </div>

            <!-- Metadata -->
            <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500">{{ $t('classification.results.processingTime') }}:</span>
                  <span class="ml-1 text-gray-900 dark:text-white">{{ latestResult.processing_time }}ms</span>
                </div>
                <div>
                  <span class="text-gray-500">{{ $t('classification.results.modelUsed') }}:</span>
                  <span class="ml-1 text-gray-900 dark:text-white">{{ latestResult.model_used }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- No Results Yet -->
          <div v-else class="text-center py-8">
            <svg class="mx-auto w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <p class="text-gray-500 dark:text-gray-400">
              撮影ボタンを押して画像を分類してみましょう
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Hidden Canvas -->
    <canvas ref="canvasElement" class="hidden"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

interface ClassificationResult {
  imageUrl: string
  predictions: string[]
  confidence_scores: number[]
  processing_time: number
  model_used: string
  timestamp: Date
}

const authStore = useAuthStore()

const videoElement = ref<HTMLVideoElement>()
const canvasElement = ref<HTMLCanvasElement>()
const cameraReady = ref(false)
const error = ref<string | null>(null)
const capturing = ref(false)
const classifying = ref(false)
const autoCapture = ref(false)
const autoCaptureInterval = ref(3000)
const countdown = ref(0)
const latestResult = ref<ClassificationResult | null>(null)

let mediaStream: MediaStream | null = null
let autoCaptureTimer: number | null = null
let countdownTimer: number | null = null

const initializeCamera = async () => {
  error.value = null
  cameraReady.value = false

  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        facingMode: 'environment'
      }
    })

    if (videoElement.value) {
      videoElement.value.srcObject = mediaStream
      await videoElement.value.play()
      cameraReady.value = true
    }
  } catch (err) {
    console.error('Camera initialization error:', err)
    if (err instanceof Error) {
      if (err.name === 'NotAllowedError') {
        error.value = 'カメラアクセスが拒否されました。ブラウザの設定でカメラアクセスを許可してください。'
      } else if (err.name === 'NotFoundError') {
        error.value = 'カメラが見つかりません。デバイスにカメラが接続されているか確認してください。'
      } else {
        error.value = 'カメラの初期化に失敗しました: ' + err.message
      }
    } else {
      error.value = 'カメラの初期化に失敗しました'
    }
  }
}

const captureImage = async () => {
  if (!videoElement.value || !canvasElement.value || capturing.value) return

  capturing.value = true

  try {
    const video = videoElement.value
    const canvas = canvasElement.value
    const context = canvas.getContext('2d')

    if (!context) {
      throw new Error('Canvas context not available')
    }

    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    context.drawImage(video, 0, 0)

    canvas.toBlob(async (blob) => {
      if (!blob) {
        throw new Error('Failed to capture image')
      }

      const imageUrl = URL.createObjectURL(blob)
      
      try {
        classifying.value = true
        const result = await classifyImage(blob)
        
        latestResult.value = {
          imageUrl,
          ...result,
          timestamp: new Date()
        }
      } catch (classificationError) {
        console.error('Classification error:', classificationError)
        window.dispatchEvent(new CustomEvent('app:toast', {
          detail: {
            type: 'error',
            title: '分類エラー',
            message: '画像の分類に失敗しました'
          }
        }))
      } finally {
        classifying.value = false
      }
    }, 'image/jpeg', 0.8)
  } catch (err) {
    console.error('Capture error:', err)
    window.dispatchEvent(new CustomEvent('app:toast', {
      detail: {
        type: 'error',
        title: '撮影エラー',
        message: '画像の撮影に失敗しました'
      }
    }))
  } finally {
    capturing.value = false
  }
}

const classifyImage = async (imageBlob: Blob) => {
  const formData = new FormData()
  formData.append('file', imageBlob, 'webcam-capture.jpg')

  const response = await fetch('/api/v1/classify', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${authStore.token}`,
    },
    body: formData
  })

  if (!response.ok) {
    throw new Error('Classification failed')
  }

  return await response.json()
}

const toggleAutoCapture = () => {
  if (autoCapture.value) {
    stopAutoCapture()
  } else {
    startAutoCapture()
  }
}

const startAutoCapture = () => {
  autoCapture.value = true
  countdown.value = autoCaptureInterval.value
  
  const startNextCapture = () => {
    autoCaptureTimer = window.setTimeout(async () => {
      if (autoCapture.value && !capturing.value && !classifying.value) {
        await captureImage()
        countdown.value = autoCaptureInterval.value
        startNextCapture()
      }
    }, autoCaptureInterval.value)
  }

  const updateCountdown = () => {
    countdownTimer = window.setTimeout(() => {
      if (autoCapture.value && countdown.value > 0) {
        countdown.value -= 100
        updateCountdown()
      }
    }, 100)
  }

  startNextCapture()
  updateCountdown()
}

const stopAutoCapture = () => {
  autoCapture.value = false
  if (autoCaptureTimer) {
    clearTimeout(autoCaptureTimer)
    autoCaptureTimer = null
  }
  if (countdownTimer) {
    clearTimeout(countdownTimer)
    countdownTimer = null
  }
  countdown.value = 0
}

const restartAutoCapture = () => {
  if (autoCapture.value) {
    stopAutoCapture()
    startAutoCapture()
  }
}

const stopCamera = () => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
    mediaStream = null
  }
  cameraReady.value = false
  stopAutoCapture()
}

const formatDate = (date: Date): string => {
  return date.toLocaleTimeString('ja-JP', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(() => {
  initializeCamera()
})

onUnmounted(() => {
  stopCamera()
  
  if (latestResult.value?.imageUrl) {
    URL.revokeObjectURL(latestResult.value.imageUrl)
  }
})
</script>

<style scoped>
.spinner {
  @apply w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

.spinner-small {
  @apply w-4 h-4 border-2 border-current border-t-transparent rounded-full;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.aspect-w-4 {
  position: relative;
  padding-bottom: calc(3 / 4 * 100%);
}

.aspect-w-4 > * {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>