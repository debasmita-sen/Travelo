import json
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from config import GROQ_API_KEY, GROQ_MODEL, MAX_LLM_MESSAGE_CHARS
from tools.attraction_tools import search_attractions
from tools.budget_tools import calculate_budget
from tools.food_tools import get_food_and_drink
from tools.news_tools import get_news
from tools.route_tools import get_route
from tools.weather_tools import get_weather


class AttractionToolInput(BaseModel):
    destination: str = Field(..., description="Destination city or place to search.")
    interests: str = Field("", description="Comma-separated traveler interests such as art, food, beaches, or history.")


class WeatherToolInput(BaseModel):
    destination: str = Field(..., description="Destination city or place for the weather forecast.")
    start_date: str = Field(..., description="Trip start date in YYYY-MM-DD format.")
    days: int = Field(..., ge=1, le=14, description="Number of travel days to forecast.")


class RouteToolInput(BaseModel):
    origin: str = Field("", description="Trip origin. Empty string is allowed when the traveler did not provide one.")
    destination: str = Field(..., description="Trip destination.")


class DestinationToolInput(BaseModel):
    destination: str = Field(..., description="Trip destination.")


class BudgetToolInput(BaseModel):
    destination: str = Field(..., description="Trip destination.")
    days: int = Field(..., ge=1, le=14, description="Number of travel days.")
    travelers: int = Field(..., ge=1, description="Number of travelers.")
    total_budget: float = Field(..., ge=0, description="Budget amount normalized for the app.")
    input_amount: Optional[float] = Field(None, ge=0, description="Original user-entered budget amount, if available.")
    input_currency: str = Field("INR", description="Currency code for the original user-entered budget.")
    local_amount: Optional[float] = Field(None, ge=0, description="Destination-local budget amount, if available.")
    local_currency: Optional[str] = Field("USD", description="Destination-local currency code, if available.")


class LangChainManagerService:
    """LangChain/Groq manager adapter that runs the same project tools."""

    def __init__(self, chat_model=None, tools: Optional[List[Any]] = None):
        self.unavailable_reason = ""
        self._imports = self._load_langchain_imports()
        self.tools = tools or self._build_tools()
        self.tools_by_name = {tool.name: tool for tool in self.tools}
        self.llm = chat_model or self._build_chat_model()

    def generate_trip_brief(self, trip, context: Dict[str, Any], system_prompt: str) -> str:
        if not self.llm:
            return self.unavailable_reason or "LangChain manager not configured."

        verified_tool_results = self._run_required_tools(trip)
        user_payload = self._fit_text(json.dumps({
            "original_user_message": context.get("user_question", ""),
            "trip": trip.__dict__,
            "orchestrator_context": self._compact_context(context),
            "verified_langchain_tool_results": verified_tool_results,
        }, default=str))

        messages = [
            self._imports["SystemMessage"](
                content=(
                    system_prompt
                    + "\nUse the verified_langchain_tool_results as primary evidence. "
                    + "They come from LangChain-bound project tools for weather, OpenStreetMap attractions, routes, food, budget, and news. "
                    + "Do not invent URLs, headlines, or live readings. If data is fallback or missing, say so clearly."
                )
            ),
            self._imports["HumanMessage"](content=user_payload),
        ]

        try:
            tool_bound_llm = self.llm.bind_tools(self.tools)
            first_response = tool_bound_llm.invoke(messages)
            tool_messages = self._execute_requested_tools(first_response)
            if tool_messages:
                final_messages = messages + [first_response] + tool_messages + [
                    self._imports["HumanMessage"](
                        content="Write the final manager travel brief now. Be concise and do not expose raw JSON."
                    )
                ]
                return self._content_from_message(self.llm.invoke(final_messages))
            return self._content_from_message(first_response)
        except Exception as exc:
            return f"LangChain manager failed: {exc}. Using deterministic local planning output."

    def _load_langchain_imports(self):
        try:
            from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
            from langchain_core.tools import tool
            from langchain_groq import ChatGroq
        except ImportError as exc:
            self.unavailable_reason = f"LangChain packages not installed: {exc}. Using deterministic local planning output."
            return {}
        return {
            "ChatGroq": ChatGroq,
            "HumanMessage": HumanMessage,
            "SystemMessage": SystemMessage,
            "ToolMessage": ToolMessage,
            "tool": tool,
        }

    def _build_chat_model(self):
        if not self._imports:
            return None
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_free_api_key_here":
            self.unavailable_reason = "Groq API key not configured. Using deterministic local planning output."
            return None
        return self._imports["ChatGroq"](
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=0.3,
            max_retries=1,
        )

    def _build_tools(self):
        if not self._imports:
            return []
        tool = self._imports["tool"]

        @tool(args_schema=AttractionToolInput)
        def travel_attractions(destination: str, interests: str = "") -> str:
            """Find destination attractions using the project's OpenStreetMap/Overpass-backed tool."""
            return self._to_json(search_attractions(destination, interests)[:8])

        @tool(args_schema=WeatherToolInput)
        def travel_weather(destination: str, start_date: str, days: int) -> str:
            """Fetch destination weather with the project's WeatherAPI-backed tool and local fallback."""
            return self._to_json(get_weather(destination, start_date, int(days))[:14])

        @tool(args_schema=RouteToolInput)
        def travel_route(origin: str, destination: str) -> str:
            """Plan route guidance with the project's OpenRouteService-backed route tool."""
            return self._to_json(get_route(origin or "", destination))

        @tool(args_schema=DestinationToolInput)
        def travel_food(destination: str) -> str:
            """Fetch local food and drink recommendations from the project's food tool."""
            return self._to_json(get_food_and_drink(destination))

        @tool(args_schema=BudgetToolInput)
        def travel_budget(
            destination: str,
            days: int,
            travelers: int,
            total_budget: float,
            input_amount: Optional[float] = None,
            input_currency: str = "INR",
            local_amount: Optional[float] = None,
            local_currency: Optional[str] = "USD",
        ) -> str:
            """Estimate budget using the project's budget tool and local city cost data."""
            return self._to_json(calculate_budget(
                destination,
                int(days),
                int(travelers),
                float(total_budget),
                input_amount,
                input_currency,
                local_amount,
                local_currency,
            ))

        @tool(args_schema=DestinationToolInput)
        def travel_news(destination: str) -> str:
            """Fetch travel-relevant news with the project's NewsData-backed tool and fallback."""
            return self._to_json(get_news(destination)[:5])

        return [
            travel_attractions,
            travel_weather,
            travel_route,
            travel_food,
            travel_budget,
            travel_news,
        ]

    def _run_required_tools(self, trip):
        required_calls = [
            ("travel_attractions", {"destination": trip.destination, "interests": trip.interests}),
            ("travel_weather", {"destination": trip.destination, "start_date": trip.start_date, "days": trip.days}),
            ("travel_route", {"origin": trip.origin or "", "destination": trip.destination}),
            ("travel_food", {"destination": trip.destination}),
            ("travel_budget", {
                "destination": trip.destination,
                "days": trip.days,
                "travelers": trip.travelers,
                "total_budget": trip.budget,
                "input_amount": trip.budget_input_amount,
                "input_currency": trip.budget_input_currency,
                "local_amount": trip.budget_local_amount,
                "local_currency": trip.budget_local_currency,
            }),
            ("travel_news", {"destination": trip.destination}),
        ]
        results = {}
        for name, args in required_calls:
            tool = self.tools_by_name.get(name)
            if not tool:
                continue
            try:
                results[name] = json.loads(tool.invoke(args))
            except Exception as exc:
                results[name] = {"error": str(exc)}
        return results

    def _execute_requested_tools(self, ai_message):
        tool_messages = []
        tool_calls = getattr(ai_message, "tool_calls", []) or []
        for tool_call in tool_calls:
            name = tool_call.get("name")
            tool = self.tools_by_name.get(name)
            if not tool:
                continue
            try:
                content = tool.invoke(tool_call.get("args", {}))
            except Exception as exc:
                content = self._to_json({"error": str(exc)})
            tool_messages.append(self._imports["ToolMessage"](content=content, tool_call_id=tool_call["id"]))
        return tool_messages

    def _compact_context(self, context):
        itinerary = context.get("itinerary", {})
        return {
            "user_question": context.get("user_question", ""),
            "attractions": context.get("attractions", [])[:5],
            "food": context.get("food", {}),
            "budget": context.get("budget", {}),
            "weather": context.get("weather", [])[:7],
            "news": context.get("news", [])[:3],
            "route": context.get("route", {}),
            "crowds": context.get("crowds", [])[:7],
            "itinerary": {
                "destination": itinerary.get("destination"),
                "summary": itinerary.get("summary"),
                "days": itinerary.get("days", [])[:7],
            },
        }

    def _fit_text(self, text: str) -> str:
        if len(text) <= MAX_LLM_MESSAGE_CHARS:
            return text
        return text[:MAX_LLM_MESSAGE_CHARS] + "\n[Context truncated to fit LLM payload limits.]"

    def _content_from_message(self, message) -> str:
        content = getattr(message, "content", message)
        if isinstance(content, list):
            return "\n".join(str(part.get("text", part)) if isinstance(part, dict) else str(part) for part in content)
        return str(content)

    def _to_json(self, value):
        return json.dumps(value, default=str)
