from agents.manager.orchestrator import SmartTripOrchestrator
from agents.manager.manager_agent import ManagerAgent
from agents.itinerary.itinerary_agent import ItineraryAgent
from models.trip import TripRequest
from services.langchain_manager_service import LangChainManagerService


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


class FakeTool:
    def __init__(self, name, calls):
        self.name = name
        self.calls = calls

    def invoke(self, args):
        self.calls.append((self.name, args))
        return "{}"


def test_langchain_manager_runs_required_project_tools():
    calls = []
    tools = [
        FakeTool("travel_attractions", calls),
        FakeTool("travel_weather", calls),
        FakeTool("travel_route", calls),
        FakeTool("travel_food", calls),
        FakeTool("travel_budget", calls),
        FakeTool("travel_news", calls),
    ]
    service = LangChainManagerService(chat_model=object(), tools=tools)
    trip = TripRequest("Goa", "2026-06-10", "2026-06-12", 2, 1500, "food", origin="Mumbai")

    result = service._run_required_tools(trip)

    assert set(result) == {
        "travel_attractions",
        "travel_weather",
        "travel_route",
        "travel_food",
        "travel_budget",
        "travel_news",
    }
    assert ("travel_attractions", {"destination": "Goa", "interests": "food"}) in calls
    assert ("travel_route", {"origin": "Mumbai", "destination": "Goa"}) in calls


def test_manager_prefers_langchain_summary_over_direct_groq():
    agent = ManagerAgent()
    agent.langchain_manager.generate_trip_brief = lambda *args, **kwargs: "langchain tool-aware summary"
    agent.llm.generate = lambda *args, **kwargs: "direct groq summary"
    trip = TripRequest("Goa", "2026-06-10", "2026-06-12", 2, 1500, "food")

    result = agent.synthesize(trip, {"user_question": "Plan Goa with food"})

    assert result["manager_summary"] == "langchain tool-aware summary"
