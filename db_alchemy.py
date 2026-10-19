import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import sessionmaker

from models.application import Application

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

def retrieve_all_alchemy(session):
    stmt = select(Application)
    applications = session.scalars(stmt).all()

    all_apps = []

    for app in applications:
        # Copy object's dictionary
        app_dict = app.__dict__.copy()
        # Take out SQLAlchemy implicit key
        app_dict.pop('_sa_instance_state', None)

        
        all_apps.append(app_dict)

        # OR 
        #        all_apps.append({
        #     "id": app.id,
        #     "company": app.company,
        #     "title": app.title,
        #     "status": app.status
        # })
    return all_apps