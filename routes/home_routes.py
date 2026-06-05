from flask import Blueprint, render_template  # flask view helpers

home_bp = Blueprint("home", __name__)  # blueprint for home page


@home_bp.get("/")
def home():
    return render_template("home.html")  # render the homepage template
