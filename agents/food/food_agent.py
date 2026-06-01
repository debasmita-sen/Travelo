from tools.food_tools import get_food_and_drink


class FoodAgent:
    name = "food_agent"

    def run(self, trip):
        food = get_food_and_drink(trip.destination)
        return {"agent": self.name, "food": food}
