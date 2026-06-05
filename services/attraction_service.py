from typing import Dict, List  # type hints for functions

import requests  # HTTP library for live map data
from config import APP_USER_AGENT, OVERPASS_API_URL, REQUEST_TIMEOUT_SECONDS  # external API settings
from services.data_loader import load_json  # helper to load JSON files from data folder
from services.geocoding_service import geocode_destination  # helper to turn names into coords

ATTRACTION_LIBRARY = {  # small built-in attraction examples used as fallback
    "paris": [
        {"name": "Louvre Museum", "category": "art", "cost": 22, "best_time": "morning", "description": "World-class art and architecture.", "source": "local_fallback"},
        {"name": "Montmartre Walk", "category": "culture", "cost": 0, "best_time": "late afternoon", "description": "Village-like streets, cafes, and Sacre-Coeur views.", "source": "local_fallback"},
        {"name": "Seine River Cruise", "category": "relaxation", "cost": 18, "best_time": "evening", "description": "Gentle city overview from the water.", "source": "local_fallback"}
    ],
    "tokyo": [
        {"name": "Asakusa and Senso-ji", "category": "history", "cost": 0, "best_time": "morning", "description": "Classic temple district with street snacks.", "source": "local_fallback"},
        {"name": "Shibuya Crossing", "category": "city", "cost": 0, "best_time": "evening", "description": "Iconic neon city energy.", "source": "local_fallback"},
        {"name": "TeamLab Borderless", "category": "art", "cost": 28, "best_time": "afternoon", "description": "Immersive digital art experience.", "source": "local_fallback"}
    ],
    "new york": [
    {"name": "Central Park", "category": "nature", "cost": 0, "best_time": "morning", "description": "Green breathing room in Manhattan.", "source": "local_fallback"},
    {"name": "Metropolitan Museum of Art", "category": "art", "cost": 30, "best_time": "afternoon", "description": "Huge museum with global collections.", "source": "local_fallback"},
    {"name": "Brooklyn Bridge Walk", "category": "views", "cost": 0, "best_time": "sunset", "description": "Skyline views and a memorable walk.", "source": "local_fallback"}
    ],
    "default": [
        {"name": "Old Town Walk", "category": "culture", "cost": 0, "best_time": "morning", "description": "A low-pressure way to learn the city.", "source": "local_fallback"},
        {"name": "Local Food Market", "category": "food", "cost": 18, "best_time": "lunch", "description": "Taste regional dishes and snacks.", "source": "local_fallback"},
        {"name": "Signature Viewpoint", "category": "views", "cost": 8, "best_time": "sunset", "description": "A scenic stop to anchor the day.", "source": "local_fallback"}
    ]
}

def _fallback_attractions(destination: str, interests: str = "") -> List[Dict]:
    key = destination.strip().lower()  # normalize destination name for lookup
    attractions = ATTRACTION_LIBRARY.get(key, ATTRACTION_LIBRARY["default"])  # pick city list or default
    metadata = load_json("city_metadata.json", {})  # extra metadata like themes
    themes = set(metadata.get(key, {}).get("themes", []))  # set of city themes
    requested = {item.strip().lower() for item in interests.split(",") if item.strip()}  # user interest tokens

    scored = []  # list of (score, attraction) tuples
    for attraction in attractions:
        score = 1  # base score
        if attraction["category"].lower() in requested:
            score += 2  # boost if user requested this category
        if attraction["category"].lower() in themes:
    return [item for _, item in sorted(scored, key=lambda pair: pair[0], reverse=True)]  # sort by score desc

def _overpass_attractions(latitude: float, longitude: float) -> List[Dict]:
    query = f"""
    [out:json][timeout:20];
    nwr["tourism"]["name"](around:7000,{latitude},{longitude});
    """  # Overpass QL query to find nearby tourism POIs
    response = requests.get(OVERPASS_API_URL, params={"data": query}, headers={"Accept": "application/json", "User-Agent": APP_USER_AGENT}, timeout=REQUEST_TIMEOUT_SECONDS)  # call Overpass API
    response.raise_for_status()  # raise on HTTP error
    elements = response.json().get("elements", [])  # extract result elements
    attractions = []
    seen = set()  # avoid duplicate names
    for element in elements:
        tags = element.get("tags", {})
        name = tags.get("name")
        if not name or name in seen:
            continue  # skip unnamed or duplicate
        seen.add(name)
        category = tags.get("tourism", "attraction")
        attractions.append({
            "name": name,
            "description": f"OpenStreetMap {category} near the destination.",
            "source": "openstreetmap_overpass",
        })
    return attractions[:8]  # limit to first 8 results

def find_attractions(destination: str, interests: str = "") -> List[Dict]:
    coords = geocode_destination(destination)  # try to get lat/lng for destination
    if coords:
        try:
            live_attractions = _overpass_attractions(*coords)  # attempt live query
            if live_attractions:
                return live_attractions  # prefer live data when available
    except requests.RequestException:
        pass  # network error: fall back to local list
    return _fallback_attractions(destination, interests)  # fallback curated list
from typing import Dict, List

import requests

from config import APP_USER_AGENT, OVERPASS_API_URL, REQUEST_TIMEOUT_SECONDS
from services.data_loader import load_json
from services.geocoding_service import geocode_destination


ATTRACTION_LIBRARY = {
    "paris": [
        {"name": "Louvre Museum", "category": "art", "cost": 22, "best_time": "morning", "description": "World-class art and architecture.", "source": "local_fallback"},
        {"name": "Montmartre Walk", "category": "culture", "cost": 0, "best_time": "late afternoon", "description": "Village-like streets, cafes, and Sacre-Coeur views.", "source": "local_fallback"},
        {"name": "Seine River Cruise", "category": "relaxation", "cost": 18, "best_time": "evening", "description": "Gentle city overview from the water.", "source": "local_fallback"}
    ],
    "tokyo": [
        {"name": "Asakusa and Senso-ji", "category": "history", "cost": 0, "best_time": "morning", "description": "Classic temple district with street snacks.", "source": "local_fallback"},
        {"name": "Shibuya Crossing", "category": "city", "cost": 0, "best_time": "evening", "description": "Iconic neon city energy.", "source": "local_fallback"},
        {"name": "TeamLab Borderless", "category": "art", "cost": 28, "best_time": "afternoon", "description": "Immersive digital art experience.", "source": "local_fallback"}
    ],
    "new york": [
        {"name": "Central Park", "category": "nature", "cost": 0, "best_time": "morning", "description": "Green breathing room in Manhattan.", "source": "local_fallback"},
        {"name": "Metropolitan Museum of Art", "category": "art", "cost": 30, "best_time": "afternoon", "description": "Huge museum with global collections.", "source": "local_fallback"},
        {"name": "Brooklyn Bridge Walk", "category": "views", "cost": 0, "best_time": "sunset", "description": "Skyline views and a memorable walk.", "source": "local_fallback"}
    ],
    "default": [
        {"name": "Old Town Walk", "category": "culture", "cost": 0, "best_time": "morning", "description": "A low-pressure way to learn the city.", "source": "local_fallback"},
        {"name": "Local Food Market", "category": "food", "cost": 18, "best_time": "lunch", "description": "Taste regional dishes and snacks.", "source": "local_fallback"},
        {"name": "Signature Viewpoint", "category": "views", "cost": 8, "best_time": "sunset", "description": "A scenic stop to anchor the day.", "source": "local_fallback"}
    ]
}


def _fallback_attractions(destination: str, interests: str = "") -> List[Dict]:
    key = destination.strip().lower()
    attractions = ATTRACTION_LIBRARY.get(key, ATTRACTION_LIBRARY["default"])
    metadata = load_json("city_metadata.json", {})
    themes = set(metadata.get(key, {}).get("themes", []))
    requested = {item.strip().lower() for item in interests.split(",") if item.strip()}

    scored = []
    for attraction in attractions:
        score = 1
        if attraction["category"].lower() in requested:
            score += 2
        if attraction["category"].lower() in themes:
            score += 1
        scored.append((score, attraction))
    return [item for _, item in sorted(scored, key=lambda pair: pair[0], reverse=True)]



def _overpass_attractions(latitude: float, longitude: float) -> List[Dict]:
    query = f"""
    [out:json][timeout:20];
    nwr["tourism"]["name"](around:7000,{latitude},{longitude});
    out center 20;
    """
    response = requests.get(OVERPASS_API_URL, params={"data": query}, headers={"Accept": "application/json", "User-Agent": APP_USER_AGENT}, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    elements = response.json().get("elements", [])
    attractions = []
    seen = set()
    for element in elements:
        tags = element.get("tags", {})
        name = tags.get("name")
        if not name or name in seen:
            continue
        seen.add(name)
        category = tags.get("tourism", "attraction")
        attractions.append({
            "name": name,
            "category": category,
            "cost": 0,
            "best_time": "morning",
            "description": f"OpenStreetMap {category} near the destination.",
            "source": "openstreetmap_overpass",
        })
    return attractions[:8]


def find_attractions(destination: str, interests: str = "") -> List[Dict]:
    coords = geocode_destination(destination)
    if coords:
        try:
            live_attractions = _overpass_attractions(*coords)
            if live_attractions:
                return live_attractions
        except requests.RequestException:
            pass
    return _fallback_attractions(destination, interests)







