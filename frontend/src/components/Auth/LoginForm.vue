<template>
  <div class="w-full mx-auto">
    <div class="glass p-8 rounded-xl">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold gradient-text">{{ t('auth.login.title') }}</h2>
        <p class="text-gray-600 dark:text-gray-400 mt-2">{{ t('auth.login.subtitle') }}</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Username/Email Input -->
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('auth.login.username') }}
          </label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            autocomplete="username"
            required
            :disabled="isLoading"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            :class="{ 'border-red-500 focus:ring-red-500': errors.username }"
            :placeholder="t('auth.login.usernamePlaceholder')"
          />
          <p v-if="errors.username" class="text-red-500 text-sm mt-1">{{ errors.username }}</p>
        </div>

        <!-- Password Input -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('auth.login.password') }}
          </label>
          <div class="relative">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              required
              :disabled="isLoading"
              class="w-full px-4 py-3 pr-12 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              :class="{ 'border-red-500 focus:ring-red-500': errors.password }"
              :placeholder="t('auth.login.passwordPlaceholder')"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              :disabled="isLoading"
            >
              <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
              </svg>
            </button>
          </div>
          <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
        </div>

        <!-- Demo Accounts Card -->
        <div class="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
          <div class="flex items-center mb-3">
            <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="text-sm font-semibold text-blue-800 dark:text-blue-200">{{ t('auth.login.demo.title') }}</h3>
          </div>
          <p class="text-xs text-blue-700 dark:text-blue-300 mb-3">{{ t('auth.login.demo.description') }}</p>
          
          <div class="grid grid-cols-1 gap-2">
            <!-- Regular User Demo -->
            <div class="flex items-center justify-between p-2 bg-white dark:bg-blue-800/30 rounded border">
              <div class="flex-1">
                <div class="text-xs font-medium text-gray-900 dark:text-gray-100">{{ t('auth.login.demo.regularUser') }}</div>
                <div class="text-xs text-gray-600 dark:text-gray-400">demo / demo1234</div>
              </div>
              <button
                @click="quickLogin('demo', 'demo1234')"
                :disabled="isLoading"
                class="px-3 py-1 text-xs bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors disabled:opacity-50"
              >
                {{ t('auth.login.demo.quickLogin') }}
              </button>
            </div>
            
            <!-- Admin User Demo -->
            <div class="flex items-center justify-between p-2 bg-white dark:bg-blue-800/30 rounded border">
              <div class="flex-1">
                <div class="text-xs font-medium text-gray-900 dark:text-gray-100">{{ t('auth.login.demo.adminUser') }}</div>
                <div class="text-xs text-gray-600 dark:text-gray-400">admin / admin1234</div>
              </div>
              <button
                @click="quickLogin('admin', 'admin1234')"
                :disabled="isLoading"
                class="px-3 py-1 text-xs bg-purple-600 hover:bg-purple-700 text-white rounded transition-colors disabled:opacity-50"
              >
                {{ t('auth.login.demo.quickLogin') }}
              </button>
            </div>
          </div>
          
          <p class="text-xs text-blue-600 dark:text-blue-400 mt-2">{{ t('auth.login.demo.note') }}</p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p class="text-red-800 dark:text-red-200 text-sm">{{ error }}</p>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading || !isFormValid"
          class="w-full bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
        >
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ isLoading ? t('auth.login.submitting') : t('auth.login.submit') }}</span>
        </button>

        <!-- Register Link -->
        <div class="text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ t('auth.login.noAccount') }}
            <button
              type="button"
              @click="$emit('switchToRegister')"
              class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium ml-1"
              :disabled="isLoading"
            >
              {{ t('auth.login.signUp') }}
            </button>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import type { UserLogin } from '@/types/api'

// Props and Emits
interface Props {
  redirectTo?: string
}

interface Emits {
  (e: 'switchToRegister'): void
  (e: 'loginSuccess'): void
}

const props = withDefaults(defineProps<Props>(), {
  redirectTo: '/'
})

const emit = defineEmits<Emits>()

// Auth store and i18n
const { t, locale } = useI18n()
const authStore = useAuthStore()

// Form state
const form = ref<UserLogin>({
  username: '',
  password: ''
})

const showPassword = ref(false)
const errorKeys = ref<Partial<Record<keyof UserLogin, string>>>({})

// Computed error messages that are reactive to language changes
const errors = computed(() => {
  // Force reactivity by accessing locale.value
  locale.value
  const result: Partial<Record<keyof UserLogin, string>> = {}
  for (const [key, errorKey] of Object.entries(errorKeys.value)) {
    if (errorKey) {
      result[key as keyof typeof result] = t(errorKey)
    }
  }
  return result
})

// Computed
const isLoading = computed(() => authStore.isLoading)
const error = computed(() => authStore.error)

const isFormValid = computed(() => {
  return form.value.username.trim().length > 0 && 
         form.value.password.length > 0 && 
         Object.keys(errors.value).length === 0
})

// Validation
const validateUsername = (value: string) => {
  if (!value.trim()) {
    errorKeys.value.username = 'auth.login.validation.usernameRequired'
    return false
  }
  delete errorKeys.value.username
  return true
}

const validatePassword = (value: string) => {
  if (!value) {
    errorKeys.value.password = 'auth.login.validation.passwordRequired'
    return false
  }
  if (value.length < 8) {
    errorKeys.value.password = 'auth.login.validation.passwordMinLength'
    return false
  }
  delete errorKeys.value.password
  return true
}

// Watchers for real-time validation
watch(() => form.value.username, validateUsername)
watch(() => form.value.password, validatePassword)

// Clear errors when auth store error changes
watch(() => authStore.error, () => {
  if (!authStore.error) {
    authStore.clearError()
  }
})

// Methods
const handleSubmit = async () => {
  // Clear previous errors
  authStore.clearError()
  errorKeys.value = {}

  // Validate form
  const isUsernameValid = validateUsername(form.value.username)
  const isPasswordValid = validatePassword(form.value.password)

  if (!isUsernameValid || !isPasswordValid) {
    return
  }

  try {
    await authStore.login(form.value)
    emit('loginSuccess')
  } catch (error: any) {
    // Error is already handled by the auth store
    console.error('Login failed:', error)
  }
}

const quickLogin = async (username: string, password: string) => {
  // Clear previous errors
  authStore.clearError()
  errorKeys.value = {}
  
  // Set form values
  form.value.username = username
  form.value.password = password
  
  try {
    await authStore.login(form.value)
    emit('loginSuccess')
  } catch (error: any) {
    console.error('Quick login failed:', error)
  }
}

// Initialize form validation on mount
const validateForm = () => {
  validateUsername(form.value.username)
  validatePassword(form.value.password)
}

// Clear form
const clearForm = () => {
  form.value = {
    username: '',
    password: ''
  }
  errorKeys.value = {}
  showPassword.value = false
  authStore.clearError()
}

// Expose methods for parent component
defineExpose({
  clearForm,
  validateForm
})
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.glass {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.dark .glass {
  background: rgba(31, 41, 55, 0.95);
  border: 1px solid rgba(75, 85, 99, 0.3);
}
</style>