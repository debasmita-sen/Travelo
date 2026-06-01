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
            "If the user asks about famous food, drinks, cuisine, markets, or what to try, "
            "answer that directly using the food context and include practical tasting tips."
        )
        user = f"Trip: {trip}\nSpecialist context: {prompt_context}"
        content = self.llm.generate([
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ])
        return {"agent": "manager_agent", "manager_summary": content}

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
