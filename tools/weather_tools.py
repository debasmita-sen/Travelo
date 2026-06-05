from services.weather_service import forecast_weather  # weather forecast service


def get_weather(destination: str, start_date: str, days: int):  # tool wrapper for weather
    return forecast_weather(destination, start_date, days)
