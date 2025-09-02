<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 dark:from-gray-900 dark:via-gray-800 dark:to-gray-700">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-grid-pattern opacity-5"></div>
    
    <!-- Main Content -->
    <div class="relative min-h-screen flex items-center justify-center p-4">
      <div class="w-[50%] max-w-2xl">
        <!-- Header -->
        <div class="text-center mb-8">
          <RouterLink to="/" class="inline-flex items-center space-x-3 mb-6">
            <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h1 class="text-2xl font-bold gradient-text">{{ t('auth.appName') }}</h1>
          </RouterLink>
        </div>

        <!-- Form Container -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 transform translate-y-8"
          enter-to-class="opacity-100 transform translate-y-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 transform translate-y-0"
          leave-to-class="opacity-0 transform translate-y-8"
          mode="out-in"
        >
          <!-- Login Form -->
          <LoginForm
            v-if="currentView === 'login'"
            :redirect-to="redirectTo"
            @switch-to-register="switchToRegister"
            @login-success="handleAuthSuccess"
          />

          <!-- Register Form -->
          <RegisterForm
            v-else-if="currentView === 'register'"
            @switch-to-login="switchToLogin"
            @register-success="handleAuthSuccess"
          />
        </Transition>

        <!-- Footer Links -->
        <div class="text-center mt-8 space-y-4">
          <div class="flex justify-center space-x-6 text-sm">
            <RouterLink 
              to="/about" 
              class="text-gray-600 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 transition-colors"
            >
              {{ t('auth.footer.aboutService') }}
            </RouterLink>
            <RouterLink 
              to="/" 
              class="text-gray-600 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400 transition-colors"
            >
              {{ t('auth.footer.backToHome') }}
            </RouterLink>
          </div>
          
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ t('auth.footer.copyright') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { LoginForm, RegisterForm } from '@/components/Auth'

// Router, stores and i18n
const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()

// State
const currentView = ref<'login' | 'register'>('login')

// Computed
const redirectTo = computed(() => {
  const redirect = route.query.redirect as string
  return redirect || '/dashboard'
})

// Methods
const switchToLogin = () => {
  currentView.value = 'login'
  // Update URL without triggering route guard
  if (route.name !== 'login') {
    router.replace({ 
      name: 'login', 
      query: { redirect: route.query.redirect } 
    })
  }
}

const switchToRegister = () => {
  currentView.value = 'register'
  // Update URL without triggering route guard
  if (route.name !== 'register') {
    router.replace({ 
      name: 'register', 
      query: { redirect: route.query.redirect } 
    })
  }
}

const handleAuthSuccess = async () => {
  // Start token refresh timer
  authStore.startTokenRefreshTimer()
  
  // Redirect to intended destination
  await router.push(redirectTo.value)
}

// Watch route changes
watch(
  () => route.name,
  (routeName) => {
    if (routeName === 'login') {
      currentView.value = 'login'
    } else if (routeName === 'register') {
      currentView.value = 'register'
    }
  },
  { immediate: true }
)

// Watch for initial view from route meta
watch(
  () => route.meta?.initialView,
  (initialView) => {
    if (initialView === 'login' || initialView === 'register') {
      currentView.value = initialView
    }
  },
  { immediate: true }
)

// Initialize
onMounted(() => {
  // Set initial view based on route
  if (route.name === 'register') {
    currentView.value = 'register'
  } else {
    currentView.value = 'login'
  }
  
  // If user is already authenticated, redirect
  if (authStore.isAuthenticated) {
    router.push(redirectTo.value)
  }
})
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.bg-grid-pattern {
  background-image: radial-gradient(circle, rgba(0, 0, 0, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}

.dark .bg-grid-pattern {
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
}
</style>