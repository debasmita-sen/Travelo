from typing import Any, Dict, List
from urllib.parse import quote_plus

from config import (
    NEWSDATA_API_URL,
    NOMINATIM_API_URL,
    OPENROUTESERVICE_DIRECTIONS_URL,
    OVERPASS_API_URL,
    WEATHER_API_URL,
)


def _dedupe_sources(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique = []
    for item in sources:
        key = item.get("url") or item.get("label")
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def collect_web_sources(context: Dict[str, Any], destination: str = "") -> List[Dict[str, Any]]:
    """Build hyperlink citations from verified tool/API outputs in orchestrator context."""
    sources: List[Dict[str, Any]] = []
    dest = (destination or context.get("itinerary", {}).get("destination") or "").strip()

    weather = context.get("weather") or []
    if weather:
        sample = weather[0]
        source_key = sample.get("source", "")
        if source_key == "weatherapi_current":
            sources.append({
                "label": f"WeatherAPI — {sample.get('location_name') or dest or 'destination'}",
                "url": "https://www.weatherapi.com/",
                "kind": "weather",
                "note": "Live current conditions",
            })

    for article in (context.get("news") or [])[:6]:
        url = article.get("url")
        title = article.get("title") or "Travel news"
        if url:
            sources.append({
                "label": title,
                "url": url,
                "kind": "news",
                "note": article.get("source") or "newsdata",
            })

    route = context.get("route") or {}
    route_source = route.get("source", "")
    if route_source == "openrouteservice":
        sources.append({
            "label": f"Route guidance — {route.get('origin') or 'origin'} to {route.get('destination') or dest}",
            "url": "https://openrouteservice.org/",
            "kind": "route",
            "note": route.get("estimated_transfer_time") or "Walking route estimate",
        })

    for attraction in (context.get("attractions") or [])[:8]:
        # Only include attractions that came from the Overpass/OpenStreetMap tool
        if attraction.get("source") != "openstreetmap_overpass":
            continue
        name = attraction.get("name") or "attraction"
        query = quote_plus(f"{name} {dest}".strip())
        sources.append({
            "label": f"OpenStreetMap — {name}",
            "url": f"https://www.openstreetmap.org/search?query={query}",
            "kind": "attraction",
            "note": "Overpass tourism data",
        })
    return _dedupe_sources(sources)

GROQ_CHAT_DISCLAIMER = (
    "This reply uses the Groq language model without live web search. "
    "For verified weather, news links, routes, and attractions, turn Tools On and ask for a trip plan."
)
