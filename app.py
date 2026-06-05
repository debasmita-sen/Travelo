from flask import Flask  # import the Flask class to make the web app

from config import FLASK_SECRET_KEY, DATABASE_PATH  # get config values we need
from routes.api_routes import api_bp  # import API routes blueprint
from routes.dashboard_routes import dashboard_bp  # import dashboard blueprint
from routes.home_routes import home_bp  # import home page blueprint
from routes.planner_routes import planner_bp  # import planner blueprint
from services.history_service import clear_history  # import function to clear history data


def create_app():  # function that creates and configures the Flask app
    app = Flask(__name__)  # make a Flask app instance using this file's name
    app.secret_key = FLASK_SECRET_KEY  # set the secret key for sessions
    app.register_blueprint(home_bp)  # add the home page routes to the app
    app.register_blueprint(planner_bp)  # add the planner routes to the app
    app.register_blueprint(dashboard_bp)  # add the dashboard routes to the app
    app.register_blueprint(api_bp, url_prefix="/api")  # add API routes under /api
    
    # Clear history on each server restart
    with app.app_context():  # run code that needs app context (like DB access)
        clear_history()  # remove old history records when server starts
    
    return app  # return the configured Flask app


if __name__ == "__main__":  # if this file is run directly
    create_app().run(debug=True)  # create the app and start the dev server
