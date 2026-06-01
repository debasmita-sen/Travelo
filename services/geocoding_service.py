import requests
from typing import Optional, Tuple

from config import (
    APP_USER_AGENT,
    NOMINATIM_API_URL,
    REQUEST_TIMEOUT_SECONDS,
    WEATHER_GEOCODING_API_KEY,
    WEATHER_GEOCODING_API_URL,
)


LOCAL_COORDS = {
    "paris": (48.8566, 2.3522),
    "tokyo": (35.6762, 139.6503),
    "new york": (40.7128, -74.0060),
    "london": (51.5072, -0.1276),
    "goa": (15.2993, 74.1240),
    "eiffel tower, paris": (48.8584, 2.2945),
    "louvre museum, paris": (48.8606, 2.3376),
}


def _geocode_with_keyed_provider(destination: str) -> Optional[Tuple[float, float]]:
    if not WEATHER_GEOCODING_API_URL:
        return None

    params = {"name": destination, "count": 1, "language": "en", "format": "json"}
    if WEATHER_GEOCODING_API_KEY:
        params["apikey"] = WEATHER_GEOCODING_API_KEY

    response = requests.get(
        WEATHER_GEOCODING_API_URL,
        params=params,
        headers={"User-Agent": APP_USER_AGENT},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results", [])
    if not results:
        return None
    return float(results[0]["latitude"]), float(results[0]["longitude"])


def _geocode_with_nominatim(destination: str) -> Optional[Tuple[float, float]]:
    response = requests.get(
        NOMINATIM_API_URL,
        params={"q": destination, "format": "json", "limit": 1},
        headers={"User-Agent": APP_USER_AGENT},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    results = response.json()
    if not results:
        return None
    return float(results[0]["lat"]), float(results[0]["lon"])


def geocode_destination(destination: str) -> Optional[Tuple[float, float]]:
    key = destination.strip().lower()
    if key in LOCAL_COORDS:
        return LOCAL_COORDS[key]

    try:
        keyed_result = _geocode_with_keyed_provider(destination)
        if keyed_result:
            return keyed_result
    except requests.RequestException:
        pass

    try:
        return _geocode_with_nominatim(destination)
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        return None
