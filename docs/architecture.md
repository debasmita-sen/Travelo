# Architecture

Travelo uses a manager-led multi-agent pipeline. Tool modules provide small stable interfaces over services. Agents call tools, the orchestrator combines outputs, and the manager agent asks Groq or Gemini to synthesize a final dashboard summary.

## Components

- `routes/`: Flask HTTP and page routes.
- `agents/`: Manager and specialist agents.
- `tools/`: Agent-callable wrappers.
- `services/`: Provider clients, deterministic fallbacks, and planning logic.
- `data/`: Local planning datasets.
- `templates/` and `static/`: Dashboard UI.

## Provider Map

- Attraction: OpenStreetMap / Overpass, no key.
- Budget: local JSON/database, no key.
- Weather: WeatherAPI current weather, key required.
- Weather geocoding: optional slot for future keyed geocoder.
- Route: OpenRouteService, key required for live routing.
- News: NewsData.io, key required for live news.
- Crowd: derived from other agent outputs and local rules.
- Itinerary: uses the same LLM service as the manager.
