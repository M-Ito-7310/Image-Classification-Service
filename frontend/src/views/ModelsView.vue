<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-slate-900 dark:to-gray-900">
    <div class="container mx-auto px-4 py-8">
      <ModelList />
    </div>
  </div>
</template>

<script setup lang="ts">
import ModelList from '@/components/Models/ModelList.vue'
</script>