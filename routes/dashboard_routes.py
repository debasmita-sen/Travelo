from flask import Blueprint, render_template, session

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/dashboard")
def dashboard():
    plan = session.get("latest_plan")
    if not plan:
        return render_template("dashboard.html", plan=None)
    return render_template("dashboard.html", plan=plan)


@dashboard_bp.get("/itinerary")
def itinerary():
    plan = session.get("latest_plan")
    return render_template("itinerary.html", plan=plan)
