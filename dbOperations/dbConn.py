import pymysql
from pymysql.err import OperationalError

def get_connection():
    """
    Returns a pymysql connection object.
    Update host, user, password, and database as needed.
    """
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="fyp"  # replace with your DB name
        )
        print("✅ Database connection successful!")
        return conn
    except OperationalError as e:
        print(f"❌ Connection failed: {e}")
        return None
