from services.gemini_service import GroqService


class GeneralChatAgent:
    """Groq-backed fallback for questions that do not need travel tools."""

    def __init__(self):
        self.llm = GroqService()

    def answer(self, message: str) -> str:
        system = (
            "You are Travelo, a helpful chat assistant. Answer the user's question directly. "
            "Use clear, practical language. If the user asks about travel, food, drinks, culture, "
            "or places, provide useful suggestions with enough detail to be useful: what it is, "
            "why it matters, where to try it, and any safety or budget tip if relevant. "
            "Do not use markdown bold formatting or double asterisks. "
            "You do not have live web search. Do not invent specific URLs, headlines, or live weather. "
            "If asked for current facts you cannot verify, say so and suggest turning Tools On for a trip plan."
        )
        answer = self.llm.generate(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            temperature=0.5,
        )
        if "not configured" in answer:
            return "Groq is not configured right now, so I can only use the app's built-in travel tools and deterministic fallback reports."
        return answer
