from tools.food_tools import get_food_and_drink  # import helper for local food suggestions


class FoodAgent:  # agent that finds food and drink suggestions
    name = "food_agent"  # identifier for this agent

    def run(self, trip):  # run the agent for a trip
        food = get_food_and_drink(trip.destination)  # fetch food and drink info for destination
        return {"agent": self.name, "food": food}  # return the info in a dict
