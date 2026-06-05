from services.food_service import suggest_food_and_drink  # service that suggests local food


def get_food_and_drink(destination: str):  # tool wrapper for food suggestions
    return suggest_food_and_drink(destination)
