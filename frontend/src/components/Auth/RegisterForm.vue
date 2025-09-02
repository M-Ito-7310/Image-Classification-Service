<template>
  <div class="w-full mx-auto">
    <div class="glass p-8 rounded-xl">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold gradient-text">{{ t('auth.register.title') }}</h2>
        <p class="text-gray-600 dark:text-gray-400 mt-2">{{ t('auth.register.subtitle') }}</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Username Input -->
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('auth.register.username') }} <span class="text-red-500">*</span>
          </label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            autocomplete="username"
            required
            :disabled="isLoading"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            :class="{ 'border-red-500 focus:ring-red-500': errorKeys.username }"
            :placeholder="t('auth.register.usernamePlaceholder')"
          />
          <p v-if="errors.username" class="text-red-500 text-sm mt-1">{{ errors.username }}</p>
        </div>

        <!-- Email Input -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('auth.register.email') }} <span class="text-red-500">*</span>
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            autocomplete="email"
            required
            :disabled="isLoading"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            :class="{ 'border-red-500 focus:ring-red-500': errorKeys.email }"
            :placeholder="t('auth.register.emailPlaceholder')"
          />
          <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
        </div>

        <!-- Full Name Input -->
        <div>
          <label for="full_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('auth.register.fullName') }}
          </label>
          <input
            id="full_name"
            v-model="form.full_name"
            type="text"
            autocomplete="name"
            :disabled="isLoading"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            :class="{ 'border-red-500 focus:ring-red-500': errorKeys.full_name }"
            :placeholder="t('auth.register.fullNamePlaceholder')"
          />
          <p v-if="errors.full_name" class="text-red-500 text-sm mt-1">{{ errors.full_name }}</p>
        </div>

        <!-- Password Input -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('auth.register.password') }} <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              required
              :disabled="isLoading"
              class="w-full px-4 py-3 pr-12 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              :class="{ 'border-red-500 focus:ring-red-500': errorKeys.password }"
              :placeholder="t('auth.register.passwordPlaceholder')"
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
          
          <!-- Password strength indicator -->
          <div v-if="form.password" class="mt-2">
            <div class="flex items-center space-x-2">
              <div class="flex-1 h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                <div 
                  class="h-full transition-all duration-300"
                  :class="passwordStrengthColor"
                  :style="{ width: `${passwordStrengthPercent}%` }"
                ></div>
              </div>
              <span class="text-xs font-medium" :class="passwordStrengthTextColor">
                {{ passwordStrengthText }}
              </span>
            </div>
          </div>
        </div>

        <!-- Confirm Password Input -->
        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            {{ t('auth.register.confirmPassword') }} <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              autocomplete="new-password"
              required
              :disabled="isLoading"
              class="w-full px-4 py-3 pr-12 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              :class="{ 'border-red-500 focus:ring-red-500': errorKeys.confirmPassword }"
              :placeholder="t('auth.register.confirmPasswordPlaceholder')"
            />
            <button
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              :disabled="isLoading"
            >
              <svg v-if="showConfirmPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
              </svg>
            </button>
          </div>
          <p v-if="errors.confirmPassword" class="text-red-500 text-sm mt-1">{{ errors.confirmPassword }}</p>
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
          <span>{{ isLoading ? t('auth.register.submitting') : t('auth.register.submit') }}</span>
        </button>

        <!-- Login Link -->
        <div class="text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ t('auth.register.haveAccount') }}
            <button
              type="button"
              @click="$emit('switchToLogin')"
              class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium ml-1"
              :disabled="isLoading"
            >
              {{ t('auth.register.signIn') }}
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
import type { UserRegister } from '@/types/api'

// Props and Emits
interface Emits {
  (e: 'switchToLogin'): void
  (e: 'registerSuccess'): void
}

const emit = defineEmits<Emits>()

// Auth store and i18n
const { t, locale } = useI18n()
const authStore = useAuthStore()

// Form state
const form = ref<UserRegister>({
  username: '',
  email: '',
  password: '',
  full_name: ''
})

const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const errorKeys = ref<Partial<Record<keyof UserRegister | 'confirmPassword', string>>>({})

// Computed error messages that are reactive to language changes
const errors = computed(() => {
  // Force reactivity by accessing locale.value
  locale.value
  const result: Partial<Record<keyof UserRegister | 'confirmPassword', string>> = {}
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
  return form.value.username.trim().length >= 3 && 
         form.value.email.trim().length > 0 &&
         form.value.password.length >= 8 &&
         confirmPassword.value === form.value.password &&
         Object.keys(errorKeys.value).length === 0
})

// Password strength calculation
const passwordStrength = computed(() => {
  const password = form.value.password
  let score = 0
  
  if (password.length >= 8) score += 1
  if (password.length >= 12) score += 1
  if (/[a-z]/.test(password)) score += 1
  if (/[A-Z]/.test(password)) score += 1
  if (/[0-9]/.test(password)) score += 1
  if (/[^A-Za-z0-9]/.test(password)) score += 1
  
  return score
})

const passwordStrengthPercent = computed(() => Math.min((passwordStrength.value / 6) * 100, 100))
const passwordStrengthText = computed(() => {
  const score = passwordStrength.value
  if (score <= 2) return t('auth.register.passwordStrength.weak')
  if (score <= 4) return t('auth.register.passwordStrength.medium')
  return t('auth.register.passwordStrength.strong')
})

const passwordStrengthColor = computed(() => {
  const score = passwordStrength.value
  if (score <= 2) return 'bg-red-500'
  if (score <= 4) return 'bg-yellow-500'
  return 'bg-green-500'
})

const passwordStrengthTextColor = computed(() => {
  const score = passwordStrength.value
  if (score <= 2) return 'text-red-500'
  if (score <= 4) return 'text-yellow-500'
  return 'text-green-500'
})

// Validation
const validateUsername = (value: string) => {
  if (!value.trim()) {
    errors.value.username = t('auth.register.validation.usernameRequired')
    return false
  }
  if (value.length < 3) {
    errors.value.username = t('auth.register.validation.usernameMinLength')
    return false
  }
  if (value.length > 50) {
    errors.value.username = t('auth.register.validation.usernameMaxLength')
    return false
  }
  if (!/^[a-zA-Z0-9_-]+$/.test(value)) {
    errors.value.username = t('auth.register.validation.usernameInvalid')
    return false
  }
  delete errors.value.username
  return true
}

const validateEmail = (value: string) => {
  if (!value.trim()) {
    errors.value.email = t('auth.register.validation.emailRequired')
    return false
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(value)) {
    errors.value.email = t('auth.register.validation.emailInvalid')
    return false
  }
  delete errors.value.email
  return true
}

const validateFullName = (value: string) => {
  if (value && value.length > 100) {
    errors.value.full_name = t('auth.register.validation.fullNameMaxLength')
    return false
  }
  delete errors.value.full_name
  return true
}

const validatePassword = (value: string) => {
  if (!value) {
    errors.value.password = t('auth.register.validation.passwordRequired')
    return false
  }
  if (value.length < 8) {
    errors.value.password = t('auth.register.validation.passwordMinLength')
    return false
  }
  if (value.length > 100) {
    errors.value.password = t('auth.register.validation.passwordMaxLength')
    return false
  }
  delete errors.value.password
  return true
}

const validateConfirmPassword = (value: string) => {
  if (!value) {
    errors.value.confirmPassword = t('auth.register.validation.confirmPasswordRequired')
    return false
  }
  if (value !== form.value.password) {
    errors.value.confirmPassword = t('auth.register.validation.confirmPasswordMismatch')
    return false
  }
  delete errors.value.confirmPassword
  return true
}

// Watchers for real-time validation
watch(() => form.value.username, validateUsername)
watch(() => form.value.email, validateEmail)
watch(() => form.value.full_name, validateFullName)
watch(() => form.value.password, (newPassword) => {
  validatePassword(newPassword)
  // Re-validate confirm password when password changes
  if (confirmPassword.value) {
    validateConfirmPassword(confirmPassword.value)
  }
})
watch(() => confirmPassword.value, validateConfirmPassword)

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
  const isEmailValid = validateEmail(form.value.email)
  const isFullNameValid = validateFullName(form.value.full_name || '')
  const isPasswordValid = validatePassword(form.value.password)
  const isConfirmPasswordValid = validateConfirmPassword(confirmPassword.value)

  if (!isUsernameValid || !isEmailValid || !isFullNameValid || !isPasswordValid || !isConfirmPasswordValid) {
    return
  }

  try {
    await authStore.register(form.value)
    emit('registerSuccess')
  } catch (error: any) {
    // Error is already handled by the auth store
    console.error('Registration failed:', error)
  }
}

// Initialize form validation on mount
const validateForm = () => {
  validateUsername(form.value.username)
  validateEmail(form.value.email)
  validateFullName(form.value.full_name || '')
  validatePassword(form.value.password)
  validateConfirmPassword(confirmPassword.value)
}

// Clear form
const clearForm = () => {
  form.value = {
    username: '',
    email: '',
    password: '',
    full_name: ''
  }
  confirmPassword.value = ''
  errorKeys.value = {}
  showPassword.value = false
  showConfirmPassword.value = false
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