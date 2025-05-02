from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

db_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT", 5432),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
