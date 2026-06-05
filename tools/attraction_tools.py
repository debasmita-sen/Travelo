from services.attraction_service import find_attractions  # service-level attraction finder


def search_attractions(destination: str, interests: str = ""):  # thin tool wrapper
    return find_attractions(destination, interests)
