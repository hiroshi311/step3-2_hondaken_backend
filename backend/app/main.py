# app/main.py

from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import user, dog, reservation, location  # 全モデルをimport！
from app.models import qrcode  # ← QRコード実装後に有効化！

# 🔽 この1行を追加（ルーター読み込み！）
from app.api import reservation as reservation_api
from app.api import location as location_api
from app.api import dog as dog_api
from app.api import user as user_api
from app.api import qrcode as qr_api

from app.core import auth
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 🔽 .env読み込み（必ずここ！）
load_dotenv()
app = FastAPI()

# 本番環境だけHTTPSリダイレクトを有効にする
if os.getenv("ENV") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# CORS設定
origins = [
    "https://app-002-step3-2-node-oshima8.azurewebsites.net",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ← フロントのURL
    allow_credentials=True,
    allow_methods=["*"],  # ← これがないとPOSTすら通らない！
    allow_headers=["*"],
)


# テーブル作成（初期構築用）
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Azure MySQL Connected!"}

# ✅ ルーターを登録
app.include_router(dog_api.router)
app.include_router(location_api.router)
app.include_router(reservation_api.router)
app.include_router(user_api.router)
app.include_router(qr_api.router)

# clerk用を追加
#app.include_router(auth.router)