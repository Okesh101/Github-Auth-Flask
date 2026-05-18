# routes/admin.py

from flask import Blueprint, jsonify, g
from middlewares.auth_middleware import require_auth
from middlewares.role_middleware import require_role
from database.functions.profile import get_all_users, get_me

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/v1/admin")


# =========================================
# ADMIN DASHBOARD
# =========================================
@admin_bp.route("/dashboard", methods=['GET'])
@require_auth
@require_role("admin")
def admin_dashboard_endpoint():

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
# GET ALL USERS
# =========================================
@admin_bp.route("/users", methods=["GET"])
@require_auth
@require_role("admin")
def get_users():

    user_result = get_all_users()
    return jsonify(user_result), user_result['code']
