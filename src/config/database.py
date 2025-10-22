import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Default to local sqlite for dev
if not DATABASE_URL and not CLOUD_SQL_CONNECTION_NAME:
    DATABASE_URL = "sqlite:///./jo2024.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:

    engine = create_engine(DATABASE_URL, future=True)


session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()