# line/service.py：　会話の中身とステップ制御

from app.line.utils import get_user_id_by_line_uid
from app.models.reservation import Reservation
from app.line.utils import get_user_id_by_line_uid
from datetime import datetime

# -----------------------
#   会話ステップ
# -----------------------

# ステップ0：「予約」と送られた時の最初の処理（LINE UIDからuseridを取得）
def handle_start_reservation(line_uid: str, db, user_sessions: dict) -> str:
    app_user_id = get_user_id_by_line_uid(db, line_uid)
    
    # LINE連携が完了しているユーザーか確認
    if not app_user_id:
        return (
            "ユーザー登録が見つかりません。\n"
            "アプリでLINE連携を行ってください。" 
        )
    
    # 登録されていればステップを「awaiting_date」に進める
    user_sessions[line_uid] = {"step": "awaiting_date"}
    return "いつにしますか？（例：4/10）"

# ステップ1：ユーザーが予約日を入力したときの処理
def handle_date_input(line_uid: str, message_text: str, user_sessions: dict) -> str:
    # 入力された日付をセッションに保存
    user_sessions[line_uid]["date"] = message_text
    
    # 次のステップ「awaiting_time_range」へ進める
    user_sessions[line_uid]["step"] = "awaiting_time_range"
    return "何時から何時までにしますか？（例：13:00-14:00）"

# ステップ2：ユーザーが時間帯（例：13:00-14:00）を入力したときの処理
def handle_time_range_input(line_uid: str, message_text: str, user_sessions: dict) -> str:
    try:
        # 13:00-14:00 の形式を分解
        start_str, end_str = message_text.split("-")
        
        # 開始時間と終了時間をセッションに保存
        user_sessions[line_uid]["start_time"] = start_str.strip()
        user_sessions[line_uid]["end_time"] = end_str.strip()
        
        # 次のステップへ
        user_sessions[line_uid]["step"] = "awaiting_location"
        return "ご希望の店舗を教えてください。"

    except ValueError:
        return "時間の形式が正しくありません。\n例：13:00-14:00 のように入力してください。"

# ステップ3：ユーザーが店舗名を入力したときの処理（最終ステップ）
def handle_location_input(line_uid: str, message_text: str, user_sessions: dict) -> str:
    # セッションに店舗名を保存
    user_sessions[line_uid]["location"] = message_text

    # セッションデータ取得（確認用）
    date = user_sessions[line_uid].get("date")
    start_time = user_sessions[line_uid].get("start_time")
    end_time = user_sessions[line_uid].get("end_time")
    location = user_sessions[line_uid].get("location")

    # 応答メッセージを整形
    reply_text = (
        f"{date} {start_time}〜{end_time} に\n"
        f"{location}での予約を受け付けました！\nありがとうございます🐶"
    )

    # セッション終了
    user_sessions.pop(line_uid, None)

    return reply_text

# ✅ DBに予約を保存する関数（セッション情報をもとに）
def save_reservation_to_db(line_uid: str, user_sessions: dict, db):
    session = user_sessions.get(line_uid)
    if not session:
        return False, "⚠️ セッション情報が見つかりませんでした。"

    try:
        year = datetime.now().year
        check_in = datetime.strptime(f"{year}/{session['date']} {session['start_time']}", "%Y/%m/%d %H:%M")
        check_out = datetime.strptime(f"{year}/{session['date']} {session['end_time']}", "%Y/%m/%d %H:%M")
    except ValueError:
        return False, "⚠️ 日付や時間の形式が正しくありません。"

    user_id = get_user_id_by_line_uid(db, line_uid)
    if not user_id:
        return False, "⚠️ ユーザーが見つかりませんでした。"

    # 仮のIDを使って予約を作成
    reservation = Reservation(
        user_id=user_id,
        location_id=1,
        dog_id=1,
        check_in_time=check_in,
        check_out_time=check_out,
        scheduled_start_time=check_in,
        scheduled_end_time=check_out
    )
    db.add(reservation)
    db.commit()
    return True, None
