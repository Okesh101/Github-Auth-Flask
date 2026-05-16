# main.py

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from services.githubService import init_oauth
import os

load_dotenv()

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = FLASK_SECRET_KEY

    CORS(
        app,
        supports_credentials=True,
        origins=[FRONTEND_URL]
    )

    init_oauth(app)

    from routes.health import health_bp
    from routes.github import github_bp
    # from routes.auth import auth_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(github_bp)
    # app.register_blueprint(auth_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
