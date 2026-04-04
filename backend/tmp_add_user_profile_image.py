"""Add profile_image column to users table"""
from app.db import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN profile_image VARCHAR"))
        conn.commit()
        print("Added profile_image column to users table")
    except Exception as e:
        print(f"Column may already exist: {e}")
        conn.rollback()
