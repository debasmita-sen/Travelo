from datetime import date, timedelta  # date helpers
from typing import Dict, List  # type hints

from services.data_loader import load_json  # load static data files


def estimate_crowds(destination: str, start_date: str, days: int, weather: List[Dict]) -> List[Dict]:
    holidays = load_json("holidays.json", {})  # known holidays per city
    rules = load_json("crowd_rules.json", {"weekend_multiplier": 1.25, "holiday_multiplier": 1.5})  # simple scoring rules
    city_holidays = set(holidays.get(destination.strip().lower(), []))  # holidays for the destination
    try:
        start = date.fromisoformat(start_date)  # parse provided start date
    except ValueError:
        start = date.today()  # fallback to today if invalid

    results = []  # per-day crowd estimates
    for index in range(days):
        current = start + timedelta(days=index)  # date for this day
        score = 1.0  # base crowd score
        reasons = []  # why score changed
        if current.weekday() >= 5:  # weekend check
            score *= rules.get("weekend_multiplier", 1.25)
            reasons.append("weekend")
        if current.isoformat() in city_holidays:  # holiday check
            score *= rules.get("holiday_multiplier", 1.5)
            reasons.append("holiday")
        if index < len(weather) and "rain" in weather[index].get("condition", ""):  # rain reduces crowds outside
            score *= rules.get("rain_reduction", 0.85)
            reasons.append("rain may reduce outdoor crowds")
        level = "high" if score >= 1.45 else "moderate" if score >= 1.15 else "low"  # map score to label
        results.append({"date": current.isoformat(), "level": level, "reasons": reasons or ["normal demand"]})
    return results  # return list of estimates
