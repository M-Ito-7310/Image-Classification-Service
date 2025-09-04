import { computed } from 'vue'
import i18n from '@/i18n'
import type { ClassificationPrediction } from '@/types/api'

/**
 * Converts ImageNet class names to normalized keys for translation lookup
 * @param className - Original class name from ImageNet (e.g., "Egyptian cat", "web site")
 * @returns Normalized key for i18n lookup
 */
function normalizeClassName(className: string): string {
  return className
    .toLowerCase()
    .replace(/[\s-]+/g, '_')  // Replace spaces and hyphens with underscores
    .replace(/[^\w]/g, '')    // Remove non-word characters except underscores
}

/**
 * Translates a single ImageNet class name to the current locale
 * @param className - Original ImageNet class name
 * @returns Translated class name or original if translation not found
 */
export function translateClassName(className: string): string {
  const normalizedKey = normalizeClassName(className)
  
  // Try to get translation from imagenet section
  const translationKey = `imagenet.${normalizedKey}`
  
  // Check if translation exists in current locale
  if (i18n.global.te(translationKey)) {
    return i18n.global.t(translationKey)
  }
  
  // Fallback: return original class name with proper formatting
  return className
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

/**
 * Translates classification predictions to current locale
 * @param predictions - Array of classification predictions
 * @returns Array of predictions with translated class names
 */
export function translatePredictions(predictions: ClassificationPrediction[]): ClassificationPrediction[] {
  return predictions.map(prediction => ({
    ...prediction,
    class_name: translateClassName(prediction.class_name)
  }))
}

/**
 * Checks if a class name has translation available in current locale
 * @param className - ImageNet class name to check
 * @returns True if translation exists, false otherwise
 */
export function hasTranslation(className: string): boolean {
  const normalizedKey = normalizeClassName(className)
  const translationKey = `imagenet.${normalizedKey}`
  return i18n.global.te(translationKey)
}

/**
 * Gets all available translations for a class name across all locales
 * @param className - ImageNet class name
 * @returns Object with locale keys and translated values
 */
export function getAllTranslations(className: string): Record<string, string> {
  const normalizedKey = normalizeClassName(className)
  const translationKey = `imagenet.${normalizedKey}`
  const translations: Record<string, string> = {}
  
  // Get available locales
  const availableLocales = i18n.global.availableLocales
  
  availableLocales.forEach(locale => {
    // Temporarily switch locale to get translation
    const originalLocale = i18n.global.locale.value
    i18n.global.locale.value = locale as 'ja' | 'en'
    
    if (i18n.global.te(translationKey)) {
      translations[locale] = i18n.global.t(translationKey)
    }
    
    // Restore original locale
    i18n.global.locale.value = originalLocale
  })
  
  return translations
}

/**
 * Reactive translation function that updates when locale changes
 * @param className - ImageNet class name to translate
 * @returns Translated class name that updates with locale changes
 */
export function useTranslatedClassName(className: string) {
  const { t, te, locale } = i18n.global
  const normalizedKey = normalizeClassName(className)
  const translationKey = `imagenet.${normalizedKey}`
  
  // Return a computed ref that updates when locale changes
  return computed(() => {
    if (te(translationKey)) {
      return t(translationKey)
    }
    
    // Fallback formatting
    return className
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  })
}

/**
 * Utility to format class names for display
 * @param className - Class name to format
 * @returns Properly formatted display name
 */
export function formatClassNameForDisplay(className: string): string {
  return className
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}