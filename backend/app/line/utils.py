# line/utils.py：　LINE Bot機能に関連する軽めの処理・共通ユーティリティをまとめるファイル

from sqlalchemy.orm import Session
from app.models.user import User


# 「LINEのユーザーID（line_uid）を使って、アプリの内部ユーザーID（user.id）を取得する」関数
def get_user_id_by_line_uid(db: Session, line_uid: str):
    user = db.query(User).filter(User.line_u_id == line_uid).first()
    if user:
        return user.id
    return None