# routes/github.py

from flask import redirect, Blueprint, jsonify, url_for
from services.githubService import oauth
from database.functions.onboarding import get_user_by_provider_id, create_user
from utils.jwt_helpers import generate_access_token, generate_refresh_token
from urllib.parse import quote
from datetime import datetime, timedelta, UTC
from database.functions.jwt_auth import save_refresh_token
import os

github_bp = Blueprint("github_bp", __name__, url_prefix="/api/v1/auth")

FRONTEND_URL = os.getenv("FRONTEND_URL")
IS_PRODUCTION = os.getenv("FLASK_ENV") == "production"


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

        # Exchange code for github access token
        token = github.authorize_access_token()

        # Fetch github profile
        profile_response = github.get("user")
        github_user = profile_response.json()

        # Fetch github emails
        email_response = github.get("user/emails")
        emails = email_response.json()

        primary_email = None

        for email in emails:
            if (email.get("primary") is True and email.get("verified") is True):
                primary_email = email.get("email")
                break

        if not primary_email:
            return jsonify({
                "status": "ERROR",
                "code": 400,
                "message": "No verified primary email found."
            }), 400
        
        provider_id = str(github_user.get("id"))

        # Check if user exists
        existing_user = get_user_by_provider_id(provider_id)

        # Existing user login
        if existing_user:
            access_token = generate_access_token(existing_user)
            refresh_token = generate_refresh_token(existing_user)
            expires_at = datetime.now(UTC) + timedelta(days=30)

            save_result = save_refresh_token(existing_user["id"], refresh_token, expires_at)

            if save_result['code'] != 200:
                return jsonify(save_result), save_result['code']
            
            encoded_access_token = quote(access_token)

            response = redirect(
                f"{FRONTEND_URL}/auth/callback"
                f"?access_token={encoded_access_token}"
            )

            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=True if IS_PRODUCTION else False,
                samesite="None" if IS_PRODUCTION else "Lax",
                max_age=60 * 60 * 24 * 30
            )

            return response
        
        # Create new user
        created_user = create_user(
            provider_id=provider_id,
            provider="github",
            email=primary_email,
            username=github_user.get("login"),
            display_name=github_user.get("name"),
            profile_pic=github_user.get("avatar_url")
        )

        if created_user['code'] != 201:
            return jsonify(created_user), created_user['code']
        
        user = created_user['data']

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        expires_at = datetime.now(UTC) + timedelta(days=30)

        save_result = save_refresh_token(
            user["id"],
            refresh_token,
            expires_at
        )

        if save_result["code"] != 200:
            return jsonify(save_result), save_result["code"]

        encoded_access_token = quote(access_token)

        response = redirect(
            f"{FRONTEND_URL}/auth/callback"
            f"?access_token={encoded_access_token}"
        )

        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=True if IS_PRODUCTION else False,
            samesite="None" if IS_PRODUCTION else "Lax",
            max_age=60 * 60 * 24 * 30
        )

        return response

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "code": 500,
            "message": f"Error generating github token: {str(e)}"
        }), 500