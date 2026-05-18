# database/functions/profile.py

from database.db import get_db_connection


def get_me(user_id):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, email, display_name, profile_pic FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return {
                "status": "SUCCESS",
                "data": {
                    "id": user[0],
                    "email": user[1],
                    "name": user[2],
                    "picture": user[3]
                },
                "code": 200,
                "message": "User details fetched successfully"
            }
        else:
            return {
                "status": "ERROR",
                "message": "User not found",
                "code": 404
            }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e),
            "code": 500
        }
    finally:
        if db:
            db.close()


def get_all_users():
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users"
        )
        rows = cursor.fetchall()

        if rows is None:
            return {
                "status": "SUCCESS",
                "code": 200,
                "data": {},
                "message": "No users have been registered."
            }
        
        userData = []
        for row in rows:
            userData.append({
                "id": row['id'],
                "provider": row['provider'],
                "email": row['email'],
                "username": row['username'],
                "display_name": row['display_name'],
                "picture": row['profile_pic'],
                "joined_at": row['created_at']
            })

        return {
            "status": "SUCCESS",
            "code": 200,
            "data": userData,
            "message": "All users retreived successfully"
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "code": 500,
            "message": f"DB error fetching users: {e}."
        }
    finally:
        if db:
            db.close()
