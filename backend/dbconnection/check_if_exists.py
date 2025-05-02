# backend/dbconnection/check_if_exists.py

import psycopg2
from .db_pool import db_pool

def is_resume_already_in_db(filename):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM resumes WHERE filename = %s LIMIT 1", (filename,))
            return cur.fetchone() is not None
    finally:
        db_pool.putconn(conn)
