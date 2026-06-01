from services.weather_service import forecast_weather


def get_weather(destination: str, start_date: str, days: int):
    return forecast_weather(destination, start_date, days)
