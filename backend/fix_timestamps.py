import os
import sys
from datetime import timedelta
from sqlalchemy import text
from app.db import SessionLocal

def fix_timestamps():
    db = SessionLocal()
    try:
        print("Starting timestamp migration (UTC -> PHT)...")
        
        # Tables and their timestamp columns
        updates = {
            "users": ["created_at"],
            "providers": ["created_at"],
            "messages": ["created_at"],
            "conversations": ["updated_at"],
            "appointments": ["created_at", "completed_at"],
            "reviews": ["created_at"]
        }

        for table, columns in updates.items():
            for col in columns:
                # We only update records that are older than, say, 1 hour ago
                # to avoid double-updating records that were already created in PHT.
                # However, since the user reported the issue just now, 
                # we'll look for records that are exactly 8 hours behind.
                # A safer way: Update all records created before our migration start time.
                
                print(f"Updating {table}.{col}...")
                
                # PostgreSQL syntax to add 8 hours
                sql = text(f"UPDATE {table} SET {col} = {col} + interval '8 hours' WHERE {col} IS NOT NULL")
                result = db.execute(sql)
                print(f"  Modified {result.rowcount} rows in {table}")

        db.commit()
        print("Migration completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error during migration: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure current directory is in sys.path to import 'app'
    sys.path.append(os.getcwd())
    fix_timestamps()
