from datetime import datetime

from db import insert_db, retrieve_all_db, retrieve_id_db, delete_id_db, update_id_db
from db_alchemy import SessionFactory, retrieve_all_alchemy
from models.application import STATUS, ALLOWED_KEYS
from exceptions import ApplicationNotFoundError, ValidationError

def get_application_by_id(app_id):
    result = retrieve_id_db(app_id)

    if not result:
        return None

    return result


def get_applications():
    with SessionFactory() as session:
        all_jobs = retrieve_all_alchemy(session)
        print(all_jobs)
    return all_jobs


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
    # not necessary with PostgreSQL
    # last_id = all_applications[-1]["id"] if all_applications else 0

    # new_app = { 
    #     "id": last_id + 1, 
    #     "company": data["company"], 
    #     "title": data["title"], 
    #     "date_applied": data["date_applied"], 
    #     "status": data["status"], 
    #     "date_interview": data.get("date_interview", None) 
    # }

    new_job = insert_db(data["company"],
            data["title"], 
            data["status"])

    return new_job, None


def modify_application(app_id, data):
    if not isinstance(data, dict):
        raise ValidationError( "Body must be a valid JSON.")

    if "id" in data:
        raise ValidationError("Cannot modify id.")

    DATE_FIELDS = ["date_interview", "date_applied"]

    for field in DATE_FIELDS:
        if field in data:
            value = data[field]

            if data[field] is None and field == "date_interview":
                continue

            if not isinstance(value, str):
                raise ValidationError(f"The field {field} must be a string.")

            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(
                    f"Invalid date format for {field}. Please use the ISO standard YYYY-MM-DD (e.g., 2026-11-13, 2026-1-1)"
                )

    # all keys in allowed keys, is there any valid key in data
    if not any(key in data for key in ALLOWED_KEYS):
        raise ValidationError("No valid fields provided to modify.") 

    # all keys in data, is there any key not allowed
    if any(key not in ALLOWED_KEYS for key in data):
        raise ValidationError("Invalid field found.")   


    # don't allow null, except for date_interview
    if any((isinstance(value, str) and value.strip() == "") or (value is None and key != "date_interview") for key, value in data.items()):
        raise ValidationError("Empty field found.") 
    
    # only allow strings, except for date_interview (which can be null)
    if not all(isinstance(value,str) or key == "date_interview" for key, value in data.items()):
        raise ValidationError("Non-string field found.") 
    
    for key in ALLOWED_KEYS:
        if key in data:
            if key == "status":
                if not data["status"] in STATUS:
                    raise ValidationError("Incorrect status.") 

    application_to_modify = update_id_db(app_id, data)

    if application_to_modify is None:
        raise ApplicationNotFoundError("Application not found.")
    

    return application_to_modify


def delete_application(app_id):
    result = delete_id_db(app_id)

    if not result:
        return None, "Could not find application to delete."
    
    return result, None

