# AI画像分類・認識サービス

[![プロジェクトステータス](https://img.shields.io/badge/status-Phase%208%20Complete-brightgreen.svg)](https://github.com/M-Ito-7310/image-classification-service)
[![Python](https://img.shields.io/badge/python-3.12%2B-green.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/vue.js-3.5-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-blue.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0%2B-blue.svg)](https://www.typescriptlang.org/)
[![エンタープライズ対応](https://img.shields.io/badge/enterprise-ready-success.svg)](https://github.com/M-Ito-7310/image-classification-service)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**言語**: [English](README.md) | 日本語

本格的なAI画像分類サービスです。単一画像の高精度分析機能を提供し、最新のWeb技術で構築されています。Vue.js 3 + TypeScriptフロントエンドとFastAPIバックエンドを組み合わせ、実際のAIモデル統合、包括的な認証システム、直感的なユーザーインターフェース設計を特徴としています。

## 概要

このプロジェクトは、本格的なAI/ML統合、モダンなWeb開発プラクティス、スケーラブルなフルスタック構成を実証するものです。実際のAI統合、セキュアな認証、多言語サポート、プロフェッショナルなUI/UX設計による高度な開発スキルを示す包括的なポートフォリオプロジェクトとして構築されています。

## アーキテクチャ概要

### システムコンポーネント
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js Web    │    │  FastAPI Server │    │   AIサービス    │
│   フロントエンド │◄──►│   バックエンド   │◄──►│  TensorFlow/    │
│                 │    │                 │    │  Google Cloud   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  静的アセット    │    │   PostgreSQL    │    │  ファイル保存    │
│   (Nginx CDN)   │    │   データベース   │    │    システム      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 主要機能

### 🔍 **画像処理機能**
- **AI分類**: インテリジェント選択機能付きTensorFlowとPyTorchモデルサポート ✅ **実装済み**
- **単一画像処理**: 個別画像分析用の最適化されたワークフロー ✅ **実装済み**
- **スマート前処理**: 自動リサイズ、正規化、検証機能 ✅ **実装済み**
- **信頼度スコア**: 閾値フィルタリング機能付き詳細予測信頼度 ✅ **実装済み**
- **カスタムモデルサポート**: カスタム訓練モデルのアップロードと管理 ✅ **実装済み**
- **結果キャッシング**: パフォーマンス向上のためのインテリジェントキャッシングシステム ✅ **実装済み**
- **セキュリティ検証**: 包括的なファイルセキュリティスキャンと検証 ✅ **実装済み**

### 📤 **アップロードシステム**
- **ドラッグ&ドロップ**: 視覚的フィードバック付きモダンな単一ファイルアップロード ✅ **実装済み**
- **形式サポート**: JPEG、PNG、WebP、BMP画像形式 ✅ **実装済み**
- **ファイル検証**: 10MBまでのサイズ・セキュリティ検証 ✅ **実装済み**
- **画像プレビュー**: 処理前のリアルタイム画像プレビュー ✅ **実装済み**
- **進捗追跡**: アップロードと処理の進捗インジケーター ✅ **実装済み**

### 📊 **結果・分析機能**
- **インタラクティブ結果**: 信頼度スコア付き視覚的分類結果 ✅ **実装済み**
- **分類履歴**: ユーザー認証による永続的ストレージ ✅ **実装済み**
- **エクスポート機能**: JSONとCSVエクスポート形式 ✅ **実装済み**
- **処理メトリクス**: リアルタイム処理時間表示 ✅ **実装済み**
- **画像メタデータ**: 詳細ファイル情報と分析データ ✅ **実装済み**

### 🎨 **モダンユーザーインターフェース**
- **レスポンシブデザイン**: Tailwind CSSによるモバイルファースト設計 ✅ **実装済み**
- **ダーク/ライトテーマ**: ユーザー設定によるテーマ切り替え ✅ **実装済み**
- **多言語対応**: Vue I18nによる完全な日本語・英語インターフェース ✅ **実装済み**
- **ユーザー認証**: JWT認証によるセキュアなユーザー管理システム ✅ **実装済み**
- **モダンコンポーネント**: スムースな遷移付きHeadless UIコンポーネント ✅ **実装済み**
- **アクセシビリティ**: キーボードナビゲーションとスクリーンリーダーサポート ✅ **実装済み**
- **プロフェッショナルデザイン**: 視覚的フィードバック付きクリーンで直感的なインターフェース ✅ **実装済み**

### 🔧 **システム管理**
- **モデル管理**: カスタムAIモデルのアップロード、検証、管理 ✅ **実装済み**
- **ユーザープロファイル**: 個人設定と分類履歴管理 ✅ **実装済み**
- **システムモニタリング**: ヘルスチェックとパフォーマンス指標 ✅ **実装済み**
- **セキュリティ機能**: ファイル検証と脅威検知 ✅ **実装済み**
- **データベース統合**: ユーザーデータと履歴管理付きPostgreSQL ✅ **実装済み**
- **APIドキュメント**: 自動生成OpenAPI/Swaggerドキュメント ✅ **実装済み**

### 🔧 **開発者向け機能**
- **RESTful API**: OpenAPI/Swaggerドキュメント付き包括的API ✅ **実装済み**
- **ヘルスモニタリング**: システムヘルスチェックとパフォーマンス指標 ✅ **実装済み**
- **コンテナ化デプロイメント**: DockerとDocker Composeサポート ✅ **実装済み**
- **開発ツール**: ホットリロード、テスト、デバッグユーティリティ ✅ **実装済み**
- **型安全性**: 厳密な型付けによる完全なTypeScript統合 ✅ **実装済み**
- **データベース管理**: マイグレーションとインデックス付きPostgreSQL ✅ **実装済み**
- **セキュリティミドルウェア**: 多層検証と認証システム ✅ **実装済み**

## 技術スタック

### フロントエンドアーキテクチャ
- **フレームワーク**: Vue.js 3（Composition API + TypeScript）
- **ビルドシステム**: Vite 7.0による高速開発と最適化ビルド
- **スタイリング**: Tailwind CSS 3.4（PostCSS、Autoprefixer付き）
- **状態管理**: Piniaによる集中状態管理
- **ルーティング**: Vue Router 4によるSPAナビゲーション
- **テスティング**: Vitestによるユニットテスト、PlaywrightによるE2Eテスト
- **型安全性**: Vue TSCによる完全なTypeScript統合

### バックエンドアーキテクチャ
- **フレームワーク**: Python FastAPI 0.115（async/awaitサポート付き）
- **APIドキュメント**: 自動生成OpenAPI 3.0ドキュメント
- **データベース**: PostgreSQL 15+（SQLAlchemy 2.0 ORMと最適化インデックス）
- **認証**: セキュアなセッション管理用JWTトークン
- **ファイル処理**: マルチパートサポート付き非同期ファイル処理
- **バリデーション**: Pydantic 2.10によるデータ検証とシリアライゼーション
- **キャッシング**: パフォーマンス最適化のためのRedis統合
- **セキュリティ**: レート制限付き多層セキュリティミドルウェア

### AI/ML統合
- **ディープラーニング**: インテリジェントモデル選択によるTensorFlow 2.18とPyTorch 2.5サポート
- **コンピュータビジョン**: OpenCV 4.10による高度な画像前処理
- **クラウドAI**: フォールバックサポート付きGoogle Cloud Vision API統合
- **マルチモーダルAI**: 動画、音声、統合メディア分類
- **画像処理**: Pillow 11.0による形式変換と最適化
- **モデル管理**: 動的モデルロード、カスタムモデルサポート、マーケットプレイス
- **パフォーマンス**: 自動最適化によるGPUアクセラレーションサポート
- **リアルタイム処理**: WebSocketベースストリーミング分類

### インフラストラクチャ & DevOps
- **コンテナ化**: 開発・本番用DockerとDocker Compose
- **データベース**: 接続プーリング、マイグレーション、戦略的インデックス付きPostgreSQL
- **キャッシング**: セッションストレージ、結果キャッシング、リアルタイムデータ用Redis
- **リバースプロキシ**: 静的ファイルとロードバランシング用Nginx
- **モニタリング**: 強化されたヘルスチェック、システムメトリクス、包括的分析ダッシュボード
- **環境管理**: 本番デプロイメント用Dockerマルチステージビルド
- **セキュリティ**: 多層セキュリティミドルウェア、ファイル検証、脅威検知
- **APIゲートウェイ**: レート制限、APIキー管理、使用量追跡
- **課金システム**: 使用量ベース収益化とサブスクリプションティア
- **コラボレーションツール**: ワークスペース管理とチームコラボレーション機能

## クイックスタート

### 前提条件
- **Node.js** 22+（推奨）またはNode.js 20.19+
- **Python** 3.11以上
- **Docker**とDocker Compose（オプションですが推奨）
- **AI APIキー**（クラウド機能用Google Cloud Vision API）

### インストール

#### オプション1: Docker開発環境（推奨）

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/M-Ito-7310/image-classification-service.git
   cd image-classification-service
   ```

2. **環境設定**
   ```bash
   # 環境テンプレートをコピー
   cp .env.example .env
   
   # 環境変数を設定
   # クラウド機能を使用する場合はGoogle Cloud Vision APIキーを追加
   ```

3. **Docker Composeで起動**
   ```bash
   # すべてのサービスを起動（フロントエンド、バックエンド、データベース）
   docker-compose up -d
   
   # サービスステータスを確認
   docker-compose ps
   ```

4. **アプリケーションへのアクセス**
   - **フロントエンド**: http://localhost:3000
   - **バックエンドAPI**: http://localhost:8000
   - **APIドキュメント**: http://localhost:8000/docs
   - **データベース**: localhost:5432 (PostgreSQL)

#### オプション2: ローカル開発セットアップ

1. **バックエンドセットアップ**
   ```bash
   cd backend
   
   # Python仮想環境を作成
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # 依存関係をインストール
   pip install -r requirements.txt
   
   # バックエンドサーバーを起動
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **フロントエンドセットアップ**
   ```bash
   cd frontend
   
   # Node.js依存関係をインストール
   npm install
   
   # 開発サーバーを起動
   npm run dev
   ```

3. **データベースセットアップ**（基本機能にはオプション）
   ```bash
   # DockerでPostgreSQLを使用
   docker run --name postgres-dev \
     -e POSTGRES_DB=image_classification \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -p 5432:5432 -d postgres:15
   ```

### クイックテスト

1. **APIヘルスチェック**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. **フロントエンドアクセス**
   - ブラウザでhttp://localhost:3000を開く
   - ドラッグ&ドロップインターフェースで画像をアップロード
   - リアルタイムで分類結果を表示

## APIドキュメント

### 認証
セキュアなセッション管理とAPIキーサポートを備えたJWTベース認証システム。エンタープライズ機能には有効なAPIキーが必要です。

### コアエンドポイント

#### 画像分類
```http
POST /api/v1/classify
Content-Type: multipart/form-data

パラメータ:
- file: 画像ファイル（必須）
- model: モデル名（オプション、デフォルト: "auto"）
- threshold: 信頼度閾値（オプション、デフォルト: 0.5）
```

#### モデル管理
```http
GET /api/v1/models                    # 利用可能モデル一覧
POST /api/v1/models/upload           # カスタムモデルアップロード
GET /api/v1/models/custom            # ユーザーのカスタムモデル一覧
```

#### ヘルスチェック
```http
GET /api/v1/health                   # 基本ヘルスチェック
GET /api/v1/health/detailed # 詳細ヘルスチェック
```

完全なAPIドキュメントについては、http://localhost:8000/docs をご覧ください。

## プロジェクト構造

```
image-classification-service/
├── frontend/                 # Vue.jsフロントエンドアプリケーション
│   ├── src/
│   │   ├── components/      # Vueコンポーネント
│   │   │   ├── Upload/      # 画像アップロードコンポーネント
│   │   │   ├── Results/     # 分類結果表示
│   │   │   ├── History/     # 分類履歴
│   │   │   └── Common/      # 再利用可能UIコンポーネント
│   │   ├── views/           # ページコンポーネント
│   │   ├── stores/          # Pinia状態管理
│   │   ├── services/        # APIサービスレイヤー
│   │   ├── types/           # TypeScript型定義
│   │   └── utils/           # ユーティリティ関数
│   ├── public/              # 静的アセット
│   ├── tests/               # フロントエンドテスト
│   └── package.json
├── backend/                  # FastAPIバックエンドアプリケーション
│   ├── app/
│   │   ├── api/            # APIルートとエンドポイント
│   │   │   └── v1/         # APIバージョン1
│   │   ├── core/           # アプリケーション設定
│   │   ├── models/         # データベースモデル
│   │   ├── schemas/        # Pydanticスキーマ
│   │   ├── services/       # ビジネスロジック
│   │   │   ├── ai/         # AI/MLサービス
│   │   │   └── image/      # 画像処理サービス
│   │   └── utils/          # ユーティリティ関数
│   ├── tests/              # バックエンドテスト
│   └── requirements.txt
├── docker/                   # Docker設定ファイル
│   ├── frontend.Dockerfile
│   ├── backend.Dockerfile
│   └── nginx.conf
├── docs/                     # プロジェクトドキュメント
│   ├── API.md              # APIリファレンス
│   ├── DEPLOYMENT.md       # デプロイメントガイド
│   └── DEVELOPMENT.md      # 開発ガイド
├── scripts/                  # 開発・デプロイメントスクリプト
├── docker-compose.yml       # 開発環境セットアップ
├── Makefile                 # 開発コマンド
├── ROADMAP.ja.md           # 開発ロードマップ（日本語）
└── README.ja.md            # このファイル
```

## 開発

### バックエンド開発
```bash
cd backend

# 開発用依存関係をインストール
pip install -r requirements-dev.txt

# テストを実行
pytest

# コードフォーマット
black .
isort .

# 型チェック
mypy .

# 開発サーバーを起動
uvicorn app.main:app --reload
```

### フロントエンド開発
```bash
cd frontend

# ホットリロード付き開発サーバー
npm run dev

# 型チェック
npm run type-check

# リンティングとフォーマット
npm run lint
npm run format

# ユニットテストを実行
npm run test:unit

# E2Eテストを実行
npm run test:e2e

# 本番用ビルド
npm run build
```

### 開発コマンド（Makefile）
```bash
make dev          # 開発環境を起動
make build        # すべてのコンテナをビルド
make test         # すべてのテストを実行
make clean        # コンテナとボリュームをクリーンアップ
make logs         # アプリケーションログを表示
```

## 環境設定

### 必須環境変数
```env
# API設定
FASTAPI_ENV=development
API_HOST=0.0.0.0
API_PORT=8000

# データベース設定  
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/image_classification

# AIサービス設定
GOOGLE_CLOUD_VISION_API_KEY=your_api_key_here
HUGGING_FACE_API_KEY=your_hf_key_here

# ファイルアップロード設定
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp,bmp

# セキュリティ
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### オプション設定
```env
# Redisキャッシュ（本番用）
REDIS_URL=redis://localhost:6379

# モデル設定
DEFAULT_MODEL=imagenet_mobilenet_v2
MODEL_CACHE_SIZE=2GB
GPU_ENABLED=false

# モニタリング
ENABLE_METRICS=true
LOG_LEVEL=INFO
```

## テスト

### バックエンドテスト
```bash
# ユニットテスト
pytest tests/unit/

# 統合テスト
pytest tests/integration/

# APIテスト
pytest tests/api/

# カバレッジレポート
pytest --cov=app tests/
```

### フロントエンドテスト
```bash
# Vitestによるユニットテスト
npm run test:unit

# PlaywrightによるE2Eテスト
npm run test:e2e

# コンポーネントテスト
npm run test:component
```

## パフォーマンス & モニタリング

### パフォーマンス指標
- **APIレスポンス時間**: 標準分類で< 3秒
- **単一画像処理**: リアルタイムフィードバック付き最適化ワークフロー
- **メモリ使用量**: 最小2GB RAM、4GB+で最適化
- **ファイル処理**: 検証機能付き最大10MBファイルサポート
- **キャッシュパフォーマンス**: より高速な繰り返しクエリのための結果キャッシング
- **データベースパフォーマンス**: インデックス最適化付きPostgreSQL

### モニタリング機能
- **ヘルスチェックエンドポイント**: システムステータスと依存関係モニタリング
- **パフォーマンス指標**: レスポンス時間とスループット追跡
- **エラー追跡**: 包括的なエラーログとレポート
- **リソースモニタリング**: CPU、メモリ、GPU使用率
- **キャッシュ分析**: Redisパフォーマンスとヒット率モニタリング
- **セキュリティモニタリング**: ファイルアップロード検証と脅威検出

## デプロイメント

### 本番デプロイメント

#### Docker本番ビルド
```bash
# 本番イメージをビルド
docker-compose -f docker-compose.prod.yml build

# 本番環境にデプロイ
docker-compose -f docker-compose.prod.yml up -d
```

#### クラウドデプロイメント（AWS/GCP/Azure）
詳細なクラウドデプロイメントガイドについては[DEPLOYMENT.md](./docs/DEPLOYMENT.md)をご覧ください。

### 環境別設定
- **開発**: ホットリロード、デバッグログ、開発用依存関係
- **ステージング**: デバッグシンボル付き本番ビルド、テストデータ
- **本番**: 最適化ビルド、セキュリティ強化、モニタリング

## コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを開く

### 開発ガイドライン
- フロントエンド開発ではTypeScriptベストプラクティスに従う
- バックエンド開発ではPython型ヒントを使用し、PEP 8に従う
- 新機能の包括的なテストを書く
- API変更のドキュメントを更新
- 提出前にDockerビルドが通ることを確認

## ロードマップ

詳細な開発フェーズと今後の機能については[ROADMAP.ja.md](./ROADMAP.ja.md)をご覧ください。

**現在のステータス**: ✅ 本番対応コアシステム（完成）

### 開発進捗
- ✅ **フェーズ1**: 基盤アーキテクチャ（完了）
- ✅ **フェーズ2**: AI統合・UI開発（完了）
- ✅ **フェーズ3**: 高度機能（完了）
- ✅ **フェーズ4**: 本番最適化（完了）
- ✅ **フェーズ5**: デプロイメント（完了）
- ✅ **フェーズ6**: システム統合（完了）

## トラブルシューティング

### バックエンドサーバーの問題

**問題**: `uvicorn` コマンドが認識されない
```bash
'uvicorn' は、内部コマンドまたは外部コマンド、操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```

**解決策**: Pythonモジュール実行を使用
```bash
# 以下の代わりに: uvicorn main:app --reload
# 以下を使用: 
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### インポートエラー

**問題**: モジュールインポートエラー
```bash
ERROR:    Error loading ASGI app. Could not import module "main".
```

**解決策**: 正しいモジュールパスを確認
- `main:app` ではなく `app.main:app` を使用
- `backend` ディレクトリから実行する

### ポート競合

**問題**: ポートが既に使用中

**解決策**: ポートを変更するか既存プロセスを終了
```bash
# ポートを変更
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# ポート8000を使用しているプロセスを確認・終了
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID番号> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID番号>
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## サポート

サポートとご質問:
- GitHubでイシューを開く
- [APIドキュメント](http://localhost:8000/docs)を確認
- [開発ロードマップ](./ROADMAP.ja.md)を確認
- [デプロイメントガイド](./docs/DEPLOYMENT.md)を参照