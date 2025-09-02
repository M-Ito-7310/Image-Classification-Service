/**
 * Classification result caching system for performance optimization
 */

export interface CacheEntry {
  id: string
  filename: string
  fileHash: string
  result: any
  timestamp: number
  modelUsed: string
  expiresAt: number
}

export interface CacheStats {
  totalEntries: number
  hitRate: number
  memoryUsage: number
  oldestEntry: number
  newestEntry: number
}

export class ResultCache {
  private static readonly CACHE_KEY = 'imageClassificationCache'
  private static readonly DEFAULT_TTL = 24 * 60 * 60 * 1000 // 24 hours
  private static readonly MAX_ENTRIES = 1000
  private static cache = new Map<string, CacheEntry>()
  private static hits = 0
  private static misses = 0

  /**
   * Initialize cache from localStorage
   */
  static initialize(): void {
    try {
      const stored = localStorage.getItem(this.CACHE_KEY)
      if (stored) {
        const entries: CacheEntry[] = JSON.parse(stored)
        entries.forEach(entry => {
          if (entry.expiresAt > Date.now()) {
            this.cache.set(entry.id, entry)
          }
        })
      }
    } catch (error) {
      console.warn('Failed to initialize cache:', error)
    }
  }

  /**
   * Generate file hash for caching
   */
  private static async generateFileHash(file: File): Promise<string> {
    const buffer = await file.arrayBuffer()
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer)
    const hashArray = Array.from(new Uint8Array(hashBuffer))
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
  }

  /**
   * Generate cache key
   */
  private static generateCacheKey(fileHash: string, modelName: string): string {
    return `${fileHash}_${modelName}`
  }

  /**
   * Check if result exists in cache
   */
  static async has(file: File, modelName: string): Promise<boolean> {
    try {
      const fileHash = await this.generateFileHash(file)
      const key = this.generateCacheKey(fileHash, modelName)
      const entry = this.cache.get(key)
      
      if (entry && entry.expiresAt > Date.now()) {
        return true
      } else if (entry) {
        // Remove expired entry
        this.cache.delete(key)
        this.persist()
      }
      
      return false
    } catch (error) {
      console.error('Cache check error:', error)
      return false
    }
  }

  /**
   * Get cached result
   */
  static async get(file: File, modelName: string): Promise<any | null> {
    try {
      const fileHash = await this.generateFileHash(file)
      const key = this.generateCacheKey(fileHash, modelName)
      const entry = this.cache.get(key)
      
      if (entry && entry.expiresAt > Date.now()) {
        this.hits++
        return entry.result
      } else if (entry) {
        // Remove expired entry
        this.cache.delete(key)
        this.persist()
      }
      
      this.misses++
      return null
    } catch (error) {
      console.error('Cache get error:', error)
      this.misses++
      return null
    }
  }

  /**
   * Store result in cache
   */
  static async set(
    file: File, 
    modelName: string, 
    result: any, 
    ttl: number = this.DEFAULT_TTL
  ): Promise<void> {
    try {
      const fileHash = await this.generateFileHash(file)
      const key = this.generateCacheKey(fileHash, modelName)
      
      const entry: CacheEntry = {
        id: key,
        filename: file.name,
        fileHash,
        result,
        timestamp: Date.now(),
        modelUsed: modelName,
        expiresAt: Date.now() + ttl
      }

      this.cache.set(key, entry)
      
      // Clean up if cache is too large
      if (this.cache.size > this.MAX_ENTRIES) {
        this.cleanup()
      }
      
      this.persist()
    } catch (error) {
      console.error('Cache set error:', error)
    }
  }

  /**
   * Remove expired entries and oldest entries if needed
   */
  private static cleanup(): void {
    const now = Date.now()
    const entries = Array.from(this.cache.entries())
    
    // Remove expired entries
    entries.forEach(([key, entry]) => {
      if (entry.expiresAt <= now) {
        this.cache.delete(key)
      }
    })

    // If still too many entries, remove oldest ones
    if (this.cache.size > this.MAX_ENTRIES) {
      const remaining = Array.from(this.cache.entries())
        .sort(([, a], [, b]) => a.timestamp - b.timestamp)
        .slice(-(this.MAX_ENTRIES - 100)) // Keep most recent entries

      this.cache.clear()
      remaining.forEach(([key, entry]) => {
        this.cache.set(key, entry)
      })
    }
  }

  /**
   * Persist cache to localStorage
   */
  private static persist(): void {
    try {
      const entries = Array.from(this.cache.values())
      localStorage.setItem(this.CACHE_KEY, JSON.stringify(entries))
    } catch (error) {
      console.warn('Failed to persist cache:', error)
      // If localStorage is full, try to clear old entries
      this.cleanup()
      try {
        const entries = Array.from(this.cache.values())
        localStorage.setItem(this.CACHE_KEY, JSON.stringify(entries))
      } catch (retryError) {
        console.error('Failed to persist cache after cleanup:', retryError)
      }
    }
  }

  /**
   * Clear all cache entries
   */
  static clear(): void {
    this.cache.clear()
    this.hits = 0
    this.misses = 0
    localStorage.removeItem(this.CACHE_KEY)
  }

  /**
   * Get cache statistics
   */
  static getStats(): CacheStats {
    const entries = Array.from(this.cache.values())
    const now = Date.now()
    
    return {
      totalEntries: entries.length,
      hitRate: this.hits + this.misses > 0 ? this.hits / (this.hits + this.misses) : 0,
      memoryUsage: new Blob([JSON.stringify(entries)]).size,
      oldestEntry: entries.length > 0 ? Math.min(...entries.map(e => e.timestamp)) : now,
      newestEntry: entries.length > 0 ? Math.max(...entries.map(e => e.timestamp)) : now
    }
  }

  /**
   * Remove entries for specific model
   */
  static clearModel(modelName: string): void {
    const toRemove: string[] = []
    
    this.cache.forEach((entry, key) => {
      if (entry.modelUsed === modelName) {
        toRemove.push(key)
      }
    })
    
    toRemove.forEach(key => this.cache.delete(key))
    this.persist()
  }

  /**
   * Get cached results for specific model
   */
  static getModelResults(modelName: string): CacheEntry[] {
    return Array.from(this.cache.values())
      .filter(entry => entry.modelUsed === modelName && entry.expiresAt > Date.now())
      .sort((a, b) => b.timestamp - a.timestamp)
  }

  /**
   * Preload frequently used results
   */
  static preloadFrequentResults(): void {
    // This could be enhanced to preload based on usage patterns
    const stats = this.getStats()
    console.log('Cache statistics:', stats)
  }
}

// Initialize cache when module loads
ResultCache.initialize()

// Auto-cleanup every 5 minutes
setInterval(() => {
  const entries = Array.from(ResultCache['cache'].values())
  const expired = entries.filter(entry => entry.expiresAt <= Date.now()).length
  
  if (expired > 0) {
    ResultCache['cleanup']()
    console.log(`Cleaned up ${expired} expired cache entries`)
  }
}, 5 * 60 * 1000)