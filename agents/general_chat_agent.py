from services.gemini_service import GroqService


class GeneralChatAgent:
    """Groq-backed fallback for questions that do not need travel tools."""

    def __init__(self):
        self.llm = GroqService()

    def answer(self, message: str) -> str:
        system = (
            "You are Travelo, a helpful chat assistant. Answer the user's question directly. "
            "Use clear, practical language. If the user asks about travel, food, drinks, culture, "
            "or places, provide useful suggestions without claiming live tool access."
        )
        return self.llm.generate(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            temperature=0.5,
        )
