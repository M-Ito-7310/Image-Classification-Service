import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: {
        title: 'AI画像分類サービス',
        description: '最新のAI技術を使用した高精度画像分類システム'
      }
    },
    {
      path: '/classify',
      name: 'classify',
      component: () => import('../views/ClassificationView.vue'),
      meta: {
        title: '画像分類 - AI画像分類サービス',
        description: '画像をアップロードしてAIによる自動分類を実行'
      }
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/HistoryView.vue'),
      meta: {
        title: '分類履歴 - AI画像分類サービス',
        description: 'これまでの画像分類結果の履歴を確認',
        requiresAuth: true
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
      meta: {
        title: '設定 - AI画像分類サービス',
        description: 'アプリケーションの設定とカスタマイズ',
        requiresAuth: true
      }
    },
    // Authentication routes
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/AuthView.vue'),
      meta: {
        title: 'ログイン - AI画像分類サービス',
        description: 'アカウントにログインしてサービスをご利用ください',
        guestOnly: true,
        initialView: 'login'
      }
    },
    {
      path: '/register',
      name: 'register', 
      component: () => import('../views/AuthView.vue'),
      meta: {
        title: '新規登録 - AI画像分類サービス',
        description: '新しいアカウントを作成してサービスをご利用ください',
        guestOnly: true,
        initialView: 'register'
      }
    },
    // User dashboard and profile
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: {
        title: 'ダッシュボード - AI画像分類サービス',
        description: 'ユーザーダッシュボード',
        requiresAuth: true
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: {
        title: 'プロフィール - AI画像分類サービス',
        description: 'ユーザープロフィールの管理',
        requiresAuth: true
      }
    },
    // Custom model management routes
    {
      path: '/models',
      name: 'models',
      component: () => import('../views/ModelsView.vue'),
      meta: {
        title: 'カスタムモデル - AI画像分類サービス',
        description: 'カスタムモデルの管理とアップロード',
        requiresAuth: true
      }
    },
    {
      path: '/models/upload',
      name: 'models-upload',
      component: () => import('../views/ModelUploadView.vue'),
      meta: {
        title: 'モデルアップロード - AI画像分類サービス',
        description: 'カスタムモデルのアップロード',
        requiresAuth: true
      }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: {
        title: 'このサービスについて - AI画像分類サービス',
        description: 'AI画像分類サービスの詳細情報'
      }
    },
    // 404 page
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: {
        title: 'ページが見つかりません - AI画像分類サービス'
      }
    }
  ],
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth store if not already done
  if (!authStore.isInitialized) {
    await authStore.initialize()
  }

  // Update document title
  if (to.meta?.title) {
    document.title = to.meta.title as string
  }

  // Update meta description
  if (to.meta?.description) {
    const metaDescription = document.querySelector('meta[name="description"]')
    if (metaDescription) {
      metaDescription.setAttribute('content', to.meta.description as string)
    }
  }

  // Check if route requires authentication
  if (to.meta?.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Store the intended destination
      const redirectTo = to.fullPath
      
      // Redirect to login with return path
      next({
        name: 'login',
        query: { redirect: redirectTo }
      })
      return
    }
  }

  // Check if route is for guests only (login/register pages)
  if (to.meta?.guestOnly) {
    if (authStore.isAuthenticated) {
      // If user is already authenticated, redirect to dashboard or home
      const redirectTo = from.query?.redirect as string || '/dashboard'
      next(redirectTo)
      return
    }
  }

  // Check admin routes
  if (to.meta?.requiresAdmin) {
    if (!authStore.isAuthenticated) {
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
      return
    }
    
    if (!authStore.isAdmin) {
      // Redirect non-admin users to home or show 403
      next({ name: 'home' })
      return
    }
  }

  next()
})

// Handle authentication state changes
router.afterEach((to, from) => {
  // Clear any previous auth errors when navigating
  const authStore = useAuthStore()
  if (authStore.error) {
    authStore.clearError()
  }
})

export default router
