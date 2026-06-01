from dataclasses import dataclass, field
from typing import List


@dataclass
class DayPlan:
    day: int
    title: str
    activities: List[str] = field(default_factory=list)
    estimated_cost: float = 0.0


@dataclass
class Itinerary:
    destination: str
    days: List[DayPlan] = field(default_factory=list)
    summary: str = ""
