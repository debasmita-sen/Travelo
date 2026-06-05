import requests
from typing import Optional, Tuple

from config import (
    APP_USER_AGENT,
    NOMINATIM_API_URL,
    REQUEST_TIMEOUT_SECONDS,
    WEATHER_GEOCODING_API_KEY,
    WEATHER_GEOCODING_API_URL,
)


LOCAL_COORDS = {}


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


def _query_nominatim(q: str) -> Optional[dict]:
    try:
        response = requests.get(
            NOMINATIM_API_URL,
            params={"q": q, "format": "json", "limit": 5},
            headers={"User-Agent": APP_USER_AGENT},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        results = response.json()
        if not results:
            return None
        # Prioritize non-buildings
        for res in results:
            if res.get("class") != "building" and res.get("type") not in ("residential", "house"):
                return res
        return results[0]
    except Exception:
        return None


def _geocode_with_nominatim(destination: str) -> Optional[Tuple[float, float]]:
    res = _query_nominatim(destination)
    if not res:
        return None

    # If the found place is a building or residential (often false positive for a town/city),
    # and it starts with s/sh, try alternative spelling (s <-> sh).
    if res.get("class") == "building" or res.get("type") in ("residential", "house"):
        alt_q = None
        dest_lower = destination.lower()
        if dest_lower.startswith("s") and not dest_lower.startswith("sh"):
            alt_q = "sh" + destination[1:]
        elif dest_lower.startswith("sh"):
            alt_q = "s" + destination[2:]

        if alt_q:
            alt_res = _query_nominatim(alt_q)
            if alt_res and not (alt_res.get("class") == "building" or alt_res.get("type") in ("residential", "house")):
                res = alt_res

    return float(res["lat"]), float(res["lon"])


def geocode_destination(destination: str) -> Optional[Tuple[float, float]]:
    key = destination.strip().lower()
    if key in LOCAL_COORDS:
        return LOCAL_COORDS[key]

    """Resolve a free-text destination into (lat, lon) using Nominatim.

    Returns None when the destination cannot be geocoded or on errors.
    """
    try:
        keyed_result = _geocode_with_keyed_provider(destination)
        if keyed_result:
            return keyed_result
    except requests.RequestException:
        pass

    try:
        res = _geocode_with_nominatim(destination)
        if res:
            return res

        # Try relaxing the query by dropping the last word if there are multiple words
        words = destination.strip().split()
        if len(words) > 1:
            relaxed = " ".join(words[:-1])
            res = _geocode_with_nominatim(relaxed)
            if res:
                return res
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        pass

    return None
