from tools.weather_tools import get_weather


class WeatherAgent:
    name = "weather_agent"

    def run(self, trip):
        weather = get_weather(trip.destination, trip.start_date, trip.days)
        return {"agent": self.name, "weather": weather}
