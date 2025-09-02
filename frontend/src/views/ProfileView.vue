<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="container-custom py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          {{ t('profile.title') }}
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          {{ t('profile.subtitle') }}
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Profile Information -->
        <div class="lg:col-span-2">
          <div class="glass p-6 rounded-xl">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">
                {{ t('profile.personalInfo.title') }}
              </h2>
              <button
                v-if="!isEditing"
                @click="startEditing"
                class="px-4 py-2 text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 bg-primary-50 hover:bg-primary-100 dark:bg-primary-900/20 dark:hover:bg-primary-900/30 rounded-lg transition-colors"
              >
                {{ t('profile.actions.edit') }}
              </button>
            </div>

            <form v-if="isEditing" @submit.prevent="saveProfile" class="space-y-6">
              <!-- Email -->
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {{ t('profile.personalInfo.email') }}
                </label>
                <input
                  id="email"
                  v-model="profileForm.email"
                  type="email"
                  required
                  :disabled="isLoading"
                  class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  :class="{ 'border-red-500 focus:ring-red-500': errors.email }"
                />
                <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
              </div>

              <!-- Full Name -->
              <div>
                <label for="full_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {{ t('profile.personalInfo.fullNameOptional') }}
                </label>
                <input
                  id="full_name"
                  v-model="profileForm.full_name"
                  type="text"
                  :disabled="isLoading"
                  class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  :class="{ 'border-red-500 focus:ring-red-500': errors.full_name }"
:placeholder="t('profile.personalInfo.fullNamePlaceholder')"
                />
                <p v-if="errors.full_name" class="text-red-500 text-sm mt-1">{{ errors.full_name }}</p>
              </div>

              <!-- Action Buttons -->
              <div class="flex space-x-4">
                <button
                  type="submit"
                  :disabled="isLoading || !isFormValid"
                  class="flex-1 bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
                >
                  <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{{ isLoading ? t('profile.actions.saving') : t('profile.actions.save') }}</span>
                </button>
                <button
                  type="button"
                  @click="cancelEditing"
                  :disabled="isLoading"
                  class="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-medium py-3 px-6 rounded-lg transition-colors"
                >
                  {{ t('profile.actions.cancel') }}
                </button>
              </div>

              <!-- Error Message -->
              <div v-if="error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p class="text-red-800 dark:text-red-200 text-sm">{{ error }}</p>
              </div>
            </form>

            <!-- Display Mode -->
            <div v-else class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {{ t('profile.personalInfo.username') }}
                  </label>
                  <p class="text-gray-900 dark:text-white font-medium">{{ authStore.user?.username || t('profile.personalInfo.notSet') }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {{ t('profile.personalInfo.email') }}
                  </label>
                  <p class="text-gray-900 dark:text-white font-medium">{{ authStore.user?.email || t('profile.personalInfo.notSet') }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {{ t('profile.personalInfo.fullName') }}
                  </label>
                  <p class="text-gray-900 dark:text-white font-medium">{{ authStore.user?.full_name || t('profile.personalInfo.notSet') }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {{ t('profile.personalInfo.accountType') }}
                  </label>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                        :class="authStore.user?.is_admin ? 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400' : 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'">
                    {{ authStore.user?.is_admin ? t('profile.personalInfo.admin') : t('profile.personalInfo.regularUser') }}
                  </span>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {{ t('profile.personalInfo.registeredDate') }}
                  </label>
                  <p class="text-gray-900 dark:text-white font-medium">{{ formatDate(authStore.user?.created_at) }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {{ t('profile.personalInfo.lastLogin') }}
                  </label>
                  <p class="text-gray-900 dark:text-white font-medium">{{ formatDate(authStore.user?.last_login) }}</p>
                </div>
              </div>
            </div>

            <!-- Success Message -->
            <div v-if="successMessage" class="mt-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
              <p class="text-green-800 dark:text-green-200 text-sm">{{ successMessage }}</p>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Password Change Card -->
          <div class="glass p-6 rounded-xl">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">
              {{ t('profile.security.title') }}
            </h3>
            
            <form v-if="showPasswordForm" @submit.prevent="changePassword" class="space-y-4">
              <div>
                <label for="current_password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ t('profile.security.currentPassword') }}
                </label>
                <input
                  id="current_password"
                  v-model="passwordForm.current_password"
                  type="password"
                  required
                  :disabled="isPasswordLoading"
                  class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                />
              </div>
              
              <div>
                <label for="new_password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ t('profile.security.newPassword') }}
                </label>
                <input
                  id="new_password"
                  v-model="passwordForm.new_password"
                  type="password"
                  required
                  :disabled="isPasswordLoading"
                  class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                />
              </div>
              
              <div class="flex space-x-2">
                <button
                  type="submit"
                  :disabled="isPasswordLoading"
                  class="flex-1 bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm"
                >
                  {{ isPasswordLoading ? t('profile.actions.changing') : t('profile.actions.change') }}
                </button>
                <button
                  type="button"
                  @click="showPasswordForm = false"
                  :disabled="isPasswordLoading"
                  class="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-medium py-2 px-4 rounded-lg transition-colors text-sm"
                >
                  {{ t('profile.actions.cancel') }}
                </button>
              </div>
            </form>
            
            <button
              v-else
              @click="showPasswordForm = true"
              class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-white font-medium py-3 px-4 rounded-lg transition-colors"
            >
              {{ t('profile.security.changePassword') }}
            </button>
          </div>

          <!-- Active Sessions Card -->
          <div class="glass p-6 rounded-xl">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">
              {{ t('profile.security.sessions') }}
            </h3>
            
            <div v-if="sessions.length === 0" class="text-center py-4">
              <p class="text-gray-500 dark:text-gray-400 text-sm">{{ t('profile.security.sessionsLoading') }}</p>
            </div>
            
            <div v-else class="space-y-3">
              <div
                v-for="session in sessions"
                :key="session.id"
                class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <p class="font-medium text-gray-900 dark:text-white text-sm">
                      {{ session.user_agent || t('profile.security.unknownDevice') }}
                    </p>
                    <p class="text-xs text-gray-600 dark:text-gray-400">
                      {{ formatDate(session.created_at) }}
                    </p>
                    <p v-if="session.ip_address" class="text-xs text-gray-500 dark:text-gray-400">
                      IP: {{ session.ip_address }}
                    </p>
                  </div>
                  <button
                    @click="revokeSession(session.id)"
                    class="text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 text-xs"
                  >
                    {{ t('profile.security.terminateSession') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import type { UserSession } from '@/types/api'

// Stores and i18n
const { t, locale } = useI18n()
const authStore = useAuthStore()

// State
const isEditing = ref(false)
const isLoading = ref(false)
const isPasswordLoading = ref(false)
const showPasswordForm = ref(false)
const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)
const sessions = ref<UserSession[]>([])

const profileForm = ref({
  email: '',
  full_name: ''
})

const passwordForm = ref({
  current_password: '',
  new_password: ''
})

const errors = ref<Partial<Record<string, string>>>({})

// Computed
const isFormValid = computed(() => {
  return profileForm.value.email.trim().length > 0 && 
         Object.keys(errors.value).length === 0
})

// Methods
const formatDate = (dateString?: string): string => {
  if (!dateString) return t('profile.personalInfo.notSet')
  
  const date = new Date(dateString)
  return date.toLocaleDateString(locale.value === 'ja' ? 'ja-JP' : 'en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const startEditing = () => {
  if (authStore.user) {
    profileForm.value.email = authStore.user.email
    profileForm.value.full_name = authStore.user.full_name || ''
  }
  isEditing.value = true
  error.value = null
  successMessage.value = null
}

const cancelEditing = () => {
  isEditing.value = false
  errors.value = {}
  error.value = null
}

const validateEmail = (value: string) => {
  if (!value.trim()) {
    errors.value.email = t('profile.validation.emailRequired')
    return false
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(value)) {
    errors.value.email = t('profile.validation.emailInvalid')
    return false
  }
  delete errors.value.email
  return true
}

const validateFullName = (value: string) => {
  if (value && value.length > 100) {
    errors.value.full_name = t('profile.validation.fullNameMaxLength')
    return false
  }
  delete errors.value.full_name
  return true
}

// Watch for form changes
watch(() => profileForm.value.email, validateEmail)
watch(() => profileForm.value.full_name, validateFullName)

const saveProfile = async () => {
  // Clear previous errors
  error.value = null
  errors.value = {}
  
  // Validate form
  const isEmailValid = validateEmail(profileForm.value.email)
  const isFullNameValid = validateFullName(profileForm.value.full_name || '')
  
  if (!isEmailValid || !isFullNameValid) {
    return
  }

  isLoading.value = true
  
  try {
    await authStore.updateProfile({
      email: profileForm.value.email,
      full_name: profileForm.value.full_name || undefined
    })
    
    isEditing.value = false
    successMessage.value = t('profile.messages.profileUpdated')
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = null
    }, 5000)
  } catch (error: any) {
    error.value = error.message || t('profile.messages.profileUpdateFailed')
  } finally {
    isLoading.value = false
  }
}

const changePassword = async () => {
  isPasswordLoading.value = true
  
  try {
    await authStore.changePassword(
      passwordForm.value.current_password,
      passwordForm.value.new_password
    )
    
    passwordForm.value = { current_password: '', new_password: '' }
    showPasswordForm.value = false
    successMessage.value = t('profile.messages.passwordChanged')
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = null
    }, 5000)
  } catch (error: any) {
    error.value = error.message || t('profile.messages.passwordChangeFailed')
  } finally {
    isPasswordLoading.value = false
  }
}

const loadSessions = async () => {
  try {
    sessions.value = await authStore.getUserSessions()
  } catch (error) {
    console.error('Failed to load sessions:', error)
  }
}

const revokeSession = async (sessionId: number) => {
  try {
    await authStore.revokeSession(sessionId)
    // Reload sessions
    await loadSessions()
    successMessage.value = t('profile.messages.sessionTerminated')
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (error: any) {
    error.value = error.message || t('profile.messages.sessionTerminateFailed')
  }
}

// Lifecycle
onMounted(() => {
  loadSessions()
})
</script>

<style scoped>
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

.container-custom {
  max-width: 1200px;
  margin: 0 auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container-custom {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container-custom {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}
</style>