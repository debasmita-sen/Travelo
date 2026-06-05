from services.route_service import plan_route  # route planning service


def get_route(origin: str, destination: str):  # tool wrapper to compute route
    return plan_route(origin, destination)
