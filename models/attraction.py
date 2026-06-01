from dataclasses import dataclass


@dataclass
class Attraction:
    name: str
    category: str
    estimated_cost: float
    best_time: str
    description: str
