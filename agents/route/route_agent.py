from tools.route_tools import get_route


class RouteAgent:
    name = "route_agent"

    def run(self, trip):
        route = get_route(trip.origin or "", trip.destination)
        return {"agent": self.name, "route": route}
