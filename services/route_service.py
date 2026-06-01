from typing import Dict, Optional, Tuple

import requests

from config import (
    OPENROUTESERVICE_API_KEY,
    OPENROUTESERVICE_DIRECTIONS_URL,
    REQUEST_TIMEOUT_SECONDS,
)
from services.geocoding_service import geocode_destination


def _fallback_route(origin: str, destination: str, reason: str) -> Dict:
    if not origin:
        origin = "your hotel"
    return {
        "origin": origin,
        "destination": destination,
        "recommended_mode": "public transport + walking",
        "estimated_transfer_time": "30-60 minutes inside the city",
        "distance_km": None,
        "duration_minutes": None,
        "source": "local_fallback",
        "fallback_reason": reason,
        "notes": [
            "Group nearby attractions by neighborhood.",
            "Start farther stops early, then drift back toward lodging."
        ]
    }


def plan_route(origin: str, destination: str) -> Dict:
    if not OPENROUTESERVICE_API_KEY or OPENROUTESERVICE_API_KEY == "your_openrouteservice_key_here":
        return _fallback_route(origin, destination, "OPENROUTESERVICE_API_KEY is not configured")

    start_coords = geocode_destination(origin) if origin else None
    end_coords = geocode_destination(destination)
    if not end_coords:
        return _fallback_route(origin, destination, "destination could not be geocoded")
    if not start_coords:
        return _fallback_route(origin, destination, "origin could not be geocoded")

    start_lat, start_lon = start_coords
    end_lat, end_lon = end_coords
    payload = {"coordinates": [[start_lon, start_lat], [end_lon, end_lat]]}

    try:
        response = requests.post(
            OPENROUTESERVICE_DIRECTIONS_URL,
            json=payload,
            headers={"Authorization": OPENROUTESERVICE_API_KEY, "Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        summary = response.json()["routes"][0]["summary"]
        return {
            "origin": origin,
            "destination": destination,
            "recommended_mode": "walking route from OpenRouteService",
            "estimated_transfer_time": f"{round(summary['duration'] / 60)} minutes",
            "distance_km": round(summary["distance"] / 1000, 2),
            "duration_minutes": round(summary["duration"] / 60, 1),
            "source": "openrouteservice",
            "notes": ["Live route estimate from OpenRouteService."]
        }
    except (requests.RequestException, KeyError, IndexError, TypeError):
        return _fallback_route(origin, destination, "OpenRouteService request failed")
