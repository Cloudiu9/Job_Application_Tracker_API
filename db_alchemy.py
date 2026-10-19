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

def retrieve_all_alchemy(session):
    stmt = select(Application)
    applications = session.scalars(stmt).all()

    all_apps = []

    for app in applications:
        all_apps.append({
            "id": app.id,
            "company": app.company,
            "title": app.title,
            "date_applied": app.date_applied,
            "status": app.status,
            "date_interview": app.date_interview
        })
    return all_apps

def retrieve_id_alchemy(session, app_id):
    stmt = select(Application).where(Application.id == app_id)
    application = session.scalars(stmt).one_or_none()

    if application is None:
        return None
    
    return {
        "id": application.id,
        "company": application.company,
        "title": application.title,
        "date_applied": application.date_applied,
        "status": application.status,
        "date_interview": application.date_interview
    }