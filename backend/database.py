import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config import DATABASE_URL

if DATABASE_URL.startswith("postgres"):
    connect_url = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(connect_url, pool_pre_ping=True)
else:
    os.makedirs("data", exist_ok=True)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from backend.models import Job

    Base.metadata.create_all(bind=engine)
    print("[DB] Tables ready.")
