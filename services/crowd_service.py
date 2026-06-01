from datetime import date, timedelta
from typing import Dict, List

from services.data_loader import load_json


def estimate_crowds(destination: str, start_date: str, days: int, weather: List[Dict]) -> List[Dict]:
    holidays = load_json("holidays.json", {})
    rules = load_json("crowd_rules.json", {"weekend_multiplier": 1.25, "holiday_multiplier": 1.5})
    city_holidays = set(holidays.get(destination.strip().lower(), []))
    try:
        start = date.fromisoformat(start_date)
    except ValueError:
        start = date.today()

    results = []
    for index in range(days):
        current = start + timedelta(days=index)
        score = 1.0
        reasons = []
        if current.weekday() >= 5:
            score *= rules.get("weekend_multiplier", 1.25)
            reasons.append("weekend")
        if current.isoformat() in city_holidays:
            score *= rules.get("holiday_multiplier", 1.5)
            reasons.append("holiday")
        if index < len(weather) and "rain" in weather[index].get("condition", ""):
            score *= rules.get("rain_reduction", 0.85)
            reasons.append("rain may reduce outdoor crowds")
        level = "high" if score >= 1.45 else "moderate" if score >= 1.15 else "low"
        results.append({"date": current.isoformat(), "level": level, "reasons": reasons or ["normal demand"]})
    return results
