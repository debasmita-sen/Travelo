from dataclasses import dataclass  # convenient classes for simple data containers
from datetime import date  # date parsing and arithmetic
from typing import Optional  # optional type hints

from config import MAX_TRIP_DAYS  # maximum allowed trip days from config


@dataclass
class TripRequest:  # representation of a user's trip request
    destination: str  # destination name
    start_date: str  # ISO start date string
    end_date: str  # ISO end date string
    travelers: int  # number of travelers
    budget: float  # total budget in base currency
    interests: str  # comma-separated interests
    origin: Optional[str] = None  # optional origin location
    budget_input_amount: Optional[float] = None  # raw input amount if provided
    budget_input_currency: str = "INR"  # currency code for input
    budget_local_amount: Optional[float] = None  # optionally provided local converted amount
    budget_local_currency: str = "USD"  # currency of the local amount

    @property
    def days(self) -> int:  # compute trip days from start/end dates safely
        try:
            start = date.fromisoformat(self.start_date)
            end = date.fromisoformat(self.end_date)
            return min(max((end - start).days + 1, 1), MAX_TRIP_DAYS)  # at least 1 day, capped
        except ValueError:
            return 1  # fallback to one day if dates are invalid
