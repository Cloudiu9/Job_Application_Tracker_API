from db import update_id_db

if __name__ == "__main__":
    new_job = update_id_db(1, data={"status":"interview", "company":"Continental", "title":""})
    print(f"Modified job: {new_job}")
