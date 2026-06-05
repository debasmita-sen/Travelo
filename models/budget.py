from dataclasses import dataclass  # simple container for budget parts


@dataclass
class BudgetBreakdown:  # breakdown of a trip budget into categories
    total_budget: float  # total amount available
    lodging: float  # estimated lodging cost
    food: float  # estimated food cost
    transport: float  # estimated transport cost
    activities: float  # estimated activities cost
    buffer: float  # leftover or buffer amount
