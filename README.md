# 🐶 Honda犬の一時預かりサービス（バックエンド）

FastAPI + SQLAlchemy + MySQL (Azure) を使った、Hondaディーラーでの犬の一時預かりサービスのバックエンドです。

---

## 🚀 セットアップ手順

### 1. 仮想環境の作成（推奨）

```bash
python -m venv venv
source venv/bin/activate  # Windowsなら venv\Scripts\activate

2. ライブラリのインストール
bash
コピーする
編集する
pip install -r requirements.txt

3. .env の作成（環境変数）
env
コピーする
編集する
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=your_host.mysql.database.azure.com
DB_PORT=3306
DB_NAME=step3_2_hondaken

AZURE_STORAGE_ACCOUNT_NAME=blobstep32
AZURE_BLOB_CONTAINER_NAME=team8-hondadog-locations
AZURE_BLOB_PATH=location_images/

4. 起動
bash
コピーする
編集する
uvicorn app.main:app --reload
アクセス → http://localhost:8000

📁 ディレクトリ構成
bash
コピーする
編集する
backend/
├── app/
│   ├── api/            # ルーティング
│   ├── core/           # DB接続など
│   ├── crud/           # DB操作ロジック
│   ├── models/         # SQLAlchemyモデル
│   ├── schemas/        # Pydanticスキーマ
│   └── main.py         # エントリーポイント
├── .env                # 環境変数（gitignore済）
├── requirements.txt
└── README.md
✅ 今後の予定
ユーザー登録機能の実装

QRコードチェックイン機能

JWT or Google OAuth2認証
