from services.crowd_service import estimate_crowds


class CrowdAgent:
    name = "crowd_agent"

    def run(self, trip, weather_context=None):
        weather = weather_context or []
        crowds = estimate_crowds(trip.destination, trip.start_date, trip.days, weather)
        return {"agent": self.name, "crowds": crowds}
