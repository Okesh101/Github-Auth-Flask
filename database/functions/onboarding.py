# database/functions/onboarding.py

from database.db import get_db_connection
import sqlite3, uuid

def get_user_by_provider_id(provider_id):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT * FROM users
            WHERE provider_id = ?
        """, 
        (provider_id,)
        )

        return cursor.fetchone()
    finally:
        if db:
            db.close()


def create_user(provider_id, provider, email, username, display_name, profile_pic, role='user'):
    db = get_db_connection()
    try:
        cursor = db.cursor()

        user_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO users (id, provider_id, provider, email, username, display_name, profile_pic, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, provider_id, provider, email, username, display_name, profile_pic, role,)
        )

        db.commit()

        return {
            "status": "SUCCESS",
            "code": 201,
            "message": "User created successfully.",
            "data": {
                "id": user_id,
                "provider_id": provider_id,
                "provider": provider,
                "email": email,
                "username": username,
                "display_name": display_name,
                "profile_pic": profile_pic,
                "role": role
            }
        }
    except sqlite3.Error as e:
        if db:
            db.rollback()
        return {
            "status": "ERROR",
            "code": 500,
            "message": f"DB error creating user: {e}."
        }
    finally:
        if db:
            db.close()