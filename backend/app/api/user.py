from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import User, UserCreate, UserUpdate
from app.crud import user as crud
from app.core.database import SessionLocal
from app.models.user import User as UserModel
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# DBセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ユーザー登録（POST /users/）
@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


# ユーザー一覧取得（GET /users/）
@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


# ユーザー詳細取得（GET /users/{user_id}）
@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ログインユーザー自身の情報を更新（マイページ用）PUT /users/me
@router.put("/me", response_model=User)
def update_my_info(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    updated_user = crud.update_user(db, user_id=current_user.id, updates=user_update.dict(exclude_unset=True))
    return updated_user

# ユーザー情報を任意に更新（管理者用・非認証）PUT /users/{user_id}
@router.put("/{user_id}", response_model=User)
def update_user_info(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id=user_id, updates=user_update.dict(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

#from app.core.auth import get_current_user  # ← 忘れずにインポート！
#from app.models.user import User as UserModel  # ← DBモデルのUser

# 認証ユーザー専用のマイページ（GET /users/mypage）
#@router.get("/mypage", response_model=User)
#def read_my_page(current_user: UserModel = Depends(get_current_user)):
#    return current_user