from tools.budget_tools import calculate_budget


class BudgetAgent:
    name = "budget_agent"

    def run(self, trip):
        budget = calculate_budget(
            trip.destination,
            trip.days,
            trip.travelers,
            trip.budget,
            trip.budget_input_amount,
            trip.budget_input_currency,
            trip.budget_local_amount,
            trip.budget_local_currency,
        )
        return {"agent": self.name, "budget": budget}
