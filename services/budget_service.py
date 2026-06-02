from typing import Dict

from services.data_loader import load_json
from services.currency_service import convert_currency, destination_currency, format_conversion, format_currency


def estimate_budget(
    destination: str,
    days: int,
    travelers: int,
    total_budget: float,
    input_amount: float = None,
    input_currency: str = "INR",
    local_amount: float = None,
    local_currency: str = None,
) -> Dict:
    costs = load_json("city_costs.json", {})
    city_cost = costs.get(destination.strip().lower(), costs.get("default", {}))
    lodging = city_cost.get("daily_lodging", 90) * days
    food = city_cost.get("daily_food", 35) * days * travelers
    transport = city_cost.get("daily_transport", 14) * days * travelers
    activities = city_cost.get("activity_average", 20) * days * travelers
    expected_total = lodging + food + transport + activities
    buffer = max(total_budget - expected_total, 0)
    status = "comfortable" if total_budget >= expected_total else "tight"
    target_currency = local_currency or destination_currency(destination)
    converted_expected = convert_currency(expected_total, "USD", target_currency)
    converted_buffer = convert_currency(buffer, "USD", target_currency)
    converted_total = local_amount if local_amount is not None else convert_currency(total_budget, "USD", target_currency)
    converted_lodging = convert_currency(lodging, "USD", target_currency)
    converted_food = convert_currency(food, "USD", target_currency)
    converted_transport = convert_currency(transport, "USD", target_currency)
    converted_activities = convert_currency(activities, "USD", target_currency)
    original_amount = input_amount if input_amount is not None else total_budget
    input_display = format_currency(original_amount, input_currency)
    local_display = format_currency(converted_total, target_currency)
    return {
        "total_budget": round(total_budget, 2),
        "expected_total": round(expected_total, 2),
        "lodging": round(lodging, 2),
        "food": round(food, 2),
        "transport": round(transport, 2),
        "activities": round(activities, 2),
        "buffer": round(buffer, 2),
        "currency": "USD",
        "input_amount": round(original_amount, 2),
        "input_currency": input_currency,
        "input_display": input_display,
        "local_amount": round(converted_total, 2),
        "local_currency": target_currency,
        "local_display": local_display,
        "budget_display": format_conversion(original_amount, input_currency, converted_total, target_currency),
        "local_expected_total": round(converted_expected, 2),
        "local_expected_display": format_currency(converted_expected, target_currency),
        "local_lodging_display": format_currency(converted_lodging, target_currency),
        "local_food_display": format_currency(converted_food, target_currency),
        "local_transport_display": format_currency(converted_transport, target_currency),
        "local_activities_display": format_currency(converted_activities, target_currency),
        "local_buffer": round(converted_buffer, 2),
        "local_buffer_display": format_currency(converted_buffer, target_currency),
        "conversion_note": "All estimates are shown in destination currency. Conversion uses approximate static rates." if input_currency != target_currency else "All estimates are shown in the same currency as your input.",
        "status": status,
        "advice": "Budget looks workable." if status == "comfortable" else "Prioritize free attractions and simpler lodging."
    }
