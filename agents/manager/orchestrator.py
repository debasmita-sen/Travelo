from agents.attraction.attraction_agent import AttractionAgent
from agents.budget.budget_agent import BudgetAgent
from agents.crowd.crowd_agent import CrowdAgent
from agents.food.food_agent import FoodAgent
from agents.itinerary.itinerary_agent import ItineraryAgent
from agents.manager.manager_agent import ManagerAgent
from agents.news.news_agent import NewsAgent
from agents.route.route_agent import RouteAgent
from agents.weather.weather_agent import WeatherAgent
from models.trip import TripRequest


class SmartTripOrchestrator:
    """Runs the manager-led specialist pipeline for a trip request."""

    def __init__(self):
        self.attraction_agent = AttractionAgent()
        self.budget_agent = BudgetAgent()
        self.weather_agent = WeatherAgent()
        self.news_agent = NewsAgent()
        self.route_agent = RouteAgent()
        self.crowd_agent = CrowdAgent()
        self.food_agent = FoodAgent()
        self.itinerary_agent = ItineraryAgent()
        self.manager_agent = ManagerAgent()

    def plan(self, trip: TripRequest, user_message: str = ""):
        attraction_result = self.attraction_agent.run(trip)
        budget_result = self.budget_agent.run(trip)
        weather_result = self.weather_agent.run(trip)
        news_result = self.news_agent.run(trip)
        route_result = self.route_agent.run(trip)
        crowd_result = self.crowd_agent.run(trip, weather_result["weather"])
        food_result = self.food_agent.run(trip)

        context = {
            "user_question": user_message,
            "attractions": attraction_result["attractions"],
            "budget": budget_result["budget"],
            "weather": weather_result["weather"],
            "news": news_result["news"],
            "route": route_result["route"],
            "crowds": crowd_result["crowds"],
            "food": food_result["food"],
        }
        itinerary_result = self.itinerary_agent.run(trip, context)
        context["itinerary"] = itinerary_result["itinerary"]
        manager_result = self.manager_agent.synthesize(trip, context)

        return {
            "trip": trip.__dict__,
            "pipeline": [
                attraction_result,
                budget_result,
                weather_result,
                news_result,
                route_result,
                crowd_result,
                food_result,
                itinerary_result,
                manager_result,
            ],
            "context": context,
            "manager_summary": manager_result["manager_summary"],
        }
