from typing import Dict, List

import requests

from config import NEWSDATA_API_KEY, NEWSDATA_API_URL, REQUEST_TIMEOUT_SECONDS


def _fallback_news(destination: str, reason: str) -> List[Dict]:
    return [
        {
            "title": f"Travel advisory snapshot for {destination}",
            "summary": f"Live news is unavailable: {reason}.",
            "severity": "info",
            "source": "local_fallback",
        },
        {
            "title": "Check official local updates before departure",
            "summary": "Confirm transit strikes, attraction closures, weather disruption, and entry rules close to the travel date.",
            "severity": "medium",
            "source": "local_fallback",
        }
    ]


def get_travel_news(destination: str) -> List[Dict]:
    if not NEWSDATA_API_KEY or NEWSDATA_API_KEY == "your_newsdata_key_here":
        return _fallback_news(destination, "NEWSDATA_API_KEY is not configured")

    try:
        response = requests.get(
            NEWSDATA_API_URL,
            params={
                "apikey": NEWSDATA_API_KEY,
                "q": destination,
                "language": "en",
                "size": 5,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") == "error":
            return _fallback_news(destination, payload.get("results", {}).get("message", "NewsData.io returned an error"))
        articles = [
            {
                "title": article.get("title", "Untitled"),
                "summary": article.get("description") or article.get("content") or "No summary provided.",
                "url": article.get("link"),
                "published_at": article.get("pubDate"),
                "severity": "info",
                "source": "newsdata",
            }
            for article in payload.get("results", [])
        ]
        return articles or _fallback_news(destination, "no articles returned")
    except (requests.RequestException, TypeError, ValueError):
        return _fallback_news(destination, "NewsData.io request failed")
