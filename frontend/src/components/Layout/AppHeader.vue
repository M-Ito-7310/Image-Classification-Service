<template>
  <header class="sticky top-0 z-50 glass border-b border-gray-200 dark:border-gray-700">
    <div class="container-custom">
      <div class="flex items-center justify-between h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center space-x-4">
          <RouterLink to="/" class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold gradient-text">{{ t('common.appName') }}</h1>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ locale === 'ja' ? '画像分類・認識サービス' : 'Image Classification & Recognition' }}</p>
            </div>
          </RouterLink>
        </div>

        <!-- Navigation -->
        <nav class="hidden md:flex items-center space-x-8">
          <RouterLink
            to="/"
            class="text-gray-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400 transition-colors font-medium"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path === '/' }"
          >
            {{ t('nav.home') }}
          </RouterLink>
          <RouterLink
            to="/classify"
            class="text-gray-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400 transition-colors font-medium"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path === '/classify' }"
          >
            {{ t('nav.classify') }}
          </RouterLink>
          <RouterLink
            to="/history"
            class="text-gray-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400 transition-colors font-medium"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path === '/history' }"
          >
            {{ t('nav.history') }}
          </RouterLink>
          <RouterLink
            v-if="authStore.isAuthenticated"
            to="/models"
            class="text-gray-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400 transition-colors font-medium"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path.startsWith('/models') }"
          >
            カスタムモデル
          </RouterLink>
          <RouterLink
            v-if="authStore.isAuthenticated"
            to="/dashboard"
            class="text-gray-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400 transition-colors font-medium"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path === '/dashboard' }"
          >
            {{ t('nav.dashboard') }}
          </RouterLink>
          <RouterLink
            to="/about"
            class="text-gray-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400 transition-colors font-medium"
            :class="{ 'text-primary-600 dark:text-primary-400': $route.path === '/about' }"
          >
            {{ t('nav.about') }}
          </RouterLink>
        </nav>

        <!-- Right side actions -->
        <div class="flex items-center space-x-4">
          <!-- User Menu (when authenticated) -->
          <div v-if="authStore.isAuthenticated" class="relative" ref="userMenuRef">
            <button
              @click="userMenuOpen = !userMenuOpen"
              class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              aria-label="User menu"
            >
              <!-- User Avatar -->
              <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                {{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
              </div>
              <span class="hidden md:block text-sm font-medium text-gray-700 dark:text-gray-300">
                {{ authStore.getDisplayName() }}
              </span>
              <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- User Dropdown Menu -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 scale-95"
              enter-to-class="opacity-100 scale-100"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100 scale-100"
              leave-to-class="opacity-0 scale-95"
            >
              <div v-if="userMenuOpen" class="absolute right-0 top-full mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 py-1 z-50">
                <RouterLink
                  to="/profile"
                  @click="userMenuOpen = false"
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <div class="flex items-center space-x-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span>{{ t('nav.profile') }}</span>
                  </div>
                </RouterLink>
                <RouterLink
                  to="/settings"
                  @click="userMenuOpen = false"
                  class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <div class="flex items-center space-x-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span>{{ t('nav.settings') }}</span>
                  </div>
                </RouterLink>
                <div class="border-t border-gray-200 dark:border-gray-600 my-1"></div>
                <button
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20"
                >
                  <div class="flex items-center space-x-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    <span>{{ t('nav.logout') }}</span>
                  </div>
                </button>
              </div>
            </Transition>
          </div>

          <!-- Login/Register buttons (when not authenticated) -->
          <div v-else class="hidden md:flex items-center space-x-2">
            <RouterLink
              to="/login"
              class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-primary-600 dark:text-gray-300 dark:hover:text-primary-400 transition-colors"
            >
              {{ t('nav.login') }}
            </RouterLink>
            <RouterLink
              to="/register"
              class="px-4 py-2 text-sm font-medium bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
            >
              {{ t('nav.register') }}
            </RouterLink>
          </div>

          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Toggle theme"
          >
            <svg v-if="isDark" class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

          <!-- Language Toggle -->
          <button
            @click="toggleLanguage"
            class="px-3 py-1 text-sm font-medium rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-600 dark:text-gray-400"
          >
            {{ locale === 'ja' ? '日本語' : 'English' }}
          </button>

          <!-- Mobile Menu Button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Toggle menu"
          >
            <svg class="w-6 h-6 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 -translate-y-1"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-1"
      >
        <nav v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex flex-col space-y-2">
            <RouterLink
              to="/"
              @click="mobileMenuOpen = false"
              class="px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium"
              :class="{ 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400': $route.path === '/' }"
            >
              {{ t('nav.home') }}
            </RouterLink>
            <RouterLink
              to="/classify"
              @click="mobileMenuOpen = false"
              class="px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium"
              :class="{ 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400': $route.path === '/classify' }"
            >
              {{ t('nav.classify') }}
            </RouterLink>
            <RouterLink
              to="/history"
              @click="mobileMenuOpen = false"
              class="px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium"
              :class="{ 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400': $route.path === '/history' }"
            >
              {{ t('nav.history') }}
            </RouterLink>
            <RouterLink
              v-if="authStore.isAuthenticated"
              to="/models"
              @click="mobileMenuOpen = false"
              class="px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium"
              :class="{ 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400': $route.path.startsWith('/models') }"
            >
              カスタムモデル
            </RouterLink>
            <RouterLink
              v-if="authStore.isAuthenticated"
              to="/dashboard"
              @click="mobileMenuOpen = false"
              class="px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium"
              :class="{ 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400': $route.path === '/dashboard' }"
            >
              {{ t('nav.dashboard') }}
            </RouterLink>
            <RouterLink
              to="/about"
              @click="mobileMenuOpen = false"
              class="px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium"
              :class="{ 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400': $route.path === '/about' }"
            >
              {{ t('nav.about') }}
            </RouterLink>
            
            <!-- Mobile Auth Section -->
            <div class="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
              <!-- Authenticated user menu for mobile -->
              <div v-if="authStore.isAuthenticated" class="space-y-2">
                <div class="px-4 py-2 text-sm text-gray-500 dark:text-gray-400">
                  {{ authStore.getDisplayName() }}
                </div>
                <RouterLink
                  to="/profile"
                  @click="mobileMenuOpen = false"
                  class="block px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium"
                >
                  {{ t('nav.profile') }}
                </RouterLink>
                <button
                  @click="handleLogout(); mobileMenuOpen = false"
                  class="block w-full text-left px-4 py-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400 font-medium"
                >
                  {{ t('nav.logout') }}
                </button>
              </div>
              
              <!-- Login/Register buttons for mobile -->
              <div v-else class="space-y-2">
                <RouterLink
                  to="/login"
                  @click="mobileMenuOpen = false"
                  class="block px-4 py-2 text-center rounded-lg border border-primary-500 text-primary-600 hover:bg-primary-50 dark:text-primary-400 dark:hover:bg-primary-900/20 font-medium"
                >
                  {{ t('nav.login') }}
                </RouterLink>
                <RouterLink
                  to="/register"
                  @click="mobileMenuOpen = false"
                  class="block px-4 py-2 text-center rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-medium"
                >
                  {{ t('nav.register') }}
                </RouterLink>
              </div>
            </div>
          </div>
        </nav>
      </Transition>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import { setLanguage } from '@/i18n'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { t, locale } = useI18n()

const mobileMenuOpen = ref(false)
const userMenuOpen = ref(false)
const isDark = ref(false)
const currentLanguage = computed(() => locale.value)
const userMenuRef = ref<HTMLElement>()

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

const toggleLanguage = () => {
  const newLang = locale.value === 'ja' ? 'en' : 'ja'
  setLanguage(newLang as 'ja' | 'en')
}

const handleLogout = async () => {
  userMenuOpen.value = false
  
  try {
    await authStore.logout()
    await router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

// Click outside handler for user menu
const handleClickOutside = (event: MouseEvent) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target as Node)) {
    userMenuOpen.value = false
  }
}

onMounted(() => {
  // Check for saved theme preference
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }

  // Check for saved language preference
  const savedLanguage = localStorage.getItem('language')
  if (savedLanguage && ['ja', 'en'].includes(savedLanguage)) {
    setLanguage(savedLanguage as 'ja' | 'en')
  }

  // Add click outside listener
  document.addEventListener('click', handleClickOutside)
  
  // Initialize auth store
  authStore.initialize()
})

onUnmounted(() => {
  // Remove click outside listener
  document.removeEventListener('click', handleClickOutside)
})
</script>