import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # load environment variables from a .env file when present

# Base paths and runtime options
BASE_DIR = Path(__file__).resolve().parent  # project root folder
# SQLite path used by the history store; override with env var in production
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "database" / "smarttrip.db"))
# Flask secret key (keep secret in production)
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
# Network timeout for external API calls (seconds)
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))
# Maximum days the app will plan for in an itinerary
MAX_TRIP_DAYS = int(os.getenv("MAX_TRIP_DAYS", "14"))
# Defensive limit for total characters sent to LLM providers
MAX_LLM_MESSAGE_CHARS = int(os.getenv("MAX_LLM_MESSAGE_CHARS", "12000"))

# --- LLM provider configuration ---
# Choose between 'groq' (ChatGroq) or 'gemini' (Google Gemini API)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# --- Attraction / map services ---
# Overpass/OpenStreetMap endpoints (no API key typically required)
OVERPASS_API_URL = os.getenv("OVERPASS_API_URL", "https://overpass-api.de/api/interpreter")
NOMINATIM_API_URL = os.getenv("NOMINATIM_API_URL", "https://nominatim.openstreetmap.org/search")
# User-Agent string included in requests to Nominatim/Overpass
APP_USER_AGENT = os.getenv("APP_USER_AGENT", "Travelo/1.0")

# --- Weather service ---
# WeatherAPI key and endpoint for current/forecast lookups
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://api.weatherapi.com/v1/current.json")

# Optional keyed geocoding endpoint that some weather providers expose
WEATHER_GEOCODING_API_URL = os.getenv("WEATHER_GEOCODING_API_URL", "")
WEATHER_GEOCODING_API_KEY = os.getenv("WEATHER_GEOCODING_API_KEY", "")

# --- Routing ---
# OpenRouteService API key and directions endpoint
OPENROUTESERVICE_API_KEY = os.getenv("OPENROUTESERVICE_API_KEY", "")
OPENROUTESERVICE_DIRECTIONS_URL = os.getenv(
    "OPENROUTESERVICE_DIRECTIONS_URL",
    "https://api.openrouteservice.org/v2/directions/foot-walking",
)

# --- News ---
# NewsData.io API key and URL for travel-related headlines
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY", "")
NEWSDATA_API_URL = os.getenv("NEWSDATA_API_URL", "https://newsdata.io/api/1/news")
