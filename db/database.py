import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

def get_connection():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT")),
            cursorclass=DictCursor,
            ssl={"ssl": {}}
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None
