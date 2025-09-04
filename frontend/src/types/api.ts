// API Response Types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: ApiError
  message?: string
}

export interface ApiError {
  code: string
  message: string
  details?: Record<string, any>
}

// Classification Types
export interface ClassificationPrediction {
  class_name: string
  confidence: number
  class_id: string | number
}

export interface ClassificationResult {
  id?: string
  predictions: ClassificationPrediction[]
  confidence_scores?: Record<string, number>
  processing_time: number
  model_used: string
  threshold_applied?: number
  image_metadata?: ImageMetadata
  image_url?: string
  filename?: string
}

export interface ImageMetadata {
  filename: string
  size: number
  format: string
  dimensions: [number, number]
  width?: number
  height?: number
  has_transparency?: boolean
}

// Classification History Types
export interface ClassificationHistory {
  id: number
  image_filename: string
  image_path: string
  model_name: string
  predictions: ClassificationPrediction[]
  processing_time: number
  confidence_score: number
  created_at: string
}

export interface ClassificationStats {
  total_classifications: number
  monthly_classifications: number
  daily_classifications: number
  average_accuracy: number
  average_processing_time: number
  most_used_models: Array<{
    name: string
    count: number
  }>
}

// Model Types
export interface ModelInfo {
  name: string
  description: string
  version?: string
  classes: number | string[]
  input_size?: [number, number]
  status: 'active' | 'inactive' | 'loading'
  accuracy?: number
  inference_time?: number
  categories?: string[]
  provider?: string
  created_at?: string
  updated_at?: string
  metadata?: Record<string, any>
  performance_metrics?: {
    top1_accuracy?: number
    top5_accuracy?: number
    f1_score?: number
    inference_time_ms?: number
  }
}

export interface ModelsResponse {
  available_models: ModelInfo[]
  default_model?: string
}

// Health Check Types
export interface HealthCheck {
  status: 'healthy' | 'unhealthy'
  timestamp: string
  version?: string
  services?: Record<string, string>
  system?: {
    cpu_percent?: number
    memory_percent?: number
    disk_percent?: number
  }
}

// Upload Types
export interface UploadOptions {
  model?: string
  threshold?: number
  max_results?: number
  enhance_image?: boolean
  language?: 'ja' | 'en'
}

export interface UploadProgress {
  loaded: number
  total: number
  percentage: number
}

// Classification History Types (for future use)
export interface ClassificationHistory {
  id: string
  filename: string
  model_used: string
  predictions: ClassificationPrediction[]
  processing_time: number
  created_at: string
  image_url?: string
  user_id?: string
}

export interface HistoryResponse {
  history: ClassificationHistory[]
  pagination?: {
    total: number
    limit: number
    offset: number
    has_next: boolean
  }
}

// Error Types
export interface ValidationError {
  field: string
  message: string
  code?: string
}

export interface HttpError extends Error {
  status: number
  statusText: string
  data?: any
}

// Authentication Types
export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  is_admin: boolean
  created_at: string
  last_login?: string
}

export interface UserLogin {
  username: string
  password: string
}

export interface UserRegister {
  username: string
  email: string
  password: string
  full_name?: string
}

export interface Token {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface AuthResponse {
  user: User
  token: Token
  message: string
}

export interface UserSession {
  id: number
  session_token: string
  expires_at: string
  created_at: string
  is_active: boolean
  user_agent?: string
  ip_address?: string
}