from dataclasses import dataclass
from datetime import date
from typing import Optional

from config import MAX_TRIP_DAYS


@dataclass
class TripRequest:
    destination: str
    start_date: str
    end_date: str
    travelers: int
    budget: float
    interests: str
    origin: Optional[str] = None
    budget_input_amount: Optional[float] = None
    budget_input_currency: str = "INR"
    budget_local_amount: Optional[float] = None
    budget_local_currency: str = "USD"

    @property
    def days(self) -> int:
        try:
            start = date.fromisoformat(self.start_date)
            end = date.fromisoformat(self.end_date)
            return min(max((end - start).days + 1, 1), MAX_TRIP_DAYS)
        except ValueError:
            return 1
