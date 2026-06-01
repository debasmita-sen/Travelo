from typing import Dict, List


FOOD_LIBRARY = {
    "goa": {
        "foods": [
            {"name": "Goan fish curry", "why_try": "Coconut, kokum, and local spices make it a coastal classic."},
            {"name": "Pork vindaloo", "why_try": "A bold, tangy Goan-Portuguese dish with vinegar and spice."},
            {"name": "Bebinca", "why_try": "Layered coconut dessert often served at celebrations."},
        ],
        "drinks": [
            {"name": "Feni", "why_try": "A famous local spirit made from cashew apple or coconut."},
            {"name": "Kokum juice", "why_try": "A refreshing sweet-sour local cooler."},
        ],
    },
    "paris": {
        "foods": [
            {"name": "Croissant", "why_try": "Buttery pastry best enjoyed fresh from a neighborhood boulangerie."},
            {"name": "Steak frites", "why_try": "A dependable bistro classic."},
            {"name": "Macarons", "why_try": "Colorful almond meringue sweets associated with Paris pâtisseries."},
        ],
        "drinks": [
            {"name": "Café crème", "why_try": "A simple café ritual for slow mornings."},
            {"name": "French wine", "why_try": "Easy to pair with bistro meals and cheese plates."},
        ],
    },
    "tokyo": {
        "foods": [
            {"name": "Sushi", "why_try": "Tokyo is famous for precise, high-quality sushi counters."},
            {"name": "Ramen", "why_try": "From shoyu to tonkotsu, it is a must-try comfort meal."},
            {"name": "Tempura", "why_try": "Light, crisp frying with seafood and seasonal vegetables."},
        ],
        "drinks": [
            {"name": "Matcha", "why_try": "A classic tea experience with sweets or desserts."},
            {"name": "Sake", "why_try": "A traditional rice drink served in many styles."},
        ],
    },
    "new york": {
        "foods": [
            {"name": "New York pizza", "why_try": "A foldable slice is an essential city snack."},
            {"name": "Bagel with schmear", "why_try": "A breakfast staple with deep local roots."},
            {"name": "Cheesecake", "why_try": "Dense, creamy, and strongly associated with the city."},
        ],
        "drinks": [
            {"name": "Egg cream", "why_try": "A classic soda-fountain drink despite having no egg or cream."},
            {"name": "Craft cocktails", "why_try": "New York has influential cocktail bars across many neighborhoods."},
        ],
    },
    "london": {
        "foods": [
            {"name": "Fish and chips", "why_try": "The classic casual British meal."},
            {"name": "Sunday roast", "why_try": "A hearty pub tradition with roast meat, potatoes, and gravy."},
            {"name": "Afternoon tea", "why_try": "A polished spread of tea, sandwiches, scones, and cakes."},
        ],
        "drinks": [
            {"name": "English breakfast tea", "why_try": "A comforting everyday classic."},
            {"name": "Cask ale", "why_try": "A traditional pub drink with local variety."},
        ],
    },
}


def suggest_food_and_drink(destination: str) -> Dict[str, List[Dict]]:
    key = destination.strip().lower()
    suggestions = FOOD_LIBRARY.get(key)
    if not suggestions:
        suggestions = {
            "foods": [
                {"name": "Local food market", "why_try": "A practical way to sample regional snacks and specialties."},
                {"name": "Signature street food", "why_try": "Ask locals or hotel staff for the safest busy stalls."},
                {"name": "Regional dessert", "why_try": "Desserts often reveal distinctive local ingredients."},
            ],
            "drinks": [
                {"name": "Local tea or coffee", "why_try": "A low-risk way to experience everyday food culture."},
                {"name": "Seasonal non-alcoholic cooler", "why_try": "Useful during warm sightseeing days."},
            ],
        }

    return {
        "destination": destination,
        "foods": suggestions["foods"],
        "drinks": suggestions["drinks"],
        "source": "local_culinary_knowledge",
    }
