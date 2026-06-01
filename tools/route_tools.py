from services.route_service import plan_route


def get_route(origin: str, destination: str):
    return plan_route(origin, destination)
