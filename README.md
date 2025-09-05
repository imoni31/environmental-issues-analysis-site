# Environmental Issues Analysis Site
環境問題を分析するサイト

## プロジェクト概要
このプロジェクトは環境データの分析と可視化を行うWebアプリケーションです。FlaskバックエンドとVue.jsフロントエンドで構成されています。

## システム構成
- **バックエンド**: Python Flask API
- **フロントエンド**: Vue.js 3
- **データ処理**: Pandas, NumPy
- **可視化**: Chart.js

## セットアップ手順

### 必要な環境
- Python 3.8以上
- Node.js 16以上
- npm または yarn

### バックエンド（Flask API）のセットアップ

1. **Python仮想環境の作成と有効化**
   ```bash
   # 仮想環境の作成
   python -m venv venv
   
   # 仮想環境の有効化
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **必要なパッケージのインストール**
   ```bash
   pip install -r requirements.txt
   ```

3. **バックエンドサーバーの起動**
   ```bash
   python app.py
   ```
   
   サーバーは http://localhost:5000 で起動します。

### フロントエンド（Vue.js）のセットアップ

1. **フロントエンドディレクトリに移動**
   ```bash
   cd frontend
   ```

2. **依存関係のインストール**
   ```bash
   npm install
   ```

3. **開発サーバーの起動**
   ```bash
   npm run serve
   ```
   
   フロントエンドは http://localhost:8080 で起動します。

## API エンドポイント

| エンドポイント | メソッド | 説明 |
|-------------|--------|------|
| `/api/environmental-data` | GET | 環境データの取得 |
| `/api/environmental-data/statistics` | GET | 統計データの取得 |
| `/api/locations` | GET | 利用可能な地域一覧の取得 |
| `/api/health` | GET | API健全性チェック |

## 開発コマンド

### フロントエンド
```bash
# 開発サーバー起動
npm run serve

# 本番ビルド
npm run build

# コード検証
npm run lint
```

### バックエンド
```bash
# 開発サーバー起動（デバッグモード）
python app.py
```

## プロジェクト構造
```
environmental-issues-analysis-site/
├── app.py                  # Flaskアプリケーション
├── requirements.txt        # Pythonパッケージ
├── frontend/              # Vue.jsフロントエンド
│   ├── package.json       # Node.js依存関係
│   ├── src/              # ソースコード
│   └── public/           # 静的ファイル
└── README.md             # このファイル
```
