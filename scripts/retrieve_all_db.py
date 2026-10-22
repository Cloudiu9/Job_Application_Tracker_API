from db_old import retrieve_all_db

if __name__ == "__main__":
    all_jobs = retrieve_all_db()
    print(f"All jobs: {all_jobs}")
