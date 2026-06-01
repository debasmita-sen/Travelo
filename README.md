# Travelo

Travelo is an agentic travel planning demo. A Groq/Gemini manager coordinates specialist agents for attractions, budget, weather, news, routing, crowd levels, and itinerary generation.

## Agent Providers

| Agent | Provider | API key needed? | `.env` variables |
| --- | --- | --- | --- |
| Manager Agent | Groq or Gemini | Yes | `LLM_PROVIDER`, `GROQ_API_KEY`, `GEMINI_API_KEY` |
| Attraction Agent | OpenStreetMap / Overpass | No | `OVERPASS_API_URL`, `NOMINATIM_API_URL` |
| Budget Agent | Local JSON / database | No | None required |
| Weather Agent | WeatherAPI current weather | Yes | `WEATHER_API_KEY`, `WEATHER_API_URL` |
| Weather geocoding | Reserved slot for future keyed geocoder | Optional | `WEATHER_GEOCODING_API_URL`, `WEATHER_GEOCODING_API_KEY` |
| Route Agent | OpenRouteService | Yes | `OPENROUTESERVICE_API_KEY` |
| News Agent | NewsData.io | Yes | `NEWSDATA_API_KEY`, `NEWSDATA_API_URL` |
| Crowd Agent | Uses outputs from weather/news/route/date rules | No | None required |
| Itinerary Agent | Uses Manager's LLM config | Same as manager | `LLM_PROVIDER`, `GROQ_API_KEY`, `GEMINI_API_KEY` |

## Flow

User -> `planner_routes.py` -> Manager Orchestrator -> Attraction Agent -> Budget Agent -> Weather Agent -> News Agent -> Route Agent -> Crowd Agent -> Itinerary Agent -> Dashboard

## Setup

1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your keys in `.env`.
4. Run the app: `python app.py`
5. Open `http://127.0.0.1:5000`

Missing or invalid keys do not crash the demo. The services fall back to local deterministic planning output where possible.
