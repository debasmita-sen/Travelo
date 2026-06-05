from services.news_service import get_travel_news  # service for travel-related news


def get_news(destination: str):  # tool wrapper to fetch news for a destination
    return get_travel_news(destination)
