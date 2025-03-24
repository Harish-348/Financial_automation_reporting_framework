# module/db_connection.py
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
# import os

load_dotenv()
# print(os.getenv("user"))
host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("password")
database=os.getenv("database")

DB_CONFIG = {
    "host": host,
    "user": user,
    "password": password,
    "database": database
}
engine = create_engine(f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

def execute_queries(queries):
    with engine.connect() as conn:
        for query in queries:
            conn.execute(text(query))
            conn.commit()

def fetch_data(query):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)