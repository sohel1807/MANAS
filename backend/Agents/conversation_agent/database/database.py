import psycopg2
import os
from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection(database_url):
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print("Database Connection Error:", e)
        return None