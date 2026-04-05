import psycopg2
import os
from dotenv import load_dotenv

# Load env from the backend folder
load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")

def fix_users_table():
    conn = None
    try:
        print(f"Connecting to database: {DATABASE_URL}")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Make password column nullable
        print("Updating users table to allow NULL passwords...")
        cur.execute("ALTER TABLE users ALTER COLUMN password DROP NOT NULL;")
        
        conn.commit()
        print("Success! The users table has been updated.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    fix_users_table()
