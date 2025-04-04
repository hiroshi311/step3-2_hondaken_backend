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

app = FastAPI()

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