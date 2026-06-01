from dataclasses import dataclass


@dataclass
class BudgetBreakdown:
    total_budget: float
    lodging: float
    food: float
    transport: float
    activities: float
    buffer: float
