from services.gemini_service import LLMService
from services.data_loader import load_json


class ItineraryAgent:
    name = "itinerary_agent"

    def __init__(self):
        self.llm = LLMService()

    def run(self, trip, context):
        attractions = context.get("attractions", [])
        weather = context.get("weather", [])
        crowds = context.get("crowds", [])
        budget = context.get("budget", {})
        costs = load_json("city_costs.json", {})
        city_cost = costs.get(trip.destination.strip().lower(), costs.get("default", {}))
        default_activity_cost = city_cost.get("activity_average", 20)
        days = []
        for index in range(trip.days):
            attraction = attractions[index % len(attractions)] if attractions else {"name": "Local exploration", "description": "Explore at an easy pace.", "cost": 0, "source": "local_fallback"}
            weather_day = weather[index] if index < len(weather) else {"condition": "mild", "tip": "Keep plans flexible."}
            crowd_day = crowds[index] if index < len(crowds) else {"level": "moderate"}
            estimated_cost, cost_note = self._estimate_activity_cost(attraction, default_activity_cost)
            days.append({
                "day": index + 1,
                "title": f"Day {index + 1}: {attraction['name']}",
                "weather": weather_day,
                "crowd_level": crowd_day.get("level", "moderate"),
                "activities": [
                    f"Start with {attraction['name']} ({attraction.get('best_time', 'morning')}).",
                    attraction.get("description", "Enjoy the local highlight."),
                    "Leave a recovery window for meals, transit, and spontaneous finds."
                ],
                "estimated_cost": estimated_cost,
                "cost_note": cost_note
            })

        local_summary = f"{trip.days}-day plan for {trip.travelers} traveler(s). Budget status: {budget.get('status', 'unknown')}."
        llm_summary = self.llm.generate([
            {"role": "system", "content": "You are SmartTripAI's itinerary agent. Write a short, practical itinerary summary using the provided structured plan."},
            {"role": "user", "content": f"Trip: {trip}\nBudget: {budget}\nDays: {days}"},
        ])
        if "not configured" in llm_summary:
            llm_summary = local_summary

        return {
            "agent": self.name,
            "itinerary": {
                "destination": trip.destination,
                "summary": llm_summary,
                "days": days,
                "llm_provider_note": "Itinerary Agent uses the same LLM configuration as the Manager Agent.",
            }
        }

    def _estimate_activity_cost(self, attraction, default_activity_cost):
        if "estimated_cost" in attraction:
            return attraction["estimated_cost"], "Estimated activity cost."

        cost = attraction.get("cost")
        if cost is None:
            return default_activity_cost, "Estimated from average local activity cost."

        if cost > 0:
            return cost, "Known or typical attraction cost."

        if attraction.get("source") == "openstreetmap_overpass":
            return default_activity_cost, "Price unavailable from map data, using local average."

        return 0, "Free or low-cost activity."
