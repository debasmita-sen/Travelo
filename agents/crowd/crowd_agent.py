from services.crowd_service import estimate_crowds  # import crowd estimation helper


class CrowdAgent:  # agent that estimates crowd levels
    name = "crowd_agent"  # identifier for this agent

    def run(self, trip, weather_context=None):  # run with optional weather context
        weather = weather_context or []  # use provided weather or empty list
        crowds = estimate_crowds(trip.destination, trip.start_date, trip.days, weather)  # estimate crowds
        return {"agent": self.name, "crowds": crowds}  # return results in a dict
