import os
import psycopg
from dotenv import load_dotenv
from psycopg import sql
from psycopg.rows import dict_row
from models.application import STATUS

load_dotenv()

def get_db_connection():
    """Create and return new PostgreSQL connection."""
    conn = psycopg.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
    return conn

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

            print("applications table successfully created.")

def delete_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS applications;")

        print("applications table successfully deleted.")

def insert_db(company, title, status):
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # Prepare sql statement with parameters
            sql = ("""
            INSERT INTO applications (company, title, status)
            VALUES (%s, %s, %s) RETURNING *;
            """)

            # Prepare data to be inserted 
            data = (company, title, status)

            result = cur.execute(sql, data).fetchone()

            if not result:
                raise RuntimeError(
                    f"Database failed to return the inserted job record. "
                    f"Inputs: company='{company}', title='{title}', status='{status}'"
                )

            # This is now handled automatically by conn.cursor(row_factory=dict_row) ==> returns a dict
            # new_job = {
            #     "id": result[0],
            #     "company": result[1],
            #     "title": result[2],
            #     "date_applied": result[3],
            #     "status": result[4],
            #     "date_interview": result[5],
            # }

            return result

def retrieve_all_db():
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            sql = ("SELECT * FROM applications")

            result = cur.execute(sql).fetchall()

            return result

def retrieve_id_db(app_id):
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            sql = ("SELECT * FROM applications WHERE id = %s;")

            result = cur.execute(sql, (app_id,)).fetchone()

            return result

def delete_id_db(app_id):
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            sql = ("DELETE FROM applications WHERE id = %s RETURNING *;")

            result = cur.execute(sql, (app_id,)).fetchone()

            return result

def update_id_db(app_id, data:dict):
    if not data:
        return None

    # [... "column" : %s ...]
    sql_parts = [
        sql.SQL("{} = %s").format(sql.Identifier(column))
        for column in data.keys()
    ]

    # "status" : %s, "title": "Junior Dev"
    set_clause = sql.SQL(", ").join(sql_parts)

    query = sql.SQL("UPDATE applications SET {fields} WHERE id = %s RETURNING *").format(
            fields=set_clause
        )
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            query_values = list(data.values()) + [app_id]

            cur.execute(query, query_values)
            result = cur.fetchone()

            return result