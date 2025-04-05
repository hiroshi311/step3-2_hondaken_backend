from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx, os
from dotenv import load_dotenv
from app.models.user import User
from app.core.database import get_db
from jose import jwt

load_dotenv()  # ← .envを読み込む
if os.path.exists(".env.local"):
    load_dotenv(".env.local", override=True)

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
print("✅ Clerk Key:", os.getenv("CLERK_SECRET_KEY"))  # ← ちゃんと出力されるか確認

router = APIRouter()

@router.post("/auth/callback")
async def auth_callback(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.split(" ")[1]

    # ✅ JWTを検証なしでデコード
    decoded = jwt.decode(token, key='', options={"verify_signature": False})
    user_id = decoded.get("sub")

    print("🧠 Decoded JWT:", decoded)
    print("🆔 User ID from JWT:", user_id)

    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"https://api.clerk.com/v1/users/{user_id}",
            headers={
                "Authorization": f"Bearer {CLERK_SECRET_KEY}"
            }
        )  

    # # JWTからuser_id（sub）を抽出
    # decoded = jwt.decode(token, options={"verify_signature": False})
    # user_id = decoded.get("sub")
    
    print("📩 Clerk API status:", res.status_code)
    print("📩 Clerk API body:", res.text)

    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")

    clerk_user = res.json()

    email = None
    if "email_addresses" in clerk_user and clerk_user["email_addresses"]:
        email = clerk_user["email_addresses"][0].get("email_address")

    first_name = clerk_user.get("first_name") or "名なし"
    last_name = clerk_user.get("last_name") or "姓なし"
    google_id = clerk_user.get("external_accounts", [{}])[0].get("provider_user_id")
    profile_image_url = clerk_user.get("image_url")

    if email is None:
        raise HTTPException(status_code=400, detail="Email not found in Clerk user data")

    # 既に登録されているか確認
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return {"message": "User already exists", "user_id": existing_user.id}

    # Clerk経由のユーザーはパスワード使わないのでダミー値を入れる（またはnullable=Trueに変更）
    dummy_hashed_password = "clerk-authenticated-user"

    new_user = User(
        name_first=first_name,
        name_last=last_name,
        email=email,
        google_id=google_id,
        profile_image_url=profile_image_url,
        hashed_password=dummy_hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "user_id": new_user.id}

async def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        token = authorization.split(" ")[1]
        decoded = jwt.decode(token, key='', options={"verify_signature": False})
        user_id = decoded.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.google_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user