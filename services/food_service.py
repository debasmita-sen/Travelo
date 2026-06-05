from typing import Dict, List  # typing helpers


FOOD_LIBRARY = {  # curated food and drink suggestions used as fallback
    "goa": {
        "foods": [
            {"name": "Goan fish curry", "why_try": "Coconut, kokum, and local spices make it a coastal classic.", "where_to_try": "beach shacks, family-run Goan restaurants, or fish thali places", "tip": "Pair it with rice and ask for the spice level before ordering."},
            {"name": "Pork vindaloo", "why_try": "A bold, tangy Goan-Portuguese dish with vinegar, garlic, and chilli.", "where_to_try": "traditional Goan restaurants, especially in Panaji, Mapusa, and old village areas", "tip": "It is usually richer and sharper than generic restaurant vindaloo outside Goa."},
            {"name": "Bebinca", "why_try": "Layered coconut dessert often served at celebrations.", "where_to_try": "local bakeries, dessert shops, or Goan Catholic restaurants", "tip": "Try a small slice after dinner; it is dense, sweet, and buttery."},
        ],
        "drinks": [
            {"name": "Feni", "why_try": "A famous local spirit made from cashew apple or coconut.", "where_to_try": "licensed bars, heritage restaurants, or curated local tasting experiences", "tip": "It is strong and aromatic, so try it slowly or mixed with lime/soda."},
            {"name": "Kokum juice", "why_try": "A refreshing sweet-sour local cooler.", "where_to_try": "local restaurants, beach cafes, and lunch thali spots", "tip": "Good for hot afternoons and a safer non-alcoholic choice."},
        ],
    },
    "paris": {
        "foods": [
            {"name": "Croissant", "why_try": "Buttery pastry best enjoyed fresh from a neighborhood boulangerie.", "where_to_try": "morning bakeries away from major tourist queues", "tip": "Choose one that looks deeply golden and flaky."},
            {"name": "Steak frites", "why_try": "A dependable bistro classic.", "where_to_try": "classic bistros and brasseries", "tip": "Ask about the sauce and doneness before ordering."},
            {"name": "Macarons", "why_try": "Colorful almond meringue sweets associated with Paris pâtisseries.", "where_to_try": "pâtisseries and specialty dessert shops", "tip": "Buy a few flavors instead of a large box if you only want to sample."},
        ],
        "drinks": [
            {"name": "Café crème", "why_try": "A simple café ritual for slow mornings.", "where_to_try": "corner cafés and breakfast spots", "tip": "Best with a pastry rather than as a rushed takeaway."},
            {"name": "French wine", "why_try": "Easy to pair with bistro meals and cheese plates.", "where_to_try": "wine bars, bistros, and cheese-focused restaurants", "tip": "Ask for a by-the-glass recommendation that matches your meal."},
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
    key = destination.strip().lower()  # normalize destination
    suggestions = FOOD_LIBRARY.get(key)
    if not suggestions:
        suggestions = {  # generic fallback suggestions
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
        "source": "local_culinary_knowledge",  # mark this as local curated content
    }
