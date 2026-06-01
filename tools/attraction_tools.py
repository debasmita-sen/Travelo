from services.attraction_service import find_attractions


def search_attractions(destination: str, interests: str = ""):
    return find_attractions(destination, interests)
