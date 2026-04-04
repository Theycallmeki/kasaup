"""Add is_approved column to users table"""
from app.db import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN is_approved BOOLEAN NOT NULL DEFAULT TRUE"))
        conn.commit()
        print("Added is_approved column to users table (existing users default to TRUE)")
    except Exception as e:
        print(f"Column may already exist: {e}")
        conn.rollback()
