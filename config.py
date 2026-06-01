import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "database" / "smarttrip.db"))
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))
MAX_TRIP_DAYS = int(os.getenv("MAX_TRIP_DAYS", "14"))
MAX_LLM_MESSAGE_CHARS = int(os.getenv("MAX_LLM_MESSAGE_CHARS", "12000"))

# Manager and itinerary LLM. Use either Groq or Gemini-style configuration.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Attraction Agent: OpenStreetMap / Overpass, no API key required.
OVERPASS_API_URL = os.getenv("OVERPASS_API_URL", "https://overpass-api.de/api/interpreter")
NOMINATIM_API_URL = os.getenv("NOMINATIM_API_URL", "https://nominatim.openstreetmap.org/search")
APP_USER_AGENT = os.getenv("APP_USER_AGENT", "Travelo/1.0")

# Weather Agent: WeatherAPI current weather endpoint requires an API key.
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://api.weatherapi.com/v1/current.json")

# Optional geocoding slot for future weather/location providers.
WEATHER_GEOCODING_API_URL = os.getenv("WEATHER_GEOCODING_API_URL", "")
WEATHER_GEOCODING_API_KEY = os.getenv("WEATHER_GEOCODING_API_KEY", "")

# Route Agent: OpenRouteService requires an API key.
OPENROUTESERVICE_API_KEY = os.getenv("OPENROUTESERVICE_API_KEY", "")
OPENROUTESERVICE_DIRECTIONS_URL = os.getenv(
    "OPENROUTESERVICE_DIRECTIONS_URL",
    "https://api.openrouteservice.org/v2/directions/foot-walking",
)

# News Agent: NewsData.io requires an API key for live data.
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY", "")
NEWSDATA_API_URL = os.getenv("NEWSDATA_API_URL", "https://newsdata.io/api/1/news")
