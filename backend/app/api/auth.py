# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta
from typing import Optional

from app.schemas.auth import UserLogin, Token
from app.schemas.user import User as UserResponseSchema
from app.schemas.user import UserCreate  # ← 🔄 こっちは詳細なUserCreate
from app.core.security import (
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.core.database import get_db
from app.crud.user import get_user_by_email, create_user  # ← 🔄 登録処理を呼び出す
from app.models.user import User

router = APIRouter()

# トークン取得に使われる依存関数
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ✅ トークンから現在のユーザーを取得
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

# 🔐 ログイン処理
@router.post("/auth/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 🆕 ユーザー登録処理
@router.post("/auth/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.get("/auth/me", response_model=UserResponseSchema)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

