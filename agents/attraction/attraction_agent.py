from tools.attraction_tools import search_attractions  # import helper to find attractions


class AttractionAgent:  # agent that finds attractions for a trip
    name = "attraction_agent"  # simple name identifier for the agent

    def run(self, trip):  # run the agent given a `trip` object
        attractions = search_attractions(trip.destination, trip.interests)  # search by destination and interests
        return {"agent": self.name, "attractions": attractions}  # return a simple result dict
