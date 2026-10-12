from db import insert_db, retrieve_all_db, retrieve_id_db, delete_id_db
from models.application import STATUS, all_applications, ALLOWED_KEYS


def get_application_by_id(app_id):
    result = retrieve_id_db(app_id)

    if not result:
        return None

    return result


def get_applications():
    all_jobs = retrieve_all_db()
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
    result = delete_id_db(app_id)

    if not result:
        return None, "Could not find application to delete."
    
    return result, None

