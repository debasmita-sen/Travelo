from agents.manager.orchestrator import SmartTripOrchestrator
from agents.itinerary.itinerary_agent import ItineraryAgent
from models.trip import TripRequest


def test_orchestrator_returns_itinerary():
    trip = TripRequest("Paris", "2026-06-10", "2026-06-12", 2, 1500, "art, food")
    result = SmartTripOrchestrator().plan(trip)
    assert result["context"]["itinerary"]["destination"] == "Paris"
    assert len(result["context"]["itinerary"]["days"]) == 3


def test_orchestrator_returns_food_suggestions():
    trip = TripRequest("Goa", "2026-06-10", "2026-06-12", 2, 1500, "food")
    result = SmartTripOrchestrator().plan(trip, user_message="What famous food and drinks in Goa?")
    assert result["context"]["user_question"] == "What famous food and drinks in Goa?"
    assert result["context"]["food"]["foods"]
    assert result["context"]["food"]["drinks"]


def test_itinerary_uses_average_for_unknown_live_attraction_cost():
    trip = TripRequest("Goa", "2026-06-10", "2026-06-10", 2, 1500, "beaches")
    agent = ItineraryAgent()
    agent.llm.generate = lambda *args, **kwargs: "summary"
    result = agent.run(trip, {
        "attractions": [{
            "name": "Map Attraction",
            "description": "Found from map data.",
            "cost": 0,
            "source": "openstreetmap_overpass",
        }],
        "budget": {"status": "comfortable"},
    })
    day = result["itinerary"]["days"][0]
    assert day["estimated_cost"] > 0
    assert "Price unavailable" in day["cost_note"]
