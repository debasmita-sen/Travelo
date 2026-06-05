"""Small unit tests for service utilities.

These focus on pure logic in services such as weather forecast shaping
and should pass even when external APIs are not configured (fallbacks).
"""

from services.weather_service import forecast_weather


def test_weather_service_days():
    assert len(forecast_weather("Goa", "2026-06-01", 4)) == 4
