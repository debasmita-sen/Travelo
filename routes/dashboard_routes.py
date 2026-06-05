from flask import Blueprint, render_template, session  # flask helpers

dashboard_bp = Blueprint("dashboard", __name__)  # blueprint for dashboard views


@dashboard_bp.get("/dashboard")
def dashboard():
    plan = session.get("latest_plan")  # get last plan saved in session
    if not plan:
        return render_template("dashboard.html", plan=None)  # render empty dashboard
    return render_template("dashboard.html", plan=plan)  # render dashboard with plan


@dashboard_bp.get("/itinerary")
def itinerary():
    plan = session.get("latest_plan")  # show itinerary page for latest plan
    return render_template("itinerary.html", plan=plan)
