"""Tests for building web source citations from tool outputs.

Verifies that `collect_web_sources` produces reasonable link lists for
weather, news, routes, and OpenStreetMap attractions.
"""

from services.sources_service import collect_web_sources


def test_collect_web_sources_includes_news_links():
    context = {
        "news": [{"title": "Transit update", "url": "https://example.com/news/1", "source": "newsdata"}],
        "weather": [{"source": "weatherapi_current", "location_name": "Paris"}],
        "route": {"source": "openrouteservice", "origin": "CDG", "destination": "Paris"},
        "attractions": [{"name": "Louvre", "source": "openstreetmap_overpass"}],
        "food": {"foods": [{"name": "Croissant"}], "destination": "Paris"},
        "budget": {"status": "comfortable"},
    }
    sources = collect_web_sources(context, "Paris")
    urls = [item["url"] for item in sources if item.get("url")]
    assert "https://example.com/news/1" in urls
    assert any("weatherapi.com" in url for url in urls)
    assert any("openstreetmap.org" in url for url in urls)
