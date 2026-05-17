# utils/jwt_helpers.py

from datetime import datetime, timedelta, UTC
import jwt
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def generate_access_token(user):
    payload = {
        "user_id": user["id"],
        "provider": user["provider"],
        "role": user["role"],
        "exp": datetime.now(UTC) + timedelta(minutes=15),
        "type": "access"
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm="HS256"
    )


def generate_refresh_token(user): 
    payload = {
        "user_id": user["id"],
        "provider": user["provider"],
        "role": user["role"],
        "exp": datetime.now(UTC) + timedelta(days=30),
        "type": "refresh"
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm="HS256"
    )

