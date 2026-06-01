from datetime import date, timedelta
import re

from flask import Blueprint, jsonify, request

from agents.general_chat_agent import GeneralChatAgent
from agents.manager.orchestrator import SmartTripOrchestrator
from models.trip import TripRequest
from services.currency_service import parse_budget_text, parse_budget_value

api_bp = Blueprint("api", __name__)


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _trip_from_fields(
    destination,
    start_date,
    end_date,
    travelers,
    budget_info,
    interests,
    origin="",
):
    return TripRequest(
        destination,
        start_date,
        end_date,
        travelers,
        budget_info["amount"],
        interests,
        origin,
        budget_info["input_amount"],
        budget_info["input_currency"],
        budget_info["local_amount"],
        budget_info["local_currency"],
    )


def _extract_destination(message: str) -> str:
    patterns = [
        r"(?:famous|popular|best|local|traditional)?\s*(?:foods?|drinks?|cuisine|dishes?)\s+(?:in|of|from)\s+([A-Za-z\s,]+?)(?:\s+for|\s+on|\s+with|\?|\.|$)",
        r"(?:trip|travel|itinerary|plan|visit)\s+(?:to|for)\s+([A-Za-z\s,]+?)(?:\s+from|\s+for|\s+on|\s+with|\s+under|\s+budget|\.|$)",
        r"(?:trip|travel|itinerary|plan|visit)\s+([A-Za-z\s,]+?)(?:\s+under|\s+within|\s+budget|\.|$)",
        r"(?:to|in)\s+([A-Za-z\s,]+?)(?:\s+from|\s+for|\s+on|\s+with|\s+under|\s+budget|\.|$)",
        r"^([A-Za-z\s,]+?)\s+(?:₹|rs\.?|inr|\$|usd|eur|€|gbp|£|jpy|¥)?\s*\d+(?:,\d+)*(?:\.\d+)?\s*(?:k|lakh|lakhs|lac|lacs)?(?:\s|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).strip(" ,.")
    return "Paris"


def _extract_trip(payload):
    message = payload.get("message", "")
    today = date.today()
    default_start = today + timedelta(days=30)
    default_end = default_start + timedelta(days=2)

    destination = payload.get("destination") or _extract_destination(message)
    start_date = payload.get("start_date") or default_start.isoformat()
    end_date = payload.get("end_date") or default_end.isoformat()
    travelers = _safe_int(payload.get("travelers"), 1)
    budget_info = parse_budget_value(payload.get("budget"), destination) if payload.get("budget") else parse_budget_text(message, destination)
    interests = payload.get("interests") or "culture, food, landmarks"
    origin = payload.get("origin") or ""

    traveler_match = re.search(r"(\d+)\s*(?:people|persons|travelers|travellers|friends|adults)", message, re.IGNORECASE)
    if traveler_match and not payload.get("travelers"):
        travelers = _safe_int(traveler_match.group(1), travelers)

    budget_match = re.search(r"(?:budget|under|within)\s*[$???]?\s*(\d+(?:\.\d+)?)", message, re.IGNORECASE)
    if budget_match and not payload.get("budget"):
        budget_info = parse_budget_text(message, destination)

    interest_match = re.search(r"(?:interests?|likes?|focus(?:ed)? on)\s*:?\s*([A-Za-z,\s]+)", message, re.IGNORECASE)
    if interest_match and not payload.get("interests"):
        interests = interest_match.group(1).strip(" .")

    food_terms = ("food", "foods", "drink", "drinks", "cuisine", "dish", "dishes", "eat")
    if any(term in message.lower() for term in food_terms) and "food" not in interests.lower():
        interests = f"{interests}, food"

    return _trip_from_fields(destination, start_date, end_date, travelers, budget_info, interests, origin)


def _should_use_trip_tools(payload) -> bool:
    message = payload.get("message", "")
    if any(payload.get(key) for key in ("destination", "interests", "origin")):
        return True

    tool_terms = (
        "plan",
        "trip",
        "travel",
        "itinerary",
        "visit",
        "route",
        "weather",
        "budget",
        "crowd",
        "hotel",
        "attraction",
        "tour",
        "vacation",
        "holiday",
    )
    money_terms = r"(?:₹|rs\.?|inr|\$|usd|eur|€|gbp|£|jpy|¥)?\s*\d+(?:,\d+)*(?:\.\d+)?\s*(?:k|lakh|lakhs|lac|lacs)\b"
    return (
        any(re.search(rf"\b{term}\b", message, re.IGNORECASE) for term in tool_terms)
        or bool(re.search(money_terms, message, re.IGNORECASE))
    )


@api_bp.post("/plan")
def api_plan():
    payload = request.get_json(force=True)
    destination = payload.get("destination", "")
    budget_info = parse_budget_value(payload.get("budget"), destination)
    trip = _trip_from_fields(
        destination=destination,
        start_date=payload.get("start_date", ""),
        end_date=payload.get("end_date", ""),
        travelers=int(payload.get("travelers", 1)),
        budget_info=budget_info,
        interests=payload.get("interests", ""),
        origin=payload.get("origin", ""),
    )
    return jsonify(SmartTripOrchestrator().plan(trip))


@api_bp.post("/chat")
def api_chat():
    payload = request.get_json(force=True)
    message = payload.get("message", "")
    if not _should_use_trip_tools(payload):
        return jsonify({
            "type": "chat",
            "answer": GeneralChatAgent().answer(message),
            "user_message": message,
        })

    trip = _extract_trip(payload)
    result = SmartTripOrchestrator().plan(trip, user_message=message)
    result["type"] = "travel_plan"
    result["user_message"] = message
    return jsonify(result)
