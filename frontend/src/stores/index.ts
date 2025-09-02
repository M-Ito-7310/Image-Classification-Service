import { createPinia } from 'pinia'

// Create pinia instance
export const pinia = createPinia()

// Store exports
export { useUploadStore } from './upload'
export { useClassificationStore } from './classification'
export { useSettingsStore } from './settings'
export { useErrorStore } from './error'
export { useAuthStore } from './auth'

// Types
export type { Theme, Language, UserSettings } from './settings'
export type { AppError, ErrorAction } from './error'

// Pinia plugins could be added here if needed
// Example: pinia.use(somePlugin)

export default pinia