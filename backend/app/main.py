# app/main.py

from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import user, dog, reservation, location, qrcode  # 全モデルをimport！

# 🔽 この1行を追加（ルーター読み込み！）
from app.api import reservation as reservation_api
from app.api import location as location_api
from app.api import dog as dog_api

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