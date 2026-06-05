from datetime import date, timedelta
from typing import Dict, List

import requests

from config import REQUEST_TIMEOUT_SECONDS, WEATHER_API_KEY, WEATHER_API_URL


def _fallback_weather(destination: str, start_date: str, days: int, reason: str = "live weather unavailable") -> List[Dict]:
    patterns = {
        "goa": ["sunny", "humid", "chance of rain"],
        "london": ["cloudy", "light rain", "clear"],
        "tokyo": ["clear", "mild", "cloudy"],
        "paris": ["mild", "clear", "cloudy"],
        "new york": ["clear", "warm", "cloudy"],
    }
    city_pattern = patterns.get(destination.strip().lower(), ["clear", "cloudy", "mild"])
    try:
        start = date.fromisoformat(start_date)
    except ValueError:
        start = date.today()

    return [
        {
            "date": (start + timedelta(days=index)).isoformat(),
            "condition": city_pattern[index % len(city_pattern)],
            "high_c": 24 + (index % 5),
            "low_c": 16 + (index % 4),
            "tip": "Keep a flexible indoor backup." if "rain" in city_pattern[index % len(city_pattern)] else "Good for outdoor exploring.",
            "source": "local_fallback",
            "fallback_reason": reason,
        }
        for index in range(days)
    ]


def _weather_tip(condition: str) -> str:
    lowered = condition.lower()
    if any(term in lowered for term in ["rain", "drizzle", "thunder", "storm", "snow"]):
        return "Keep a flexible indoor backup."
    if any(term in lowered for term in ["mist", "fog", "haze"]):
        return "Allow extra time for visibility and transit delays."
    return "Good for outdoor exploring."


def forecast_weather(destination: str, start_date: str, days: int) -> List[Dict]:
    # If API key missing, return generated fallback weather
    if not WEATHER_API_KEY or WEATHER_API_KEY == "your_weatherapi_key_here":
        return _fallback_weather(destination, start_date, days, "WEATHER_API_KEY is not configured")

    try:
        response = requests.get(
            WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": destination, "aqi": "no"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
        current = payload["current"]
        location = payload.get("location", {})
        condition = current.get("condition", {}).get("text", "mixed")
        live_day = {
            "date": date.today().isoformat(),
            "condition": condition,
            "high_c": current.get("temp_c"),
            "low_c": current.get("temp_c"),
            "feelslike_c": current.get("feelslike_c"),
            "humidity": current.get("humidity"),
            "wind_kph": current.get("wind_kph"),
            "location_name": location.get("name", destination),
            "country": location.get("country"),
            "tip": _weather_tip(condition),
            "source": "weatherapi_current",
        }
        # Duplicate the live day to fill the requested number of days, adjusting dates
        return [dict(live_day, date=(date.today() + timedelta(days=index)).isoformat()) for index in range(days)]
    except (requests.RequestException, KeyError, TypeError, ValueError):
        # On any failure, return plausible local fallback forecasts
        return _fallback_weather(destination, start_date, days, "WeatherAPI request failed")
