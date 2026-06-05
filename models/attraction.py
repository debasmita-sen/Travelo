from dataclasses import dataclass  # simple container decorator


@dataclass
class Attraction:  # data model for a single attraction or point of interest
    name: str  # name of the place
    category: str  # category like art, food, nature
    estimated_cost: float  # estimated cost to visit
    best_time: str  # best time of day to visit
    description: str  # short human-friendly description
