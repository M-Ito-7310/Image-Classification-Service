import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export type Theme = 'light' | 'dark' | 'system'
export type Language = 'en' | 'ja'

export interface UserSettings {
  theme: Theme
  language: Language
  autoSave: boolean
  showAdvancedOptions: boolean
  defaultModel: string
  defaultThreshold: number
  defaultMaxResults: number
  enableImageEnhancement: boolean
  showProcessingDetails: boolean
  enableNotifications: boolean
  saveHistory: boolean
  maxHistoryItems: number
}

const DEFAULT_SETTINGS: UserSettings = {
  theme: 'system',
  language: 'ja',
  autoSave: true,
  showAdvancedOptions: false,
  defaultModel: 'default',
  defaultThreshold: 0.5,
  defaultMaxResults: 5,
  enableImageEnhancement: false,
  showProcessingDetails: true,
  enableNotifications: true,
  saveHistory: true,
  maxHistoryItems: 100
}

export const useSettingsStore = defineStore('settings', () => {
  // State
  const settings = ref<UserSettings>({ ...DEFAULT_SETTINGS })
  const isLoaded = ref(false)

  // Computed
  const isDarkMode = computed(() => {
    if (settings.value.theme === 'dark') return true
    if (settings.value.theme === 'light') return false
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  })

  const currentLanguage = computed(() => settings.value.language)
  const isJapanese = computed(() => settings.value.language === 'ja')
  const isEnglish = computed(() => settings.value.language === 'en')

  // Load settings from localStorage
  const loadSettings = () => {
    try {
      const stored = localStorage.getItem('classification-settings')
      if (stored) {
        const parsedSettings = JSON.parse(stored)
        settings.value = { ...DEFAULT_SETTINGS, ...parsedSettings }
      }
    } catch (error) {
      console.warn('Failed to load settings from localStorage:', error)
      settings.value = { ...DEFAULT_SETTINGS }
    }
    isLoaded.value = true
  }

  // Save settings to localStorage
  const saveSettings = () => {
    try {
      localStorage.setItem('classification-settings', JSON.stringify(settings.value))
    } catch (error) {
      console.error('Failed to save settings to localStorage:', error)
    }
  }

  // Update specific setting
  const updateSetting = <K extends keyof UserSettings>(
    key: K,
    value: UserSettings[K]
  ) => {
    settings.value[key] = value
    if (settings.value.autoSave) {
      saveSettings()
    }
  }

  // Update multiple settings
  const updateSettings = (newSettings: Partial<UserSettings>) => {
    settings.value = { ...settings.value, ...newSettings }
    if (settings.value.autoSave) {
      saveSettings()
    }
  }

  // Reset to defaults
  const resetSettings = () => {
    settings.value = { ...DEFAULT_SETTINGS }
    if (settings.value.autoSave) {
      saveSettings()
    }
  }

  // Theme management
  const setTheme = (theme: Theme) => {
    updateSetting('theme', theme)
    applyTheme()
  }

  const toggleTheme = () => {
    const currentTheme = settings.value.theme
    const newTheme: Theme = currentTheme === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
  }

  const applyTheme = () => {
    const html = document.documentElement
    
    if (isDarkMode.value) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
  }

  // Language management
  const setLanguage = (language: Language) => {
    updateSetting('language', language)
    
    // Update document language attribute
    document.documentElement.lang = language
  }

  const toggleLanguage = () => {
    const newLanguage: Language = settings.value.language === 'en' ? 'ja' : 'en'
    setLanguage(newLanguage)
  }

  // Model defaults
  const updateModelDefaults = (config: {
    defaultModel?: string
    defaultThreshold?: number
    defaultMaxResults?: number
    enableImageEnhancement?: boolean
  }) => {
    updateSettings(config)
  }

  // UI preferences
  const updateUIPreferences = (config: {
    showAdvancedOptions?: boolean
    showProcessingDetails?: boolean
    enableNotifications?: boolean
  }) => {
    updateSettings(config)
  }

  // History preferences
  const updateHistoryPreferences = (config: {
    saveHistory?: boolean
    maxHistoryItems?: number
  }) => {
    updateSettings(config)
  }

  // Export settings
  const exportSettings = () => {
    const exportData = {
      version: '1.0',
      timestamp: new Date().toISOString(),
      settings: settings.value
    }
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: 'application/json'
    })
    
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `classification-settings-${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  // Import settings
  const importSettings = (file: File): Promise<boolean> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      
      reader.onload = (event) => {
        try {
          const data = JSON.parse(event.target?.result as string)
          
          if (data.settings && typeof data.settings === 'object') {
            // Validate and merge with defaults
            const importedSettings = { ...DEFAULT_SETTINGS, ...data.settings }
            settings.value = importedSettings
            saveSettings()
            resolve(true)
          } else {
            throw new Error('Invalid settings file format')
          }
        } catch (error) {
          console.error('Failed to import settings:', error)
          reject(error)
        }
      }
      
      reader.onerror = () => {
        reject(new Error('Failed to read settings file'))
      }
      
      reader.readAsText(file)
    })
  }

  // Validation helpers
  const validateThreshold = (value: number): boolean => {
    return value >= 0 && value <= 1
  }

  const validateMaxResults = (value: number): boolean => {
    return value >= 1 && value <= 20
  }

  const validateMaxHistoryItems = (value: number): boolean => {
    return value >= 0 && value <= 1000
  }

  // Watch for system theme changes
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  const handleSystemThemeChange = () => {
    if (settings.value.theme === 'system') {
      applyTheme()
    }
  }

  // Initialize
  const initialize = () => {
    loadSettings()
    applyTheme()
    
    // Listen for system theme changes
    mediaQuery.addEventListener('change', handleSystemThemeChange)
    
    // Watch for theme changes
    watch(() => settings.value.theme, applyTheme)
  }

  // Cleanup
  const cleanup = () => {
    mediaQuery.removeEventListener('change', handleSystemThemeChange)
  }

  return {
    // State
    settings,
    isLoaded,

    // Computed
    isDarkMode,
    currentLanguage,
    isJapanese,
    isEnglish,

    // Actions
    loadSettings,
    saveSettings,
    updateSetting,
    updateSettings,
    resetSettings,
    setTheme,
    toggleTheme,
    applyTheme,
    setLanguage,
    toggleLanguage,
    updateModelDefaults,
    updateUIPreferences,
    updateHistoryPreferences,
    exportSettings,
    importSettings,
    validateThreshold,
    validateMaxResults,
    validateMaxHistoryItems,
    initialize,
    cleanup
  }
})