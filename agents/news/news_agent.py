from tools.news_tools import get_news


class NewsAgent:
    name = "news_agent"

    def run(self, trip):
        news = get_news(trip.destination)
        return {"agent": self.name, "news": news}
