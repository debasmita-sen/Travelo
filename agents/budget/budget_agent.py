from tools.budget_tools import calculate_budget  # import function to compute budget estimates


class BudgetAgent:  # agent that calculates trip budget details
    name = "budget_agent"  # identifier for this agent

    def run(self, trip):  # run the budget calculation for a trip object
        budget = calculate_budget(  # call helper with trip details
            trip.destination,
            trip.days,
            trip.travelers,
            trip.budget,
            trip.budget_input_amount,
            trip.budget_input_currency,
            trip.budget_local_amount,
            trip.budget_local_currency,
        )
        return {"agent": self.name, "budget": budget}  # return result in a simple dict
