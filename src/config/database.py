import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL")  # ex: postgresql://user:pass@host:5432/dbname
CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME")  # ex: project:region:instance
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Default: local sqlite for dev (keep same behaviour if nothing provided)
if not DATABASE_URL and not CLOUD_SQL_CONNECTION_NAME:
    DATABASE_URL = "sqlite:///./jo2024.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # If CLOUD_SQL_CONNECTION_NAME is set, prefer the Cloud SQL Python connector with pg8000
    if CLOUD_SQL_CONNECTION_NAME:
        try:
            from google.cloud.sql.connector import Connector # type: ignore[import]
            connector = Connector()

            def getconn():
                return connector.connect(
                    CLOUD_SQL_CONNECTION_NAME,
                    "pg8000",
                    user=DB_USER,
                    password=DB_PASS,
                    db=DB_NAME,
                )

            # create_engine with creator that returns a raw DB-API connection
            engine = create_engine("postgresql+pg8000://", creator=getconn, future=True)
        except Exception:
            # Fallback to DATABASE_URL if connector not available
            if not DATABASE_URL:
                raise
            engine = create_engine(DATABASE_URL, future=True)
    else:
        # Use explicit DATABASE_URL (could be a proxy-hosted URL)
        engine = create_engine(DATABASE_URL, future=True)

# session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()