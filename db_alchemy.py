import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# SQLALCHEMY

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME =os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

engine = create_engine(
    DATABASE_URL,
    echo=os.environ.get("DB_ECHO", "False").lower() in ("true", "1", "t"),
)

SessionFactory = sessionmaker(
    bind=engine,
)

def get_db_session():
    """Generates a contextual transactional wrapper."""
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
