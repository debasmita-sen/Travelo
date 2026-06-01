from routes.api_routes import _extract_trip, _should_use_trip_tools


def test_extract_trip_understands_food_question_destination():
    trip = _extract_trip({"message": "What famous food and drinks in Goa?"})
    assert trip.destination == "Goa"
    assert "food" in trip.interests


def test_general_question_skips_trip_tools_with_default_form_values():
    assert not _should_use_trip_tools({
        "message": "What are famous foods in Goa?",
        "start_date": "2026-06-30",
        "end_date": "2026-07-02",
        "travelers": "1",
        "budget": "1200",
    })


def test_trip_request_uses_tools():
    assert _should_use_trip_tools({"message": "Plan a 3 day trip to Goa"})


def test_short_destination_budget_uses_tools():
    trip = _extract_trip({"message": "goa 40k"})
    assert trip.destination == "goa"
    assert trip.budget_input_amount == 40000
    assert trip.budget_input_currency == "INR"
    assert trip.budget_local_currency == "INR"
    assert _should_use_trip_tools({"message": "goa 40k"})


def test_foreign_destination_budget_converts_inr_to_local_currency():
    trip = _extract_trip({"message": "paris 40k"})
    assert trip.destination == "paris"
    assert trip.budget_input_currency == "INR"
    assert trip.budget_local_currency == "EUR"
    assert trip.budget < trip.budget_input_amount


def test_explicit_usd_budget_stays_usd_input():
    trip = _extract_trip({"message": "Plan Tokyo under $500"})
    assert trip.budget_input_amount == 500
    assert trip.budget_input_currency == "USD"
    assert trip.budget_local_currency == "JPY"
