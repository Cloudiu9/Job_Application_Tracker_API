from db_old import insert_db

if __name__ == "__main__":
    new_job = insert_db("Nagarro", "Junior Software Developer", "applied")
    print(f"Inserted job: {new_job}")
