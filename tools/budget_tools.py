from services.budget_service import estimate_budget  # budget calculation service


def calculate_budget(
    destination: str,
    days: int,
    travelers: int,
    total_budget: float,
    input_amount: float = None,
    input_currency: str = "INR",
    local_amount: float = None,
    local_currency: str = None,
):
    return estimate_budget(
        destination,
        days,
        travelers,
        total_budget,
        input_amount,
        input_currency,
        local_amount,
        local_currency,
    )
