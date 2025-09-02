export default {
  common: {
    appName: 'AI Image Classification Service',
    loading: 'Loading...',
    error: 'Error',
    success: 'Success',
    warning: 'Warning',
    cancel: 'Cancel',
    confirm: 'Confirm',
    delete: 'Delete',
    edit: 'Edit',
    save: 'Save',
    close: 'Close',
    search: 'Search',
    filter: 'Filter',
    export: 'Export',
    import: 'Import',
    download: 'Download',
    upload: 'Upload',
    processing: 'Processing...',
    noData: 'No data available',
    selectAll: 'Select all',
    clearAll: 'Clear all',
    actions: 'Actions',
    view: 'View',
    refresh: 'Refresh',
    back: 'Back',
    next: 'Next',
    previous: 'Previous',
    yes: 'Yes',
    no: 'No'
  },
  
  nav: {
    home: 'Home',
    classify: 'Classify',
    history: 'History',
    settings: 'Settings',
    about: 'About',
    dashboard: 'Dashboard',
    profile: 'Profile',
    login: 'Login',
    register: 'Register',
    logout: 'Logout'
  },

  home: {
    title: 'AI Image',
    subtitle: 'Classification Service',
    description: 'Advanced AI-powered image classification with high accuracy. Easy drag & drop upload, real-time analysis, and detailed result visualization.',
    startClassifying: 'Start Classifying',
    stats: {
      accuracy: 'Classification Accuracy',
      speed: 'Processing Time',
      classes: 'Supported Classes'
    },
    features: {
      upload: {
        title: 'Easy Upload',
        description: 'Simple drag & drop or click to upload images. Support for batch processing of multiple files.'
      },
      analysis: {
        title: 'High-Precision AI Analysis',
        description: 'State-of-the-art deep learning models for accurate image classification with confidence scores.'
      },
      results: {
        title: 'Detailed Results Display',
        description: 'Clear visualization of classification results with confidence graphs, processing time, and metadata.'
      },
      formats: {
        title: 'Multiple Format Support',
        description: 'Support for major image formats including JPEG, PNG, WebP, BMP. Files up to 10MB supported.'
      },
      realtime: {
        title: 'Real-time Processing',
        description: 'Fast processing with real-time results display. Live progress tracking with progress bars.'
      },
      export: {
        title: 'Export Results',
        description: 'Export classification results in JSON or CSV format for data analysis and reporting.'
      }
    },
    howTo: {
      title: 'How to Use',
      step1: {
        title: 'Go to Classification Page',
        description: 'Click "Start Classifying" button to navigate to the dedicated page'
      },
      step2: {
        title: 'Upload Image',
        description: 'Drag & drop or click to upload images and configure classification options'
      },
      step3: {
        title: 'View AI Analysis Results',
        description: 'Review high-precision AI analysis results and export as needed'
      }
    },
    specs: {
      title: 'Technical Specifications',
      formats: 'Supported Formats',
      maxSize: 'Max File Size',
      concurrent: 'Concurrent Upload',
      speed: 'Processing Speed',
      formatsValue: 'JPEG, PNG, WebP, BMP',
      maxSizeValue: '10MB',
      concurrentValue: 'Up to 50 files',
      speedValue: 'Average <500ms'
    }
  },
  
  auth: {
    appName: 'AI Image Classifier',
    footer: {
      aboutService: 'About this service',
      backToHome: 'Back to Home',
      copyright: '© 2024 AI Image Classifier. All rights reserved.'
    },
    login: {
      title: 'Login',
      subtitle: 'Sign in to your account',
      username: 'Username or Email',
      usernamePlaceholder: 'Enter username or email',
      password: 'Password',
      passwordPlaceholder: 'Enter password',
      rememberMe: 'Remember me',
      forgotPassword: 'Forgot password?',
      submit: 'Sign In',
      submitting: 'Signing in...',
      noAccount: "Don't have an account?",
      signUp: 'Sign up',
      success: 'Login successful',
      error: 'Login failed',
      validation: {
        usernameRequired: 'Username or email is required',
        passwordRequired: 'Password is required',
        passwordMinLength: 'Password must be at least 8 characters'
      },
      demo: {
        title: 'Demo Accounts',
        description: 'Try our service instantly with these demo accounts',
        regularUser: 'Regular User',
        adminUser: 'Admin User',
        quickLogin: 'Quick Login',
        note: '* Demo purposes only, no real data included'
      }
    },
    register: {
      title: 'Register',
      subtitle: 'Let\'s create a new account',
      username: 'Username',
      usernamePlaceholder: 'Enter username (3-50 characters)',
      email: 'Email',
      emailPlaceholder: 'Enter email address',
      password: 'Password',
      passwordPlaceholder: 'Enter password (8-100 characters)',
      confirmPassword: 'Confirm Password',
      confirmPasswordPlaceholder: 'Re-enter password',
      fullName: 'Full Name (Optional)',
      fullNamePlaceholder: 'Enter full name (max 100 characters)',
      agreeTerms: 'I agree to the terms and conditions',
      submit: 'Create Account',
      submitting: 'Registering...',
      haveAccount: 'Already have an account?',
      signIn: 'Sign in',
      success: 'Registration successful',
      error: 'Registration failed',
      required: 'Required',
      passwordStrength: {
        weak: 'Weak',
        medium: 'Medium',
        strong: 'Strong'
      },
      validation: {
        usernameRequired: 'Username is required',
        usernameMinLength: 'Username must be at least 3 characters',
        usernameMaxLength: 'Username must be within 50 characters',
        usernameInvalid: 'Username can only contain letters, numbers, underscores, and hyphens',
        emailRequired: 'Email address is required',
        emailInvalid: 'Please enter a valid email address',
        fullNameMaxLength: 'Full name must be within 100 characters',
        passwordRequired: 'Password is required',
        passwordMinLength: 'Password must be at least 8 characters',
        passwordMaxLength: 'Password must be within 100 characters',
        confirmPasswordRequired: 'Password confirmation is required',
        confirmPasswordMismatch: 'Passwords do not match'
      }
    },
    logout: {
      message: 'You have been logged out',
      confirm: 'Are you sure you want to logout?'
    },
    errors: {
      invalidCredentials: 'Invalid username or password',
      userExists: 'Username already exists',
      emailExists: 'Email already registered',
      passwordMismatch: 'Passwords do not match',
      weakPassword: 'Password must be at least 8 characters',
      required: 'This field is required'
    }
  },
  
  classification: {
    title: 'Image Classification',
    subtitle: 'Upload images for AI-powered automatic classification',
    emptyState: {
      title: 'Please select an image',
      description: 'Drag & drop an image to the area above or click to select a file',
      supportedFormats: 'Supported formats: JPEG, PNG, WebP, BMP • Max 10MB'
    },
    upload: {
      title: 'Upload Image',
      description: 'Drag and drop image here or click to select',
      button: 'Choose File',
      dragActive: 'Drop here',
      formats: 'Supported: JPEG, PNG, WebP, BMP',
      maxSize: 'Max file size: 10MB',
      processing: 'Processing image...',
      error: 'Upload error',
      uploading: 'Uploading... {progress}%',
      startUpload: 'Start Upload',
      enhanceImages: 'Enhance images with preprocessing',
      duplicatesSkipped: '{count} duplicate files skipped',
      analyzingImages: 'Analyzing {count} images...',
      options: 'Classification Options',
      selectedFiles: 'Selected Files',
      removeAll: 'Remove All',
      totalSize: 'Total Size',
      model: 'Model',
      maxResults: 'Max Results',
      confidenceThreshold: 'Confidence Threshold'
    },
    results: {
      title: 'Classification Results',
      confidence: 'Confidence',
      model: 'Model Used',
      processingTime: 'Processing Time',
      topPredictions: 'Top Predictions',
      noResults: 'No results',
      tryAgain: 'Try Again',
      saveToHistory: 'Save to History',
      download: 'Download Results'
    },
    batch: {
      title: 'Batch Processing',
      selectFiles: 'Select Files',
      processing: 'Processing {current}/{total}',
      completed: 'Completed',
      failed: 'Failed',
      results: 'Batch Results'
    },
    models: {
      select: 'Select Model',
      default: 'Default',
      custom: 'Custom',
      performance: 'Performance',
      accuracy: 'Accuracy'
    },
    status: {
      uploaded: 'Uploaded',
      active: 'Active',
      error: 'Error',
      validating: 'Validating'
    },
    guide: {
      title: 'How to Use Guide',
      howToUse: 'How to Use',
      steps: {
        upload: {
          title: 'Upload Images',
          description: 'Upload image files to start the AI analysis process',
          method1: 'Drag & Drop: Drag image files and drop them onto the upload area',
          method2: 'Click Selection: Click "Choose File" button to select from file browser',
          method3: 'Multiple Files: Hold Ctrl/Cmd and select multiple images for batch upload'
        },
        options: {
          title: 'Configure Classification Options',
          description: 'Set options to optimize AI analysis accuracy and results',
          model: 'AI Model Selection',
          modelDesc: 'Choose default model or custom model based on your use case',
          confidence: 'Confidence Threshold',
          confidenceDesc: 'Set minimum confidence level for displayed results (recommended: 0.1-0.9)',
          maxResults: 'Maximum Results',
          maxResultsDesc: 'Set maximum number of classification results to display (range: 1-20)',
          preprocessing: 'Preprocessing Options',
          preprocessingDesc: 'Enable automatic preprocessing to enhance image quality'
        },
        results: {
          title: 'Review Analysis Results',
          description: 'View detailed AI image analysis results and insights',
          confidence: 'Confidence Score',
          confidenceDesc: 'Displays certainty percentage for each classification result (higher = more accurate)',
          ranking: 'Ranking Display',
          rankingDesc: 'Results displayed in confidence order, with top results being most likely classifications',
          metadata: 'Metadata Information',
          metadataDesc: 'Detailed data including processing time, model used, and file information'
        },
        export: {
          title: 'Export Results',
          description: 'Export analysis results in various formats for further use',
          jsonDesc: 'Export as structured data, ideal for programmatic processing',
          csvDesc: 'Export in spreadsheet format, convenient for analysis in spreadsheet software',
          reportTitle: 'Detailed Report',
          reportDesc: 'Generate comprehensive report with images and results, perfect for presentations'
        }
      },
      navigation: {
        previous: 'Previous',
        next: 'Next',
        done: 'Done'
      }
    }
  },
  
  history: {
    title: 'Classification History',
    subtitle: 'View all your previous image classification results',
    empty: 'No history available',
    emptySubtitle: 'When you classify images, they will appear here',
    classifyNow: 'Classify Images',
    searchPlaceholder: 'Search by filename...',
    clearHistory: 'Clear History',
    stats: {
      totalClassifications: 'Total Classifications',
      totalPredictions: 'Total Predictions',
      averageProcessingTime: 'Avg Processing Time',
      uniqueModels: 'Models Used'
    },
    results: {
      title: 'Classification Results',
      count: '{count} items'
    },
    messages: {
      downloadComplete: 'Download Complete',
      downloadSuccess: 'History item downloaded successfully',
      clearConfirm: 'Are you sure you want to delete all history? This action cannot be undone.',
      historyCleared: 'History Cleared',
      allHistoryDeleted: 'All history has been deleted'
    },
    filters: {
      all: 'All',
      today: 'Today',
      week: 'This Week',
      month: 'This Month',
      model: 'Model',
      dateRange: 'Date Range'
    },
    table: {
      image: 'Image',
      result: 'Result',
      confidence: 'Confidence',
      model: 'Model',
      date: 'Date',
      actions: 'Actions'
    },
    actions: {
      view: 'View Details',
      delete: 'Delete',
      download: 'Download',
      reprocess: 'Reprocess',
      details: 'Details'
    },
    confirm: {
      delete: 'Are you sure you want to delete this record?',
      deleteAll: 'Are you sure you want to delete all history?',
      export: 'Export history?'
    }
  },
  
  dashboard: {
    title: 'Dashboard',
    welcome: 'Welcome, {name}',
    stats: {
      totalImages: 'Images Classified',
      monthlyImages: 'This Month',
      accuracy: 'Average Accuracy',
      processingTime: 'Avg Processing Time'
    },
    recentActivity: {
      title: 'Recent Classifications',
      empty: 'No classifications yet',
      viewAll: 'View All'
    },
    quickActions: {
      title: 'Quick Actions',
      classify: 'Classify Image',
      viewHistory: 'View History',
      settings: 'Settings',
      profile: 'Edit Profile'
    },
    accountInfo: {
      title: 'Account Info',
      registeredDate: 'Registered',
      lastLogin: 'Last Login',
      plan: 'Plan',
      usage: 'Usage'
    }
  },
  
  profile: {
    title: 'Profile',
    subtitle: 'View and update your account information',
    personalInfo: {
      title: 'Basic Information',
      username: 'Username',
      email: 'Email Address',
      fullName: 'Full Name',
      fullNameOptional: 'Full Name (Optional)',
      fullNamePlaceholder: 'Enter full name',
      accountType: 'Account Type',
      registeredDate: 'Registered',
      lastLogin: 'Last Login',
      notSet: 'Not set',
      admin: 'Administrator',
      regularUser: 'Regular User',
      bio: 'Bio',
      avatar: 'Avatar'
    },
    security: {
      title: 'Change Password',
      changePassword: 'Change Password',
      currentPassword: 'Current Password',
      newPassword: 'New Password',
      confirmPassword: 'Confirm Password',
      twoFactor: 'Two-Factor Authentication',
      sessions: 'Active Sessions',
      sessionsLoading: 'Loading session information...',
      unknownDevice: 'Unknown Device',
      terminateSession: 'Terminate'
    },
    preferences: {
      title: 'Preferences',
      language: 'Language',
      theme: 'Theme',
      notifications: 'Notifications',
      privacy: 'Privacy'
    },
    actions: {
      edit: 'Edit',
      save: 'Save',
      saving: 'Saving...',
      change: 'Change',
      changing: 'Changing...',
      cancel: 'Cancel',
      deleteAccount: 'Delete Account',
      exportData: 'Export Data'
    },
    messages: {
      profileUpdated: 'Profile updated successfully',
      profileUpdateFailed: 'Failed to update profile',
      passwordChanged: 'Password changed successfully',
      passwordChangeFailed: 'Failed to change password',
      sessionTerminated: 'Session terminated successfully',
      sessionTerminateFailed: 'Failed to terminate session'
    },
    validation: {
      emailRequired: 'Email address is required',
      emailInvalid: 'Please enter a valid email address',
      fullNameMaxLength: 'Full name must be within 100 characters'
    }
  },
  
  settings: {
    title: 'Settings',
    subtitle: 'Customize application behavior and preferences',
    general: {
      title: 'General',
      language: 'Language',
      dateFormat: 'Date Format',
      timezone: 'Timezone'
    },
    appearance: {
      title: 'Appearance',
      theme: 'Theme',
      darkMode: 'Dark Mode',
      colorScheme: 'Color Scheme',
      fontSize: 'Font Size',
      animations: 'Animations',
      themes: {
        light: 'Light',
        dark: 'Dark'
      }
    },
    classification: {
      title: 'Classification Settings',
      defaultModel: 'Default Model',
      defaultThreshold: 'Default Confidence Threshold',
      defaultMaxResults: 'Default Max Results',
      enableImageEnhancement: 'Enable image preprocessing',
      enhancementDescription: 'Automatically improve image quality during upload',
      options: {
        default: 'Default'
      }
    },
    ui: {
      title: 'User Interface',
      showAdvancedOptions: 'Show advanced options',
      advancedDescription: 'Display more detailed configuration options',
      showProcessingDetails: 'Show processing details',
      processingDescription: 'Display detailed information like processing time and metadata',
      enableNotifications: 'Enable notifications',
      notificationsDescription: 'Show notifications when processing completes or errors occur'
    },
    history: {
      title: 'History Settings',
      saveHistory: 'Save classification history',
      saveDescription: 'Save classification results as history for later review',
      maxHistoryItems: 'Maximum history items',
      unlimitedNote: 'Set to 0 for unlimited storage'
    },
    dataManagement: {
      title: 'Data Management',
      autoSave: 'Auto-save',
      autoSaveDescription: 'Automatically save setting changes',
      exportSettings: 'Export Settings',
      importSettings: 'Import Settings'
    },
    reset: {
      title: 'Reset',
      description: 'Reset all settings to default values. This action cannot be undone.',
      confirm: 'Are you sure you want to reset all settings to default values? This action cannot be undone.',
      button: 'Reset All Settings'
    },
    messages: {
      importComplete: 'Import Complete',
      importSuccess: 'Settings imported successfully',
      importFailed: 'Failed to import settings',
      resetComplete: 'Settings Reset',
      resetSuccess: 'All settings have been reset to default values'
    },
    notifications: {
      title: 'Notifications',
      email: 'Email Notifications',
      browser: 'Browser Notifications',
      sound: 'Sound',
      frequency: 'Frequency'
    },
    api: {
      title: 'API Settings',
      key: 'API Key',
      endpoint: 'Endpoint',
      timeout: 'Timeout',
      retries: 'Retries'
    },
    advanced: {
      title: 'Advanced',
      cache: 'Cache',
      debug: 'Debug Mode',
      logs: 'Logs',
      reset: 'Reset Settings'
    }
  },
  
  errors: {
    general: 'An error occurred',
    network: 'Network error',
    server: 'Server error',
    notFound: 'Page not found',
    forbidden: 'Access denied',
    unauthorized: 'Authentication required',
    validation: 'Please check your input',
    fileSize: 'File size too large',
    fileType: 'Unsupported file type',
    upload: 'Upload failed',
    processing: 'Processing failed'
  },
  
  messages: {
    success: {
      saved: 'Saved successfully',
      deleted: 'Deleted successfully',
      updated: 'Updated successfully',
      uploaded: 'Uploaded successfully',
      exported: 'Exported successfully'
    },
    info: {
      loading: 'Loading...',
      processing: 'Processing...',
      saving: 'Saving...',
      uploading: 'Uploading...'
    },
    warning: {
      unsaved: 'You have unsaved changes',
      confirmDelete: 'Are you sure you want to delete?',
      confirmLogout: 'Are you sure you want to logout?'
    }
  },
  
  footer: {
    copyright: '© 2025 AI Image Classification Service',
    allRightsReserved: 'All rights reserved.',
    privacy: 'Privacy Policy',
    terms: 'Terms of Service',
    contact: 'Contact',
    about: 'About',
    description: 'Advanced AI-powered image classification service. Supports TensorFlow, PyTorch, and Google Cloud Vision API for high-precision image recognition.',
    quickLinks: 'Quick Links',
    techStack: 'Tech Stack',
    apiDocs: 'API Documentation',
    developmentPhase: 'Phase 3 in Development',
    subtitle: 'Recognition Service'
  },

  about: {
    title: 'AI Image Classification Service',
    subtitle: 'High-precision image classification system using cutting-edge deep learning technology',
    overview: {
      title: 'Service Overview',
      highAccuracy: {
        title: 'High-Precision AI Analysis',
        description: 'Using state-of-the-art Convolutional Neural Networks (CNN), we achieve 99.2% accuracy for image classification across 1000+ categories.'
      },
      realtime: {
        title: 'Real-time Processing',
        description: 'Optimized model architecture enables high-speed processing averaging under 500ms, allowing for real-time image classification.'
      },
      formats: {
        title: 'Multiple Format Support',
        description: 'Supports major image formats including JPEG, PNG, WebP, BMP, and can process files up to 10MB in size.'
      },
      batch: {
        title: 'Batch Processing Support',
        description: 'Supports bulk processing of multiple images for efficient analysis of large image sets. Real-time progress tracking available with progress bars.'
      }
    },
    techStack: {
      title: 'Tech Stack',
      frontend: 'Frontend',
      backend: 'Backend',
      vue: 'Modern reactive framework',
      typescript: 'Type-safe development environment',
      tailwind: 'Utility-first CSS framework',
      pinia: 'State management library',
      fastapi: 'High-performance Web API framework',
      python: 'Programming language for machine learning',
      tensorflow: 'Deep learning framework',
      docker: 'Containerization technology'
    },
    performance: {
      title: 'Performance Metrics',
      accuracy: 'Classification Accuracy',
      processingTime: 'Processing Time',
      supportedClasses: 'Supported Classes',
      maxFileSize: 'Max File Size',
      accuracyNote: 'Top-1 Accuracy',
      timeNote: 'Average Response Time',
      classesNote: 'ImageNet Compatible',
      fileSizeNote: 'High Resolution Support'
    },
    contact: {
      title: 'Contact',
      description: 'If you have questions, feedback, or feature requests, please feel free to contact us.',
      email: 'Contact via Email',
      github: 'Report on GitHub'
    }
  },

  models: {
    list: {
      title: 'Custom Models',
      description: 'Manage your uploaded custom models',
      upload: 'Upload Model',
      empty: {
        title: 'No custom models',
        description: 'Upload a custom model to start using your own image classification'
      },
      loading: 'Loading models...',
      error: {
        title: 'Failed to load models'
      },
      retry: 'Retry',
      classes: 'Classes',
      uploadedOn: 'Uploaded on',
      validate: 'Validate',
      delete: 'Delete',
      validationError: 'Validation Error',
      validation: {
        success: {
          title: 'Validation Successful',
          message: 'Model validation completed successfully'
        },
        error: {
          title: 'Validation Failed',
          message: 'Model validation failed'
        }
      },
      delete: {
        confirm: 'Are you sure you want to delete model "{name}"?',
        success: {
          title: 'Deletion Complete',
          message: 'Model "{name}" has been deleted'
        },
        error: {
          title: 'Deletion Failed',
          message: 'Failed to delete model'
        }
      }
    },
    upload: {
      title: 'Upload Custom Model',
      description: 'Upload TensorFlow or PyTorch models for custom classification',
      form: {
        name: 'Model Name',
        namePlaceholder: 'Enter a descriptive model name',
        description: 'Description (Optional)',
        descriptionPlaceholder: 'Enter model purpose and features',
        type: 'Model Type',
        selectType: 'Select model type',
        classes: 'Class Names',
        classPlaceholder: 'Class {index} name',
        addClass: 'Add Class',
        file: 'Model File',
        dropFile: 'Drop model file here',
        fileFormats: 'Supported formats: .h5, .hdf5, .pth, .pt',
        selectFile: 'Select File',
        upload: 'Upload',
        uploading: 'Uploading...',
        reset: 'Reset'
      },
      progress: {
        uploading: 'Uploading model',
        description: 'Please wait...'
      },
      success: {
        title: 'Upload Successful',
        message: 'Model "{name}" uploaded successfully'
      },
      error: {
        title: 'Upload Failed',
        message: 'Failed to upload model'
      }
    },
    status: {
      uploaded: 'Uploaded',
      active: 'Active',
      error: 'Error',
      validating: 'Validating'
    }
  }
}