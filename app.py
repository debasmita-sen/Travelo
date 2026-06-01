from flask import Flask

from config import FLASK_SECRET_KEY
from routes.api_routes import api_bp
from routes.dashboard_routes import dashboard_bp
from routes.home_routes import home_bp
from routes.planner_routes import planner_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = FLASK_SECRET_KEY
    app.register_blueprint(home_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
