# routes/github.py

from flask import Flask, Blueprint, jsonify, url_for
from services.githubService import oauth

github_bp = Blueprint("github_bp", __name__, url_prefix="/api/v1/auth")


@github_bp.route("/github", methods=['GET'])
def github_login_endpoint():

    redirect_uri = url_for(
        "github_bp.github_callback",
        _external=True
    )

    github = oauth.create_client("github")

    return github.authorize_redirect(redirect_uri)


@github_bp.route("/github/callback", methods=['GET'])
def github_callback():

    try:
        github = oauth.create_client("github")

        token = github.authorize_access_token()

        return jsonify({
            "status": "SUCCESS",
            "token": token,
            "code": 200,
            "message": "Github token generated successfully."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "code": 500,
            "message": f"Error generating github token: {str(e)}"
        }), 500