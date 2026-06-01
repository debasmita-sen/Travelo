from services.news_service import get_travel_news


def get_news(destination: str):
    return get_travel_news(destination)
