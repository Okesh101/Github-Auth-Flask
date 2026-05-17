# routes/auth.py

from flask import Blueprint, jsonify, request, g
from middlewares.auth_middleware import require_auth
from database.functions.jwt_auth import (
    verify_refresh_token,
    revoke_refresh_token
)
from database.functions.profile import get_me
from datetime import datetime, timedelta, UTC
import jwt
import os

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/v1/auth")

JWT_SECRET = os.getenv("JWT_SECRET_KEY")
IS_PRODUCTION = os.getenv("FLASK_ENV") == "production"

# =========================================
# REFRESH ACCESS TOKEN
# =========================================
@auth_bp.route("/refresh", methods=['POST'])
def refresh_token_endpoint():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({
            "status": "ERROR",
            "code": 401,
            "message": "Refresh token missing"
        }), 401

    # =========================
    # VERIFY JWT
    # =========================
    try:
        decoded = jwt.decode(
            refresh_token,
            JWT_SECRET,
            algorithms=["HS256"]
        )

    except jwt.ExpiredSignatureError:
        return jsonify({
            "status": "ERROR",
            "code": 401,
            "message": "Refresh token expired"
        }), 401

    except jwt.InvalidTokenError:
        return jsonify({
            "status": "ERROR",
            "code": 401,
            "message": "Invalid refresh token"
        }), 401

    # =========================
    # CHECK TOKEN TYPE
    # =========================
    if decoded["type"] != "refresh":
        return jsonify({
            "status": "ERROR",
            "code": 401,
            "message": "Invalid token type"
        }), 401

    # =========================
    # VERIFY TOKEN IN DATABASE
    # =========================
    db_token = verify_refresh_token(refresh_token)

    if db_token["code"] != 200:
        return jsonify(db_token), db_token["code"]

    # =========================
    # CREATE NEW ACCESS TOKEN
    # =========================
    access_payload = {
        "user_id": decoded["user_id"],
        "email": decoded["email"],
        "role": decoded["role"],
        "type": "access",
        "exp": datetime.now(UTC) + timedelta(minutes=15)
    }

    new_access_token = jwt.encode(
        access_payload,
        JWT_SECRET,
        algorithm="HS256"
    )

    return jsonify({
        "status": "SUCCESS",
        "code": 200,
        "message": "Access token refreshed successfully.",
        "access_token": new_access_token
    }), 200


# =========================================
# GET CURRENT USER
# =========================================
@auth_bp.route("/me", methods=["GET"])
@require_auth
def me_endpoint():

    try:
        user_id = g.user["user_id"]

        user_data = get_me(user_id)

        return jsonify(user_data), user_data["code"]

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "code": 500,
            "message": str(e)
        }), 500


# =========================================
# LOGOUT USER
# =========================================
@auth_bp.route("/logout", methods=["POST"])
@require_auth
def logout_endpoint():

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({
            "status": "ERROR",
            "code": 401,
            "message": "Refresh token missing"
        }), 401

    revoke_result = revoke_refresh_token(refresh_token)

    if revoke_result["code"] != 200:
        return jsonify(revoke_result), revoke_result["code"]

    response = jsonify({
        "status": "SUCCESS",
        "code": 200,
        "message": "Logged out successfully."
    })

    response.delete_cookie(
        "refresh_token",
        httponly=True,
        secure=True if IS_PRODUCTION else False,
        samesite="None" if IS_PRODUCTION else "Lax",
    )

    return response, 200
