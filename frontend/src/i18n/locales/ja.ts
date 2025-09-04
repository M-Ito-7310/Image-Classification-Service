export default {
  common: {
    appName: 'AI画像分類サービス',
    loading: '読み込み中...',
    error: 'エラー',
    success: '成功',
    warning: '警告',
    cancel: 'キャンセル',
    confirm: '確認',
    delete: '削除',
    edit: '編集',
    save: '保存',
    close: '閉じる',
    search: '検索',
    filter: 'フィルター',
    export: 'エクスポート',
    import: 'インポート',
    download: 'ダウンロード',
    upload: 'アップロード',
    processing: '処理中...',
    noData: 'データがありません',
    selectAll: 'すべて選択',
    clearAll: 'すべてクリア',
    actions: 'アクション',
    view: '表示',
    refresh: '更新',
    back: '戻る',
    next: '次へ',
    previous: '前へ',
    yes: 'はい',
    no: 'いいえ'
  },
  
  nav: {
    home: 'ホーム',
    classify: '画像分類',
    history: '履歴',
    settings: '設定',
    about: 'このアプリについて',
    dashboard: 'ダッシュボード',
    profile: 'プロフィール',
    login: 'ログイン',
    register: '新規登録',
    logout: 'ログアウト'
  },

  home: {
    title: 'AI画像分類',
    subtitle: 'サービス',
    description: '最新のAI技術を使用して、画像を高精度で自動分類。ドラッグ&ドロップで簡単アップロード、リアルタイム解析、詳細な結果表示を提供します。',
    startClassifying: '画像分類を開始',
    stats: {
      accuracy: '分類精度',
      speed: '処理時間',
      maxSize: '最大ファイルサイズ',
      aiAnalysis: 'AI分析',
      multipleFormats: '複数形式',
      speedValue: '<3秒',
      maxSizeValue: '10MB'
    },
    features: {
      upload: {
        title: '簡単アップロード',
        description: 'ドラッグ&ドロップまたはクリックで画像を簡単にアップロード。'
      },
      analysis: {
        title: '高精度AI分析',
        description: '最新の深層学習モデルによる高精度な画像分類。信頼度スコア付きで結果の品質を確認。'
      },
      results: {
        title: '詳細な結果表示',
        description: '分類結果を見やすく表示。信頼度グラフ、処理時間、メタデータなど詳細情報も確認可能。'
      },
      formats: {
        title: '多様な形式に対応',
        description: 'JPEG、PNG、WebP、BMPなど主要な画像形式をサポート。最大10MBまでのファイルに対応。'
      },
      realtime: {
        title: 'リアルタイム処理',
        description: '高速な処理でリアルタイムに結果を表示。プログレスバーで処理状況をリアルタイム確認。'
      },
      export: {
        title: '結果エクスポート',
        description: '分類結果をJSONやCSV形式でエクスポート。データ分析やレポート作成に活用可能。'
      },
      collaboration: {
        title: 'エンタープライズコラボレーション',
        description: 'チームワークスペース、プロジェクト共有、エンタープライズワークフロー向け共同モデル開発。'
      },
      marketplace: {
        title: 'APIマーケットプレイス',
        description: '包括的なマーケットプレイスプラットフォームを通じてAIモデルを発見・収益化。'
      },
      authentication: {
        title: 'ユーザー認証',
        description: 'JWT認証によるセキュアなログイン。個人設定と分類履歴の管理機能付き。'
      },
      modelManagement: {
        title: 'モデル管理',
        description: 'カスタムAIモデルのアップロード、検証、管理。TensorFlowとPyTorch形式に対応。'
      },
      history: {
        title: '履歴追跡',
        description: '分類結果の保存と履歴管理。過去の分析結果を検索・エクスポート可能。'
      }
    },
    howTo: {
      title: '使い方',
      step1: {
        title: '画像分類ページへ移動',
        description: '「画像分類を開始」ボタンをクリックして専用ページへ移動'
      },
      step2: {
        title: '画像をアップロード',
        description: 'ドラッグ&ドロップまたはクリックで画像をアップロードし、分類オプションを設定'
      },
      step3: {
        title: 'AI分析結果を確認',
        description: '高精度なAI分析結果を確認し、必要に応じて結果をエクスポート'
      }
    },
    specs: {
      title: '技術仕様',
      formats: '対応形式',
      maxSize: '最大ファイルサイズ',
      processing: '処理方式',
      speed: '処理速度',
      formatsValue: 'JPEG, PNG, WebP, BMP',
      maxSizeValue: '10MB',
      processingValue: '単一画像処理',
      speedValue: '平均3秒以内'
    }
  },
  
  auth: {
    appName: 'AI画像分類サービス', 
    footer: {
      aboutService: 'このサービスについて',
      backToHome: 'ホームに戻る',
      copyright: '© 2024 AI Image Classifier. All rights reserved.'
    },
    login: {
      title: 'ログイン',
      subtitle: 'アカウントにサインインしてください',
      username: 'ユーザー名またはメールアドレス',
      usernamePlaceholder: 'ユーザー名またはメールアドレスを入力',
      password: 'パスワード',
      passwordPlaceholder: 'パスワードを入力',
      rememberMe: 'ログイン状態を保持',
      forgotPassword: 'パスワードを忘れた方',
      submit: 'ログイン',
      submitting: 'ログイン中...',
      noAccount: 'アカウントをお持ちでないですか？',
      signUp: '新規登録',
      success: 'ログインに成功しました',
      error: 'ログインに失敗しました',
      validation: {
        usernameRequired: 'ユーザー名またはメールアドレスは必須です',
        passwordRequired: 'パスワードは必須です',
        passwordMinLength: 'パスワードは8文字以上である必要があります'
      },
      demo: {
        title: 'デモアカウント',
        description: 'すぐにお試しいただけるデモアカウントをご用意しています',
        regularUser: '一般ユーザー',
        adminUser: '管理者ユーザー',
        quickLogin: 'クイックログイン',
        note: '※デモ用途のため、実際のデータは含まれていません'
      }
    },
    register: {
      title: '新規登録',
      subtitle: '新しいアカウントを作成しましょう',
      username: 'ユーザー名',
      usernamePlaceholder: 'ユーザー名を入力（3-50文字）',
      email: 'メールアドレス',
      emailPlaceholder: 'メールアドレスを入力',
      password: 'パスワード',
      passwordPlaceholder: 'パスワードを入力（8-100文字）',
      confirmPassword: 'パスワード確認',
      confirmPasswordPlaceholder: 'パスワードを再入力',
      fullName: 'フルネーム（任意）',
      fullNamePlaceholder: 'フルネームを入力（100文字以内）',
      agreeTerms: '利用規約に同意します',
      submit: 'アカウント作成',
      submitting: '登録中...',
      haveAccount: 'すでにアカウントをお持ちですか？',
      signIn: 'ログイン',
      success: '登録に成功しました',
      error: '登録に失敗しました',
      required: '必須',
      passwordStrength: {
        weak: '弱い',
        medium: '普通',
        strong: '強い'
      },
      validation: {
        usernameRequired: 'ユーザー名は必須です',
        usernameMinLength: 'ユーザー名は3文字以上である必要があります',
        usernameMaxLength: 'ユーザー名は50文字以内である必要があります',
        usernameInvalid: 'ユーザー名は英数字、アンダースコア、ハイフンのみ使用できます',
        emailRequired: 'メールアドレスは必須です',
        emailInvalid: '有効なメールアドレスを入力してください',
        fullNameMaxLength: 'フルネームは100文字以内である必要があります',
        passwordRequired: 'パスワードは必須です',
        passwordMinLength: 'パスワードは8文字以上である必要があります',
        passwordMaxLength: 'パスワードは100文字以内である必要があります',
        confirmPasswordRequired: 'パスワード確認は必須です',
        confirmPasswordMismatch: 'パスワードが一致しません'
      }
    },
    logout: {
      message: 'ログアウトしました',
      confirm: 'ログアウトしてもよろしいですか？'
    },
    errors: {
      invalidCredentials: 'ユーザー名またはパスワードが正しくありません',
      userExists: 'このユーザー名は既に使用されています',
      emailExists: 'このメールアドレスは既に登録されています',
      passwordMismatch: 'パスワードが一致しません',
      weakPassword: 'パスワードは8文字以上である必要があります',
      required: 'このフィールドは必須です'
    }
  },
  
  classification: {
    title: '画像分類',
    subtitle: '画像をアップロードしてAIによる自動分類を実行します',
    emptyState: {
      title: '画像を選択してください',
      description: '上のエリアに画像をドラッグ&ドロップするか、クリックしてファイルを選択してください',
      supportedFormats: '対応形式: JPEG, PNG, WebP, BMP • 最大10MB'
    },
    results: {
      highestConfidence: '最高信頼度',
      averageConfidence: '平均信頼度',
      highConfidence: '高信頼度',
      predictions: '個の予測',
      predictionsCount: '{count}個の予測',
      showMore: 'あと{count}個を表示',
      showLess: '{count}個を非表示',
      viewDetails: '詳細を表示',
      size: 'サイズ',
      format: '形式',
      threshold: '閾値',
      download: 'ダウンロード',
      downloadCompleted: 'ダウンロード完了',
      downloadMessage: '分類結果をダウンロードしました',
      downloadError: 'ダウンロードエラー',
      downloadErrorMessage: 'ファイルのダウンロードに失敗しました',
      imagesAnalyzed: '{count}個の画像を分析',
      totalPredictions: '{count}個の予測',
      title: '分類結果',
      highConfidenceResults: '高信頼度結果',
      imageInfo: '画像情報',
      filename: 'ファイル名',
      classificationResults: '分類結果',
      sortByConfidence: '信頼度順',
      sortByName: 'クラス名順',
      confidenceDistribution: '信頼度分布',
      confidenceLevel: {
        veryHigh: '非常に高い',
        high: '高い',
        medium: '中程度',
        low: '低い',
        veryLow: '非常に低い'
      },
      clearResults: '結果をクリア',
      resultsCleared: '分類結果をクリアしました',
      format: '形式',
      resolution: '解像度',
      modelUsed: '使用モデル',
      exportJson: 'JSON形式でエクスポート',
      exportCsv: 'CSV形式でエクスポート',
      exportCompleted: 'エクスポート完了',
      exportedFormat: '{format}形式でエクスポートしました',
      processingTime: '処理時間',
      averageProcessingTime: '平均処理時間',
      detectedClasses: '検出クラス数',
      export: 'エクスポート'
    },
    upload: {
      title: '画像をアップロード',
      description: 'ここに画像をドラッグ＆ドロップまたはクリックして選択',
      button: 'ファイルを選択',
      dragActive: 'ここにドロップ',
      formats: '対応形式: JPEG, PNG, WebP, BMP',
      maxSize: '最大ファイルサイズ: 10MB',
      processing: '画像を処理中...',
      error: 'アップロードエラー',
      uploading: 'アップロード中... {progress}%',
      startUpload: 'アップロード開始',
      enhanceImages: '画像を前処理で強化する',
      duplicatesSkipped: '{count}個の重複ファイルがスキップされました',
      analyzingImages: '{count}個の画像を分析中...',
      options: '分類オプション',
      selectedFiles: '選択されたファイル',
      selectedFile: '選択されたファイル',
      removeAll: '全て削除',
      totalSize: '総サイズ',
      model: '使用モデル',
      maxResults: '最大結果数',
      confidenceThreshold: '信頼度閾値',
      enableResize: 'リサイズを有効化',
      supportedFormats: '対応形式: JPEG, PNG, WebP, BMP',
      supportedFormatsWithSize: '対応形式: JPEG, PNG, WebP, BMP • 最大10MB/ファイル',
      supportedFormatsOptimized: '対応形式: JPEG, PNG, WebP, BMP • 最適化により高速処理',
      unsupportedFilesError: '{count}個のファイルは対応していない形式または大きすぎるため追加されませんでした',
      modelLabel: '使用モデル'
    },
    models: {
      select: 'モデルを選択',
      default: 'デフォルト',
      custom: 'カスタム',
      performance: 'パフォーマンス',
      accuracy: '精度'
    },
    status: {
      uploaded: 'アップロード済み',
      active: 'アクティブ',
      error: 'エラー',
      validating: '検証中'
    },
    guide: {
      title: '使い方ガイド',
      howToUse: '使い方を見る',
      steps: {
        upload: {
          title: '画像のアップロード',
          description: '画像ファイルをアップロードして分析を開始します',
          method1: 'ドラッグ&ドロップ：画像ファイルをアップロードエリアにドラッグしてドロップ',
          method2: 'クリック選択：「ファイルを選択」ボタンをクリックしてファイルブラウザから選択',
        },
        options: {
          title: '分類オプションの設定',
          description: 'AI分析の精度と結果を最適化するためのオプションを設定します',
          model: 'AIモデル選択',
          modelDesc: '用途に応じてデフォルトモデルまたはカスタムモデルを選択',
          confidence: '信頼度閾値',
          confidenceDesc: '結果として表示する最小の信頼度レベルを設定（推奨：0.1-0.9）',
          maxResults: '最大結果数',
          maxResultsDesc: '表示する分類結果の最大数を設定（1-20の範囲）',
          preprocessing: '前処理オプション',
          preprocessingDesc: '画像の品質向上のための自動前処理を有効化'
        },
        results: {
          title: '分析結果の確認',
          description: 'AIによる画像分析結果を詳細に確認できます',
          confidence: '信頼度スコア',
          confidenceDesc: '各分類結果の確信度をパーセンテージで表示（高いほど正確）',
          ranking: 'ランキング表示',
          rankingDesc: '信頼度順に結果をランキング形式で表示、上位が最も可能性の高い分類',
          metadata: 'メタデータ情報',
          metadataDesc: '処理時間、使用モデル、ファイル情報などの詳細データを表示'
        },
        export: {
          title: '結果のエクスポート',
          description: '分析結果を様々な形式でエクスポートして活用できます',
          jsonDesc: '構造化データとして結果をエクスポート、プログラムでの処理に最適',
          csvDesc: 'スプレッドシート形式でエクスポート、表計算ソフトでの分析に便利',
          reportTitle: '詳細レポート',
          reportDesc: '画像と結果を含む包括的なレポートを生成、プレゼンテーション用途に最適'
        }
      },
      navigation: {
        previous: '前へ',
        next: '次へ',
        done: '完了'
      }
    }
  },
  
  history: {
    title: '分類履歴',
    subtitle: 'これまでの画像分類結果を確認できます',
    empty: '履歴がありません',
    emptySubtitle: '画像を分類すると、ここに履歴が表示されます',
    classifyNow: '画像を分類する',
    searchPlaceholder: 'ファイル名で検索...',
    clearHistory: '履歴をクリア',
    stats: {
      totalClassifications: '総分類数',
      totalPredictions: '総予測数',
      averageProcessingTime: '平均処理時間',
      uniqueModels: '使用モデル数'
    },
    results: {
      title: '分類結果',
      count: '{count}個'
    },
    messages: {
      downloadComplete: 'ダウンロード完了',
      downloadSuccess: '履歴項目をダウンロードしました',
      clearConfirm: 'すべての履歴を削除しますか？この操作は取り消せません。',
      historyCleared: '履歴をクリア',
      allHistoryDeleted: 'すべての履歴を削除しました'
    },
    filters: {
      all: 'すべて',
      today: '今日',
      week: '今週',
      month: '今月',
      model: 'モデル',
      dateRange: '期間'
    },
    table: {
      image: '画像',
      result: '結果',
      confidence: '信頼度',
      model: 'モデル',
      date: '日時',
      actions: 'アクション'
    },
    actions: {
      view: '詳細を見る',
      delete: '削除',
      download: 'ダウンロード',
      reprocess: '再処理',
      details: '詳細'
    },
    confirm: {
      delete: 'この記録を削除してもよろしいですか？',
      deleteAll: 'すべての履歴を削除してもよろしいですか？',
      export: '履歴をエクスポートしますか？'
    }
  },
  
  dashboard: {
    title: 'ダッシュボード',
    welcome: 'ようこそ、{name}さん',
    stats: {
      totalImages: '分類済み画像',
      monthlyImages: '今月の分類',
      accuracy: '平均精度',
      processingTime: '平均処理時間'
    },
    recentActivity: {
      title: '最近の分類結果',
      empty: 'まだ分類結果がありません',
      viewAll: 'すべて見る'
    },
    quickActions: {
      title: 'クイックアクション',
      classify: '画像を分類する',
      viewHistory: '分類履歴を見る',
      settings: '設定',
      profile: 'プロフィール編集'
    },
    accountInfo: {
      title: 'アカウント情報',
      registeredDate: '登録日',
      lastLogin: '最終ログイン',
      plan: 'プラン',
      usage: '使用量'
    }
  },
  
  profile: {
    title: 'プロフィール',
    subtitle: 'アカウント情報の確認・変更',
    personalInfo: {
      title: '基本情報',
      username: 'ユーザー名',
      email: 'メールアドレス',
      fullName: 'フルネーム',
      fullNameOptional: 'フルネーム（任意）',
      fullNamePlaceholder: 'フルネームを入力',
      accountType: 'アカウント種別',
      registeredDate: '登録日',
      lastLogin: '最終ログイン',
      notSet: '未設定',
      admin: '管理者',
      regularUser: '一般ユーザー',
      bio: '自己紹介',
      avatar: 'アバター'
    },
    security: {
      title: 'パスワード変更',
      changePassword: 'パスワードを変更',
      currentPassword: '現在のパスワード',
      newPassword: '新しいパスワード',
      confirmPassword: 'パスワード（確認）',
      twoFactor: '二要素認証',
      sessions: 'アクティブセッション',
      sessionsLoading: 'セッション情報を読み込んでいます...',
      unknownDevice: '不明なデバイス',
      terminateSession: '終了'
    },
    preferences: {
      title: '設定',
      language: '言語',
      theme: 'テーマ',
      notifications: '通知',
      privacy: 'プライバシー'
    },
    actions: {
      edit: '編集',
      save: '保存',
      saving: '保存中...',
      change: '変更',
      changing: '変更中...',
      cancel: 'キャンセル',
      deleteAccount: 'アカウント削除',
      exportData: 'データエクスポート'
    },
    messages: {
      profileUpdated: 'プロフィールが正常に更新されました',
      profileUpdateFailed: 'プロフィールの更新に失敗しました',
      passwordChanged: 'パスワードが正常に変更されました',
      passwordChangeFailed: 'パスワードの変更に失敗しました',
      sessionTerminated: 'セッションが終了されました',
      sessionTerminateFailed: 'セッションの終了に失敗しました'
    },
    validation: {
      emailRequired: 'メールアドレスは必須です',
      emailInvalid: '有効なメールアドレスを入力してください',
      fullNameMaxLength: 'フルネームは100文字以内である必要があります'
    }
  },
  
  settings: {
    title: '設定',
    subtitle: 'アプリケーションの動作をカスタマイズできます',
    general: {
      title: '一般',
      language: '言語',
      dateFormat: '日付形式',
      timezone: 'タイムゾーン'
    },
    appearance: {
      title: '外観',
      theme: 'テーマ',
      darkMode: 'ダークモード',
      colorScheme: 'カラースキーム',
      fontSize: 'フォントサイズ',
      animations: 'アニメーション',
      themes: {
        light: 'ライト',
        dark: 'ダーク'
      }
    },
    classification: {
      title: '分類設定',
      defaultModel: 'デフォルトモデル',
      defaultThreshold: 'デフォルト信頼度闾値',
      defaultMaxResults: 'デフォルト最大結果数',
      enableImageEnhancement: '画像前処理を有効にする',
      enhancementDescription: 'アップロード時に画像の品質を自動的に向上させます',
      options: {
        default: 'デフォルト'
      }
    },
    ui: {
      title: 'ユーザーインターフェース',
      showAdvancedOptions: '高度なオプションを表示',
      advancedDescription: 'より詳細な設定オプションを表示します',
      showProcessingDetails: '処理詳細を表示',
      processingDescription: '処理時間やメタデータなどの詳細情報を表示します',
      enableNotifications: '通知を有効にする',
      notificationsDescription: '処理完了時やエラー発生時に通知を表示します'
    },
    history: {
      title: '履歴設定',
      saveHistory: '分類履歴を保存',
      saveDescription: '分類結果を履歴として保存し、後で確認できるようにします',
      maxHistoryItems: '最大履歴保存数',
      unlimitedNote: '0を指定すると無制限に保存されます'
    },
    dataManagement: {
      title: 'データ管理',
      autoSave: '自動保存',
      autoSaveDescription: '設定変更を自動的に保存します',
      exportSettings: '設定をエクスポート',
      importSettings: '設定をインポート'
    },
    reset: {
      title: 'リセット',
      description: 'すべての設定をデフォルト値に戻します。この操作は取り消せません。',
      confirm: 'すべての設定をデフォルト値に戻しますか？この操作は取り消せません。',
      button: 'すべての設定をリセット'
    },
    messages: {
      importComplete: 'インポート完了',
      importSuccess: '設定をインポートしました',
      importFailed: '設定のインポートに失敗しました',
      resetComplete: '設定をリセット',
      resetSuccess: 'すべての設定をデフォルト値に戻しました'
    },
    notifications: {
      title: '通知',
      email: 'メール通知',
      browser: 'ブラウザ通知',
      sound: 'サウンド',
      frequency: '頻度'
    },
    api: {
      title: 'API設定',
      key: 'APIキー',
      endpoint: 'エンドポイント',
      timeout: 'タイムアウト',
      retries: 'リトライ回数'
    },
    advanced: {
      title: '詳細設定',
      cache: 'キャッシュ',
      debug: 'デバッグモード',
      logs: 'ログ',
      reset: '設定をリセット'
    }
  },
  
  errors: {
    general: 'エラーが発生しました',
    network: 'ネットワークエラー',
    server: 'サーバーエラー',
    notFound: 'ページが見つかりません',
    forbidden: 'アクセスが拒否されました',
    unauthorized: '認証が必要です',
    validation: '入力内容を確認してください',
    fileSize: 'ファイルサイズが大きすぎます',
    fileType: '対応していないファイル形式です',
    upload: 'アップロードに失敗しました',
    processing: '処理に失敗しました'
  },
  
  messages: {
    success: {
      saved: '保存しました',
      deleted: '削除しました',
      updated: '更新しました',
      uploaded: 'アップロードしました',
      exported: 'エクスポートしました'
    },
    info: {
      loading: '読み込み中...',
      processing: '処理中...',
      saving: '保存中...',
      uploading: 'アップロード中...'
    },
    warning: {
      unsaved: '保存されていない変更があります',
      confirmDelete: '削除してもよろしいですか？',
      confirmLogout: 'ログアウトしてもよろしいですか？'
    }
  },
  
  footer: {
    copyright: '© 2025 AI画像分類サービス',
    allRightsReserved: 'All rights reserved.',
    privacy: 'プライバシーポリシー',
    terms: '利用規約',
    contact: 'お問い合わせ',
    about: '概要',
    description: '最先端のAI技術を活用した画像分類サービス。TensorFlow、PyTorch、Google Cloud Vision APIに対応し、高精度な画像認識を提供します。',
    quickLinks: 'クイックリンク',
    techStack: '技術スタック',
    apiDocs: 'APIドキュメント',
    developmentPhase: 'Phase 3 開発中',
    subtitle: '認識サービス'
  },

  about: {
    title: 'AI画像分類サービス',
    subtitle: '最新の深層学習技術を活用した高精度画像分類システム',
    overview: {
      title: 'サービス概要',
      highAccuracy: {
        title: '高精度AI分析',
        description: '最新の畳み込みニューラルネットワーク（CNN）を使用し、1000を超えるカテゴリでの画像分類を99.2%の精度で実現しています。'
      },
      realtime: {
        title: 'リアルタイム処理',
        description: '最適化されたモデルアーキテクチャにより、平均500ms以下での高速処理を実現し、リアルタイムでの画像分類が可能です。'
      },
      formats: {
        title: '多様な対応形式',
        description: 'JPEG、PNG、WebP、BMPなど主要な画像形式に対応し、最大10MBまでのファイルを処理できます。'
      },
      enterprise: {
        title: 'エンタープライズ機能',
        description: '包括的なコラボレーションツール、APIマーケットプレイス、課金統合、エンタープライズデプロイメント向け高度なモニタリング。'
      },
      multimodal: {
        title: 'マルチモーダル処理',
        description: '包括的なメディア分析のためのリアルタイムストリーミングサポート付き高度な動画・音声分類機能。'
      }
    },
    techStack: {
      title: '技術スタック',
      frontend: 'フロントエンド',
      backend: 'バックエンド',
      vue: 'モダンなリアクティブフレームワーク',
      typescript: '型安全な開発環境',
      tailwind: 'ユーティリティファーストCSS',
      pinia: '状態管理ライブラリ',
      fastapi: '高性能WebAPIフレームワーク',
      python: '機械学習向けプログラミング言語',
      tensorflow: '深層学習フレームワーク',
      postgresql: 'リレーショナルデータベース',
      docker: 'コンテナ化技術'
    },
    performance: {
      title: 'パフォーマンス指標',
      accuracy: '分類精度',
      processingTime: '処理時間',
      supportedFormats: '対応形式',
      maxFileSize: '最大ファイルサイズ',
      accuracyNote: 'Top-1 Accuracy',
      timeNote: '平均応答時間',
      classesNote: 'ImageNet準拠',
      fileSizeNote: '高解像度対応'
    },
    contact: {
      title: 'お問い合わせ',
      description: 'ご質問、フィードバック、機能要求などがございましたら、お気軽にお問い合わせください。',
      email: 'メールでお問い合わせ',
      github: 'GitHubで報告'
    }
  },

  models: {
    list: {
      title: 'カスタムモデル',
      description: 'アップロードしたカスタムモデルを管理できます',
      upload: 'モデルをアップロード',
      empty: {
        title: 'カスタムモデルがありません',
        description: 'カスタムモデルをアップロードして、独自の画像分類を開始しましょう'
      },
      loading: 'モデルを読み込み中...',
      error: {
        title: 'モデルの読み込みに失敗しました'
      },
      retry: '再試行',
      classes: 'クラス',
      uploadedOn: 'アップロード日',
      validate: '検証',
      delete: '削除',
      validationError: '検証エラー',
      validation: {
        success: {
          title: '検証成功',
          message: 'モデルの検証が完了しました'
        },
        error: {
          title: '検証失敗',
          message: 'モデルの検証に失敗しました'
        }
      },
      deleteModel: {
        confirm: 'モデル「{name}」を削除してもよろしいですか？',
        success: {
          title: '削除完了',
          message: 'モデル「{name}」を削除しました'
        },
        error: {
          title: '削除失敗',
          message: 'モデルの削除に失敗しました'
        }
      }
    },
    upload: {
      title: 'カスタムモデルアップロード',
      description: 'TensorFlowまたはPyTorchモデルをアップロードして使用できます',
      form: {
        name: 'モデル名',
        namePlaceholder: 'わかりやすいモデル名を入力',
        description: '説明（任意）',
        descriptionPlaceholder: 'モデルの用途や特徴を入力',
        type: 'モデルタイプ',
        selectType: 'モデルタイプを選択',
        classes: 'クラス名',
        classPlaceholder: 'クラス {index} の名前',
        addClass: 'クラスを追加',
        file: 'モデルファイル',
        dropFile: 'モデルファイルをここにドロップしてください',
        fileFormats: '対応形式: .h5, .hdf5, .pth, .pt',
        selectFile: 'ファイルを選択',
        upload: 'アップロード',
        uploading: 'アップロード中...',
        reset: 'リセット'
      },
      progress: {
        uploading: 'モデルをアップロード中',
        description: 'しばらくお待ちください...'
      },
      success: {
        title: 'アップロード成功',
        message: 'モデル「{name}」のアップロードが完了しました'
      },
      error: {
        title: 'アップロード失敗',
        message: 'モデルのアップロードに失敗しました'
      }
    },
    status: {
      uploaded: 'アップロード済み',
      active: 'アクティブ',
      error: 'エラー',
      validating: '検証中'
    }
  },

  // ImageNet class labels translations
  imagenet: {
    // Common objects and scenes
    web_site: 'ウェブサイト',
    envelope: '封筒',
    menu: 'メニュー',
    notebook: 'ノート',
    book_jacket: 'ブックカバー',
    magazine: '雑誌',
    computer_keyboard: 'コンピューターキーボード',
    computer_mouse: 'コンピューターマウス',
    laptop: 'ノートパソコン',
    desktop_computer: 'デスクトップパソコン',
    cellular_telephone: '携帯電話',
    remote_control: 'リモコン',
    
    // Animals
    tabby_cat: 'トラ猫',
    Egyptian_cat: 'エジプト猫',
    Persian_cat: 'ペルシャ猫',
    golden_retriever: 'ゴールデンレトリバー',
    Labrador_retriever: 'ラブラドールレトリバー',
    beagle: 'ビーグル',
    German_shepherd: 'ジャーマンシェパード',
    robin: 'コマドリ',
    jay: 'カケス',
    magpie: 'カササギ',
    tiger: '虎',
    lion: 'ライオン',
    leopard: 'ヒョウ',
    elephant: '象',
    
    // Vehicles
    sports_car: 'スポーツカー',
    convertible: 'コンバーチブル',
    limousine: 'リムジン',
    pickup_truck: 'ピックアップトラック',
    fire_engine: '消防車',
    garbage_truck: 'ゴミ収集車',
    airliner: '旅客機',
    warplane: '軍用機',
    space_shuttle: 'スペースシャトル',
    ambulance: '救急車',
    police_van: 'パトカー',
    
    // Food
    pizza: 'ピザ',
    cheeseburger: 'チーズバーガー',
    hot_dog: 'ホットドッグ',
    ice_cream: 'アイスクリーム',
    chocolate_sauce: 'チョコレートソース',
    pretzel: 'プレッツェル',
    bagel: 'ベーグル',
    croissant: 'クロワッサン',
    dough: '生地',
    
    // Household items
    coffee_mug: 'コーヒーマグ',
    wine_bottle: 'ワインボトル',
    beer_bottle: 'ビール瓶',
    water_bottle: '水筒',
    mixing_bowl: 'ボウル',
    frying_pan: 'フライパン',
    wok: '中華鍋',
    spatula: 'ヘラ',
    
    // Clothing
    jersey: 'ジャージ',
    T_shirt: 'Tシャツ',
    jeans: 'ジーンズ',
    suit: 'スーツ',
    bow_tie: '蝶ネクタイ',
    necktie: 'ネクタイ',
    miniskirt: 'ミニスカート',
    bikini: 'ビキニ',
    
    // Fruits and Food
    granny_smith: 'グラニースミスりんご',
    pomegranate: 'ザクロ',
    orange: 'オレンジ',
    candle: 'ろうそく',
    croquet_ball: 'クロケットボール',
    
    // Animals - Cats
    tabby: 'タビー猫',
    egyptian_cat: 'エジプト猫',
    tiger_cat: 'トラ猫',
    persian_cat: 'ペルシャ猫',
    siamese_cat: 'シャム猫',
    
    // Animals - Dogs
    golden_retriever: 'ゴールデンレトリバー',
    labrador_retriever: 'ラブラドールレトリバー',
    german_shepherd: 'ジャーマンシェパード',
    beagle: 'ビーグル',
    chihuahua: 'チワワ',
    pug: 'パグ',
    bulldog: 'ブルドッグ',
    poodle: 'プードル',
    husky: 'ハスキー',
    dalmatian: 'ダルメシアン',
    
    // Animals - Wild Animals
    lion: 'ライオン',
    tiger: 'トラ',
    elephant: 'ゾウ',
    bear: 'クマ',
    wolf: 'オオカミ',
    fox: 'キツネ',
    zebra: 'シマウマ',
    giraffe: 'キリン',
    monkey: 'サル',
    gorilla: 'ゴリラ',
    chimpanzee: 'チンパンジー',
    panda: 'パンダ',
    koala: 'コアラ',
    kangaroo: 'カンガルー',
    deer: 'シカ',
    rabbit: 'ウサギ',
    squirrel: 'リス',
    
    // Animals - Birds
    eagle: 'ワシ',
    owl: 'フクロウ',
    parrot: 'オウム',
    swan: 'ハクチョウ',
    duck: 'アヒル',
    chicken: '鶏',
    rooster: '雄鶏',
    turkey: '七面鳥',
    peacock: 'クジャク',
    flamingo: 'フラミンゴ',
    penguin: 'ペンギン',
    ostrich: 'ダチョウ',
    
    // Animals - Sea Life
    shark: 'サメ',
    whale: 'クジラ',
    dolphin: 'イルカ',
    octopus: 'タコ',
    jellyfish: 'クラゲ',
    starfish: 'ヒトデ',
    crab: 'カニ',
    lobster: 'ロブスター',
    turtle: 'カメ',
    
    // Animals - Insects
    butterfly: 'チョウ',
    bee: 'ハチ',
    ant: 'アリ',
    spider: 'クモ',
    dragonfly: 'トンボ',
    ladybug: 'テントウムシ',
    
    // Fruits
    apple: 'リンゴ',
    banana: 'バナナ',
    strawberry: 'イチゴ',
    lemon: 'レモン',
    pineapple: 'パイナップル',
    watermelon: 'スイカ',
    grape: 'ブドウ',
    peach: '桃',
    cherry: 'サクランボ',
    fig: 'イチジク',
    
    // Vegetables
    broccoli: 'ブロッコリー',
    carrot: 'ニンジン',
    cucumber: 'キュウリ',
    tomato: 'トマト',
    potato: 'ジャガイモ',
    onion: 'タマネギ',
    cabbage: 'キャベツ',
    lettuce: 'レタス',
    corn: 'トウモロコシ',
    mushroom: 'キノコ',
    
    // Food
    pizza: 'ピザ',
    hamburger: 'ハンバーガー',
    hotdog: 'ホットドッグ',
    sandwich: 'サンドイッチ',
    bread: 'パン',
    cake: 'ケーキ',
    cookie: 'クッキー',
    ice_cream: 'アイスクリーム',
    chocolate: 'チョコレート',
    
    // Vehicles
    car: '車',
    truck: 'トラック',
    bus: 'バス',
    motorcycle: 'バイク',
    bicycle: '自転車',
    airplane: '飛行機',
    helicopter: 'ヘリコプター',
    boat: 'ボート',
    ship: '船',
    train: '電車',
    submarine: '潜水艦',
    
    // Household Items
    chair: '椅子',
    table: 'テーブル',
    bed: 'ベッド',
    sofa: 'ソファ',
    television: 'テレビ',
    computer: 'コンピュータ',
    phone: '電話',
    clock: '時計',
    lamp: 'ランプ',
    mirror: '鏡',
    refrigerator: '冷蔵庫',
    microwave: '電子レンジ',
    toaster: 'トースター',
    vacuum: '掃除機',
    
    // Tools and Objects
    hammer: 'ハンマー',
    screwdriver: 'ドライバー',
    scissors: 'ハサミ',
    knife: 'ナイフ',
    spoon: 'スプーン',
    fork: 'フォーク',
    plate: '皿',
    cup: 'カップ',
    bottle: 'ボトル',
    glass: 'グラス',
    key: '鍵',
    lock: '錠',
    
    // Clothing
    shirt: 'シャツ',
    pants: 'ズボン',
    dress: 'ドレス',
    jacket: 'ジャケット',
    coat: 'コート',
    hat: '帽子',
    shoes: '靴',
    socks: '靴下',
    gloves: '手袋',
    tie: 'ネクタイ',
    belt: 'ベルト',
    
    // Sports
    football: 'アメリカンフットボール',
    basketball: 'バスケットボール',
    baseball: '野球',
    tennis: 'テニス',
    soccer: 'サッカー',
    golf: 'ゴルフ',
    volleyball: 'バレーボール',
    
    // Musical Instruments
    piano: 'ピアノ',
    guitar: 'ギター',
    violin: 'バイオリン',
    drum: 'ドラム',
    trumpet: 'トランペット',
    flute: 'フルート',
    
    // Nature
    tree: '木',
    flower: '花',
    grass: '草',
    mountain: '山',
    river: '川',
    ocean: '海',
    beach: 'ビーチ',
    forest: '森',
    desert: '砂漠',
    cloud: '雲',
    sun: '太陽',
    moon: '月',
    star: '星'
  }
}