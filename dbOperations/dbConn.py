import os
import pymysql
from pymysql.err import OperationalError
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Returns a pymysql connection object.
    Connection parameters are read from environment variables.
    """
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "fyp")
        )
        print("✅ Database connection successful!")
        return conn
    except OperationalError as e:
        print(f"❌ Connection failed: {e}")
        return None
