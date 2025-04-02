from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# ← ここ！ssl_mode を含めない
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SSL証明書のパス
ssl_cert = os.path.join(os.path.dirname(__file__), "DigiCertGlobalRootCA.crt.pem")

# ← sslはここで別に設定（macOS用）
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {"ssl-ca": "/etc/ssl/cert.pem"}
    }
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
