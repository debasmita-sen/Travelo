from flask import Blueprint, redirect, render_template, request, session, url_for

from agents.manager.orchestrator import SmartTripOrchestrator
from models.trip import TripRequest
from services.currency_service import parse_budget_value

planner_bp = Blueprint("planner", __name__)


@planner_bp.get("/planner")
def planner():
    return render_template("planner.html")


@planner_bp.post("/planner")
def create_plan():
    destination = request.form.get("destination", "")
    budget_info = parse_budget_value(request.form.get("budget", 0), destination)
    trip = TripRequest(
        destination=destination,
        start_date=request.form.get("start_date", ""),
        end_date=request.form.get("end_date", ""),
        travelers=int(request.form.get("travelers", 1)),
        budget=budget_info["amount"],
        interests=request.form.get("interests", ""),
        origin=request.form.get("origin", ""),
        budget_input_amount=budget_info["input_amount"],
        budget_input_currency=budget_info["input_currency"],
        budget_local_amount=budget_info["local_amount"],
        budget_local_currency=budget_info["local_currency"],
    )
    result = SmartTripOrchestrator().plan(trip)
    session["latest_plan"] = result
    return redirect(url_for("dashboard.dashboard"))
