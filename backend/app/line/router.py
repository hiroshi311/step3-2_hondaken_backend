from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from app.core.database import get_db
from app.line.service import (
    handle_start_reservation,
    handle_date_input,
    handle_time_range_input,
    handle_location_input,
    save_reservation_to_db,
)
import os
from dotenv import load_dotenv

# 環境変数の読み込み（LINEチャンネル設定）
load_dotenv()

router = APIRouter()
user_sessions = {}

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))

# LINEのWebhookエンドポイント
@router.post("/webhook")
async def webhook(
    request: Request,
    x_line_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    # リクエストボディ取得
    body = await request.body()
    body_text = body.decode("utf-8")

    # LINE署名の検証
    try:
        events = parser.parse(body_text, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # メッセージイベントごとに処理
    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            line_uid = event.source.user_id
            message_text = event.message.text.strip()

            # ステップ0：予約開始
            if message_text == "予約":
                reply_text = handle_start_reservation(line_uid, db, user_sessions)

            # ステップ1：日付入力
            elif user_sessions.get(line_uid, {}).get("step") == "awaiting_date":
                reply_text = handle_date_input(line_uid, message_text, user_sessions)

            #　ステップ2：時間入力
            elif user_sessions.get(line_uid, {}).get("step") == "awaiting_time_range":
                reply_text = handle_time_range_input(line_uid, message_text, user_sessions)
            
            # ステップ3：店舗入力
            elif user_sessions.get(line_uid, {}).get("step") == "awaiting_location":
                # DB保存処理を先に行う
                success, error = save_reservation_to_db(line_uid, user_sessions, db)
                if not success:
                    reply_text = error
                else:
                    # 応答だけする
                    reply_text = handle_location_input(line_uid, message_text, user_sessions)

            # それ以外（未対応 or セッションなし）
            else:
                reply_text = "「予約」と送ると予約が始まります！"

            # LINEに返信
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )

    return {"message": "OK"}
