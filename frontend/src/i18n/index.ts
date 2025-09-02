import { createI18n } from 'vue-i18n'
import ja from './locales/ja'
import en from './locales/en'

export type MessageSchema = typeof ja

// Get saved language from localStorage or detect from browser
const getSavedLanguage = (): string => {
  const saved = localStorage.getItem('language')
  if (saved && ['ja', 'en'].includes(saved)) {
    return saved
  }
  
  // Detect from browser
  const browserLang = navigator.language.toLowerCase()
  if (browserLang.startsWith('ja')) {
    return 'ja'
  }
  return 'en'
}

const i18n = createI18n<[MessageSchema], 'ja' | 'en'>({
  legacy: false, // Use Composition API
  locale: getSavedLanguage(),
  fallbackLocale: 'en',
  messages: {
    ja,
    en
  },
  globalInjection: true,
  missingWarn: false,
  fallbackWarn: false
})

// Save language preference when changed
export const setLanguage = (lang: 'ja' | 'en') => {
  i18n.global.locale.value = lang
  localStorage.setItem('language', lang)
  document.documentElement.lang = lang
}

// Export for use in components
export default i18n