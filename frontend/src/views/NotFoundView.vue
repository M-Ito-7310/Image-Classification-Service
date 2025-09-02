<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center py-12">
    <div class="max-w-md w-full text-center px-4">
      <!-- 404 Illustration -->
      <div class="mb-8">
        <div class="mx-auto w-32 h-32 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mb-6">
          <svg class="w-16 h-16 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m-3-5v1m-8 8h16M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        
        <h1 class="text-6xl font-bold text-gray-300 dark:text-gray-600 mb-4">
          404
        </h1>
      </div>

      <!-- Error Message -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          ページが見つかりません
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          お探しのページは存在しないか、移動された可能性があります。
          URLをご確認いただくか、下記のリンクからホームページにお戻りください。
        </p>
      </div>

      <!-- Navigation Options -->
      <div class="space-y-4">
        <router-link
          to="/"
          class="block w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-6 rounded-lg transition-colors"
        >
          ホームページに戻る
        </router-link>
        
        <div class="flex space-x-4">
          <router-link
            to="/classify"
            class="flex-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium py-2 px-4 rounded-lg transition-colors text-sm"
          >
            画像分類
          </router-link>
          
          <router-link
            to="/history"
            class="flex-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium py-2 px-4 rounded-lg transition-colors text-sm"
          >
            履歴
          </router-link>
          
          <router-link
            to="/about"
            class="flex-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium py-2 px-4 rounded-lg transition-colors text-sm"
          >
            詳細
          </router-link>
        </div>
      </div>

      <!-- Additional Help -->
      <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-700">
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
          問題が解決しない場合は、お気軽にお問い合わせください
        </p>
        <a
          href="mailto:support@example.com"
          class="inline-flex items-center text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.476a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          サポートに連絡
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404 Not Found page - static content
</script>