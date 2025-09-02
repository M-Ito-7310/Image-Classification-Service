<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="container-custom py-8">
      <!-- Header Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          {{ t('dashboard.title') }}
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          {{ t('dashboard.welcome', { name: authStore.getDisplayName() }) }}
        </p>
      </div>

      <!-- Quick Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="glass p-6 rounded-xl">
          <div class="flex items-center">
            <div class="p-3 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
              <svg class="w-6 h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ t('dashboard.stats.totalImages') }}</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalClassifications }}</p>
            </div>
          </div>
        </div>

        <div class="glass p-6 rounded-xl">
          <div class="flex items-center">
            <div class="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ t('dashboard.stats.monthlyImages') }}</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.monthlyClassifications }}</p>
            </div>
          </div>
        </div>

        <div class="glass p-6 rounded-xl">
          <div class="flex items-center">
            <div class="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ t('dashboard.stats.accuracy') }}</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.averageAccuracy }}%</p>
            </div>
          </div>
        </div>

        <div class="glass p-6 rounded-xl">
          <div class="flex items-center">
            <div class="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
              <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ t('dashboard.stats.processingTime') }}</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.averageProcessingTime }}ms</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Recent Activity -->
        <div class="lg:col-span-2">
          <div class="glass p-6 rounded-xl">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">
                {{ t('dashboard.recentActivity.title') }}
              </h2>
              <RouterLink
                to="/history"
                class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium"
              >
                {{ t('dashboard.recentActivity.viewAll') }} →
              </RouterLink>
            </div>

            <div v-if="recentActivity.length === 0" class="text-center py-8">
              <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p class="text-gray-500 dark:text-gray-400">{{ t('dashboard.recentActivity.empty') }}</p>
              <RouterLink
                to="/classify"
                class="inline-flex items-center mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                {{ t('dashboard.quickActions.classify') }}
              </RouterLink>
            </div>

            <div v-else class="space-y-4">
              <div
                v-for="item in recentActivity"
                :key="item.id"
                class="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <div class="w-12 h-12 bg-gradient-to-br from-gray-300 to-gray-400 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="font-medium text-gray-900 dark:text-white">{{ item.filename }}</h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    {{ item.predictions[0]?.class_name || 'Unknown' }} ({{ Math.round((item.predictions[0]?.confidence || 0) * 100) }}%)
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(item.created_at) }}</p>
                </div>
                <div class="text-right">
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ item.processing_time }}ms
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="space-y-6">
          <!-- Quick Actions Card -->
          <div class="glass p-6 rounded-xl">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              {{ t('dashboard.quickActions.title') }}
            </h2>
            <div class="space-y-3">
              <RouterLink
                to="/classify"
                class="block w-full bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl text-center"
              >
                {{ t('dashboard.quickActions.classify') }}
              </RouterLink>
              <RouterLink
                to="/history"
                class="block w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-white font-medium py-3 px-4 rounded-lg transition-colors text-center"
              >
                {{ t('dashboard.quickActions.viewHistory') }}
              </RouterLink>
              <RouterLink
                to="/settings"
                class="block w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-white font-medium py-3 px-4 rounded-lg transition-colors text-center"
              >
                {{ t('dashboard.quickActions.settings') }}
              </RouterLink>
            </div>
          </div>

          <!-- Account Info Card -->
          <div class="glass p-6 rounded-xl">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              {{ t('dashboard.accountInfo.title') }}
            </h2>
            <div class="space-y-3">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                  {{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
                </div>
                <div>
                  <p class="font-medium text-gray-900 dark:text-white">{{ authStore.user?.username }}</p>
                  <p class="text-sm text-gray-600 dark:text-gray-400">{{ authStore.user?.email }}</p>
                </div>
              </div>
              <div class="pt-3 border-t border-gray-200 dark:border-gray-700">
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  {{ t('dashboard.accountInfo.registeredDate') }}: {{ formatDate(authStore.user?.created_at) }}
                </p>
                <p v-if="authStore.user?.last_login" class="text-sm text-gray-600 dark:text-gray-400">
                  {{ t('dashboard.accountInfo.lastLogin') }}: {{ formatDate(authStore.user.last_login) }}
                </p>
              </div>
              <RouterLink
                to="/profile"
                class="block w-full text-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm"
              >
                {{ t('dashboard.quickActions.profile') }}
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useHistoryStore } from '@/stores/history'

// Stores and i18n
const { t, locale } = useI18n()
const authStore = useAuthStore()
const historyStore = useHistoryStore()

// State
const stats = ref({
  totalClassifications: 0,
  monthlyClassifications: 0,
  averageAccuracy: 0,
  averageProcessingTime: 0
})

const recentActivity = ref<any[]>([])

// Methods
const formatDate = (dateString?: string): string => {
  if (!dateString) return t('common.noData')
  
  const date = new Date(dateString)
  return date.toLocaleDateString(locale.value === 'ja' ? 'ja-JP' : 'en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadDashboardData = async () => {
  try {
    // Fetch statistics
    const statsData = await historyStore.fetchStats()
    if (statsData) {
      stats.value = {
        totalClassifications: statsData.total_classifications,
        monthlyClassifications: statsData.monthly_classifications,
        averageAccuracy: Math.round(statsData.average_accuracy),
        averageProcessingTime: Math.round(statsData.average_processing_time)
      }
    }

    // Fetch recent history
    await historyStore.fetchHistory(1, 5)
    recentActivity.value = historyStore.recentHistory
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    // If API fails, show mock data for development
    stats.value = {
      totalClassifications: 0,
      monthlyClassifications: 0,
      averageAccuracy: 0,
      averageProcessingTime: 0
    }
    recentActivity.value = []
  }
}

// Lifecycle
onMounted(() => {
  loadDashboardData()
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