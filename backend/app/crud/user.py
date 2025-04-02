from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from typing import List, Optional
from passlib.context import CryptContext


# パスワードのハッシュ化に使う（bcrypt）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ユーザー作成
def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        name_last=user.name_last,
        name_first=user.name_first,
        email=user.email,
        birthday=user.birthday,
        postal_code=user.postal_code,
        prefecture=user.prefecture,
        city=user.city,
        address_line=user.address_line,
        phone_number=user.phone_number,
        gender=user.gender,
        google_id=user.google_id,
        profile_image_url=user.profile_image_url,
        line_u_id=user.line_u_id,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


# ユーザーIDで取得
def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


# Email で取得（ログインなどで使用予定）
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()
