from services.food_service import suggest_food_and_drink


def get_food_and_drink(destination: str):
    return suggest_food_and_drink(destination)
