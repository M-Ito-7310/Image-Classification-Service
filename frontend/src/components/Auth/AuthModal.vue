<template>
  <!-- Modal Backdrop -->
  <Teleport to="body">
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isVisible"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click.self="handleBackdropClick"
      >
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>

        <!-- Modal Container -->
        <div class="relative min-h-screen flex items-center justify-center p-4">
          <Transition
            enter-active-class="transition ease-out duration-300"
            enter-from-class="opacity-0 transform translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to-class="opacity-100 transform translate-y-0 sm:scale-100"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="opacity-100 transform translate-y-0 sm:scale-100"
            leave-to-class="opacity-0 transform translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div v-if="isVisible" class="relative w-full max-w-md mx-auto">
              <!-- Close Button -->
              <button
                @click="close"
                class="absolute -top-12 right-0 text-white hover:text-gray-300 transition-colors z-10"
                aria-label="Close modal"
              >
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <!-- Form Container -->
              <div class="relative">
                <!-- Login Form -->
                <Transition
                  enter-active-class="transition ease-out duration-300"
                  enter-from-class="opacity-0 transform translate-x-full"
                  enter-to-class="opacity-100 transform translate-x-0"
                  leave-active-class="transition ease-in duration-200"
                  leave-from-class="opacity-100 transform translate-x-0"
                  leave-to-class="opacity-0 transform -translate-x-full"
                >
                  <LoginForm
                    v-if="currentView === 'login'"
                    ref="loginFormRef"
                    :redirect-to="redirectTo"
                    @switch-to-register="switchToRegister"
                    @login-success="handleAuthSuccess"
                  />
                </Transition>

                <!-- Register Form -->
                <Transition
                  enter-active-class="transition ease-out duration-300"
                  enter-from-class="opacity-0 transform translate-x-full"
                  enter-to-class="opacity-100 transform translate-x-0"
                  leave-active-class="transition ease-in duration-200"
                  leave-from-class="opacity-100 transform translate-x-0"
                  leave-to-class="opacity-0 transform -translate-x-full"
                >
                  <RegisterForm
                    v-if="currentView === 'register'"
                    ref="registerFormRef"
                    @switch-to-login="switchToLogin"
                    @register-success="handleAuthSuccess"
                  />
                </Transition>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'

// Props and Emits
interface Props {
  modelValue: boolean
  initialView?: 'login' | 'register'
  redirectTo?: string
  allowBackdropClose?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'authSuccess', user: any): void
  (e: 'close'): void
}

const props = withDefaults(defineProps<Props>(), {
  initialView: 'login',
  redirectTo: '/',
  allowBackdropClose: true
})

const emit = defineEmits<Emits>()

// Router and stores
const router = useRouter()
const authStore = useAuthStore()

// State
const isVisible = ref(false)
const currentView = ref<'login' | 'register'>(props.initialView)
const loginFormRef = ref<InstanceType<typeof LoginForm>>()
const registerFormRef = ref<InstanceType<typeof RegisterForm>>()

// Watch for modelValue changes
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue) {
      open()
    } else {
      close()
    }
  },
  { immediate: true }
)

// Watch for initial view changes
watch(
  () => props.initialView,
  (newView) => {
    currentView.value = newView
  }
)

// Methods
const open = () => {
  isVisible.value = true
  currentView.value = props.initialView
  document.body.style.overflow = 'hidden'
  
  // Focus management
  nextTick(() => {
    const firstInput = document.querySelector('.modal input') as HTMLInputElement
    if (firstInput) {
      firstInput.focus()
    }
  })
}

const close = () => {
  isVisible.value = false
  document.body.style.overflow = ''
  emit('update:modelValue', false)
  emit('close')
  
  // Clear forms when closing
  nextTick(() => {
    loginFormRef.value?.clearForm()
    registerFormRef.value?.clearForm()
  })
}

const switchToLogin = () => {
  currentView.value = 'login'
  nextTick(() => {
    registerFormRef.value?.clearForm()
  })
}

const switchToRegister = () => {
  currentView.value = 'register'
  nextTick(() => {
    loginFormRef.value?.clearForm()
  })
}

const handleBackdropClick = () => {
  if (props.allowBackdropClose) {
    close()
  }
}

const handleAuthSuccess = async () => {
  const user = authStore.user
  
  // Emit success event
  emit('authSuccess', user)
  
  // Close modal
  close()
  
  // Start token refresh timer
  authStore.startTokenRefreshTimer()
  
  // Redirect if needed
  if (props.redirectTo && props.redirectTo !== router.currentRoute.value.path) {
    await router.push(props.redirectTo)
  }
}

// Keyboard event handlers
const handleKeydown = (event: KeyboardEvent) => {
  if (!isVisible.value) return
  
  if (event.key === 'Escape' && props.allowBackdropClose) {
    close()
  }
  
  // Tab trapping
  if (event.key === 'Tab') {
    const modal = document.querySelector('.modal')
    if (!modal) return
    
    const focusableElements = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    
    const firstElement = focusableElements[0] as HTMLElement
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement
    
    if (event.shiftKey) {
      if (document.activeElement === firstElement) {
        lastElement.focus()
        event.preventDefault()
      }
    } else {
      if (document.activeElement === lastElement) {
        firstElement.focus()
        event.preventDefault()
      }
    }
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})

// Expose methods
defineExpose({
  open,
  close,
  switchToLogin,
  switchToRegister
})
</script>

<style scoped>
.modal {
  /* Add class for tab trapping */
}

/* Prevent body scroll when modal is open */
:deep(body.modal-open) {
  overflow: hidden;
}

/* Custom scrollbar for modal content */
:deep(.overflow-y-auto::-webkit-scrollbar) {
  width: 6px;
}

:deep(.overflow-y-auto::-webkit-scrollbar-track) {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

:deep(.overflow-y-auto::-webkit-scrollbar-thumb) {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

:deep(.overflow-y-auto::-webkit-scrollbar-thumb:hover) {
  background: rgba(0, 0, 0, 0.5);
}

/* Dark mode scrollbar */
:deep(.dark .overflow-y-auto::-webkit-scrollbar-track) {
  background: rgba(255, 255, 255, 0.1);
}

:deep(.dark .overflow-y-auto::-webkit-scrollbar-thumb) {
  background: rgba(255, 255, 255, 0.3);
}

:deep(.dark .overflow-y-auto::-webkit-scrollbar-thumb:hover) {
  background: rgba(255, 255, 255, 0.5);
}
</style>