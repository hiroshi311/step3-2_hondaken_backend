from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# 共通スキーマ（Base）
class UserBase(BaseModel):
    name_last: str
    name_first: str
    email: EmailStr
    birthday: Optional[datetime] = None
    postal_code: Optional[str] = None
    prefecture: Optional[str] = None
    city: Optional[str] = None
    address_line: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    google_id: Optional[str] = None
    profile_image_url: Optional[str] = None
    line_u_id: Optional[str] = None

# 登録時（リクエスト用）
class UserCreate(UserBase):
    password: str  # パスワードは平文で受け取り、後でハッシュ化

# レスポンス時
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
