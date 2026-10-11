from flask import abort, jsonify, request
from psycopg import sql
from models.application import STATUS, all_applications, ALLOWED_KEYS
from db import get_db_connection

def initialize_db():
    # 'with' safely closes the connection at the end
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # We use sql.SQL and sql.Literal to safely format STATUS into the query
            query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS applications (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                company TEXT NOT NULL,
                title TEXT NOT NULL,
                date_applied DATE NOT NULL DEFAULT CURRENT_DATE, 
                status TEXT NOT NULL CHECK (status IN ({})),
                date_interview DATE
                );
        """).format(
            sql.SQL(", ").join(sql.Literal(s) for s in STATUS)
        )

            cur.execute(query)

            # in psycogp3 commit is usually automatically called at the end of with, but still call it just to make sure
            conn.commit()

    return "applications table successfully created."

def delete_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS applications;")

    return "applications table successfully deleted."

def get_application_by_id(app_id):
    for app in all_applications:
        if app['id'] == app_id:
            return app
    return None


def get_applications():
    return all_applications


def create_application(data):
    if data is None:
        return None, "Body must be a valid JSON."
    
    if data.get("status") not in STATUS:
        return None, "Bad request. (Status is missing or wrong)"
    
    if not data.get("company"):
        return None, "Bad request. (Missing company)"
    
    if not data.get("title"):
        return None, "Bad request. (Missing title)"

    # if omitted, = current date
    # if not data.get("date_applied"):
    #     return None, "Bad request. (Missing date applied)"

    # check against application list being empty
    last_id = all_applications[-1]["id"] if all_applications else 0

    new_app = { 
        "id": last_id + 1, 
        "company": data["company"], 
        "title": data["title"], 
        "date_applied": data["date_applied"], 
        "status": data["status"], 
        "date_interview": data.get("date_interview", None) 
    }

    all_applications.append(new_app)
    return new_app, None


def modify_application(app_id, data):
    application_to_modify = None
    for app in all_applications:
        if app["id"] == app_id:
            application_to_modify = app
            break

    if data is None:
        return None, "Body must be a valid JSON."

    if application_to_modify is None:
        return None, "Could not find application to modify."

    if "id" in data:
        return None, "Cannot modify id."

    if not any(key in data for key in ALLOWED_KEYS):
        return None, "No valid fields provided to modify."

        # wrong: any(key not in ALLOWED_KEYS for key in data)
        # all keys in data, is there any key not allowed
    if any(key not in ALLOWED_KEYS for key in data):
        return None, "Invalid field found."
    
    for key in ALLOWED_KEYS:
        if key in data:
            if key == "status":
                if data["status"] in STATUS:
                    application_to_modify["status"] = data["status"]
                else:
                    return None, "Incorrect status."
            else:
                application_to_modify[key] = data[key]

    return application_to_modify, None


def delete_application(app_id):
    for index, app in enumerate(all_applications):
        if app["id"] == app_id:
            del all_applications[index]
            return app, None

    return None, "Could not find application to delete."