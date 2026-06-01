from services.weather_service import forecast_weather


def test_weather_service_days():
    assert len(forecast_weather("Goa", "2026-06-01", 4)) == 4
