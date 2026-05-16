# routes/health.py

from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint("health_bp", __name__, url_prefix="/api/v1")

@health_bp.route("/health", methods=['GET'])
def health_check_endpoint():
    return jsonify({
        "status": "SUCCESS",
        "code": 200,
        "message": f"Server is running at {str(datetime.now().time()).split(".")[0]}"
    }), 200