import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor libraries
          'vendor': ['vue', 'vue-router', 'pinia'],
          'ui': ['@headlessui/vue', '@heroicons/vue'],
          'i18n': ['vue-i18n'],
          'utils': ['axios', 'lodash-es'],
          // Component chunks
          'auth': [
            './src/components/Auth/AuthModal.vue',
            './src/components/Auth/LoginForm.vue', 
            './src/components/Auth/RegisterForm.vue',
            './src/stores/auth.ts'
          ],
          'models': [
            './src/components/Models/ModelUpload.vue',
            './src/components/Models/ModelList.vue',
            './src/views/ModelsView.vue'
          ],
          'batch': [
            './src/components/Batch/BatchClassification.vue'
          ],
          'camera': [
            './src/components/Camera/WebcamCapture.vue'
          ]
        }
      }
    },
    // Bundle size optimization
    chunkSizeWarningLimit: 500, // 500KB warning limit
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log in production
        drop_debugger: true
      }
    }
  },
  // Performance optimization
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', 'vue-i18n']
  }
})
