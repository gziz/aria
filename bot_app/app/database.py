from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

SQLALCHAMY_DATABASE_URL = f'postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_hostname}:{settings.postgres_port}/{settings.postgres_db}'
engine = create_engine(
    SQLALCHAMY_DATABASE_URL,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
