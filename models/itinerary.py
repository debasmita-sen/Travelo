from dataclasses import dataclass, field  # data class helpers
from typing import List  # type hints


@dataclass
class DayPlan:  # structured plan for a single day
    day: int  # day number in the trip
    title: str  # short title for the day
    activities: List[str] = field(default_factory=list)  # list of activity strings
    estimated_cost: float = 0.0  # estimated daily cost


@dataclass
class Itinerary:  # overall itinerary containing days and a summary
    destination: str  # trip destination name
    days: List[DayPlan] = field(default_factory=list)  # list of `DayPlan` objects
    summary: str = ""  # brief summary of the itinerary
