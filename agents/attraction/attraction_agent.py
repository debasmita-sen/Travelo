from tools.attraction_tools import search_attractions


class AttractionAgent:
    name = "attraction_agent"

    def run(self, trip):
        attractions = search_attractions(trip.destination, trip.interests)
        return {"agent": self.name, "attractions": attractions}
