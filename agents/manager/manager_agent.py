from services.gemini_service import GroqService


class ManagerAgent:
    """Groq-backed manager that turns tool results into a concise trip brief."""

    def __init__(self):
        self.llm = GroqService()

    def synthesize(self, trip, context):
        prompt_context = self._build_prompt_context(context)
        system = (
            "You are SmartTripAI's manager agent. Summarize specialist tool outputs "
            "into practical travel guidance. Be specific, honest about data limits, and concise. "
            "Always answer every part of the user's message. If they ask for a tool-based plan "
            "and also ask a side question about the destination, include both: first a short "
            "travel plan summary, then a section named 'Side answer' that directly answers the "
            "extra question using your general travel knowledge and available context. "
            "Do not use markdown bold formatting or double asterisks. "
            "If the user asks about famous food, drinks, cuisine, markets, or what to try, "
            "answer that directly using the food context, including what it is, where to try it, "
            "and a practical tasting tip."
        )
        user = f"Original user message: {context.get('user_question', '')}\nTrip: {trip}\nSpecialist context: {prompt_context}"
        content = self.llm.generate([
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ])
        if "not configured" in content:
            content = self._local_summary(trip, context)
        return {"agent": "manager_agent", "manager_summary": content}

    def _local_summary(self, trip, context):
        budget = context.get("budget", {})
        itinerary = context.get("itinerary", {})
        food = context.get("food", {})
        attractions = context.get("attractions", [])
        weather = context.get("weather", [])
        route = context.get("route", {})

        highlights = [item.get("name") for item in attractions[:3] if item.get("name")]
        food_items = food.get("foods", [])[:3]
        drink_items = food.get("drinks", [])[:2]
        food_names = [item.get("name") for item in food_items[:2] if item.get("name")]
        drink_names = [item.get("name") for item in drink_items[:1] if item.get("name")]
        weather_note = weather[0].get("condition") if weather else "mixed"

        return "\n".join([
            f"Structured {trip.days}-day travel plan for {trip.destination}.",
            f"Budget status: {budget.get('status', 'review')} with expected total {budget.get('local_expected_display') or budget.get('expected_total', 'unknown')}.",
            f"Top stops: {', '.join(highlights) if highlights else 'local highlights and flexible exploration'}.",
            f"Food and drinks to try: {self._format_food_details(food_items, drink_items)}",
            f"Weather starts {weather_note}; keep backup indoor options where needed.",
            f"Route guidance: {route.get('recommended_mode', 'public transport + walking')}.",
            self._local_side_answer(trip, context, food_items, drink_items),
            itinerary.get("summary", "Use the day-by-day plan below for practical timing."),
        ])

    def _local_side_answer(self, trip, context, food_items, drink_items):
        question = context.get("user_question", "").lower()
        if not question:
            return "Side answer: No separate side question was detected."

        if any(term in question for term in ("food", "foods", "drink", "drinks", "cuisine", "dish", "eat")):
            return f"Side answer: For {trip.destination}, {self._format_food_details(food_items, drink_items)}"

        if any(term in question for term in ("famous", "known for", "special", "culture")):
            attractions = [item.get("name") for item in context.get("attractions", [])[:2] if item.get("name")]
            return f"Side answer: {trip.destination} is worth exploring for {', '.join(attractions) if attractions else 'its local culture, food, markets, and landmark areas'}."

        return "Side answer: The extra question is included in the plan context; use the sections below for the practical details."

    def _format_food_details(self, food_items, drink_items):
        items = food_items + drink_items
        if not items:
            return "try regional foods, local drinks, busy markets, and well-reviewed family restaurants."

        details = []
        for item in items:
            name = item.get("name")
            if not name:
                continue
            why = item.get("why_try", "It is a local specialty.")
            where = item.get("where_to_try")
            tip = item.get("tip")
            detail = f"{name}: {why}"
            if where:
                detail += f" Try it at {where}."
            if tip:
                detail += f" Tip: {tip}"
            details.append(detail)
        return " ".join(details)

    def _build_prompt_context(self, context):
        itinerary = context.get("itinerary", {})
        return {
            "user_question": context.get("user_question", ""),
            "attractions": context.get("attractions", [])[:5],
            "food": context.get("food", {}),
            "budget": context.get("budget", {}),
            "weather": context.get("weather", [])[:7],
            "news": [
                {
                    "title": item.get("title"),
                    "summary": item.get("summary"),
                    "severity": item.get("severity"),
                    "source": item.get("source"),
                }
                for item in context.get("news", [])[:3]
            ],
            "route": context.get("route", {}),
            "crowds": context.get("crowds", [])[:7],
            "itinerary": {
                "destination": itinerary.get("destination"),
                "summary": itinerary.get("summary"),
                "days": itinerary.get("days", [])[:7],
            },
        }
