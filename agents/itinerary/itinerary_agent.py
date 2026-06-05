from services.gemini_service import LLMService  # import LLM wrapper service
from services.data_loader import load_json  # import helper to load JSON files


class ItineraryAgent:  # agent that builds a day-by-day itinerary
    name = "itinerary_agent"  # identifier for this agent

    def __init__(self):  # set up the agent
        self.llm = LLMService()  # create an LLM service instance for summaries

    def run(self, trip, context):  # create an itinerary using trip and context data
        attractions = context.get("attractions", [])  # list of attractions to use
        weather = context.get("weather", [])  # weather info per day
        crowds = context.get("crowds", [])  # crowd estimates per day
        budget = context.get("budget", {})  # budget info
        costs = load_json("city_costs.json", {})  # load city cost data from assets
        city_cost = costs.get(trip.destination.strip().lower(), costs.get("default", {}))  # find city-specific costs
        default_activity_cost = city_cost.get("activity_average", 20)  # fallback activity cost
        days = []  # will hold each day's plan
        for index in range(trip.days):  # build plan for each day
            attraction = attractions[index % len(attractions)] if attractions else {"name": "Local exploration", "description": "Explore at an easy pace.", "cost": 0, "source": "local_fallback"}  # pick an attraction or fallback
            weather_day = weather[index] if index < len(weather) else {"condition": "mild", "tip": "Keep plans flexible."}  # pick weather or default
            crowd_day = crowds[index] if index < len(crowds) else {"level": "moderate"}  # pick crowd level or default
            estimated_cost, cost_note = self._estimate_activity_cost(attraction, default_activity_cost)  # estimate activity cost
            days.append({  # append a structured day plan
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

        local_summary = f"{trip.days}-day plan for {trip.travelers} traveler(s). Budget status: {budget.get('status', 'unknown')}."  # quick fallback summary
        llm_summary = self.llm.generate([  # ask the LLM to write a short summary
            {"role": "system", "content": "You are SmartTripAI's itinerary agent. Write a short, practical itinerary summary using the provided structured plan."},
            {"role": "user", "content": f"Trip: {trip}\nBudget: {budget}\nDays: {days}"},
        ])
        if "not configured" in llm_summary:  # if LLM isn't available, use local summary
            llm_summary = local_summary

        return {  # return the itinerary structured output
            "agent": self.name,
            "itinerary": {
                "destination": trip.destination,
                "summary": llm_summary,
                "days": days,
                "llm_provider_note": "Itinerary Agent uses the same LLM configuration as the Manager Agent.",
            }
        }

    def _estimate_activity_cost(self, attraction, default_activity_cost):  # helper to estimate cost for one attraction
        if "estimated_cost" in attraction:
            return attraction["estimated_cost"], "Estimated activity cost."  # return provided estimate

        cost = attraction.get("cost")  # check for explicit cost
        if cost is None:
            return default_activity_cost, "Estimated from average local activity cost."  # fallback to city average

        if cost > 0:
            return cost, "Known or typical attraction cost."  # known positive cost

        if attraction.get("source") == "openstreetmap_overpass":
            return default_activity_cost, "Price unavailable from map data, using local average."  # maps don't include price info

        return 0, "Free or low-cost activity."  # otherwise assume free or very cheap
