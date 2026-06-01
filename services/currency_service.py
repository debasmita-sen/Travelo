import re
from typing import Dict, Optional


USD_RATES = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.92,
    "JPY": 157.0,
    "GBP": 0.79,
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "INR": "₹",
    "EUR": "€",
    "JPY": "¥",
    "GBP": "£",
}

DESTINATION_CURRENCIES = {
    "goa": "INR",
    "india": "INR",
    "mumbai": "INR",
    "delhi": "INR",
    "bangalore": "INR",
    "kolkata": "INR",
    "paris": "EUR",
    "france": "EUR",
    "tokyo": "JPY",
    "japan": "JPY",
    "london": "GBP",
    "united kingdom": "GBP",
    "uk": "GBP",
    "new york": "USD",
    "usa": "USD",
    "united states": "USD",
}


def destination_currency(destination: str) -> str:
    key = destination.strip().lower()
    return DESTINATION_CURRENCIES.get(key, "USD")


def convert_currency(amount: float, source_currency: str, target_currency: str) -> float:
    source_rate = USD_RATES.get(source_currency, 1.0)
    target_rate = USD_RATES.get(target_currency, 1.0)
    return amount / source_rate * target_rate


def parse_budget_text(text: str, destination: str, default_amount: float = 1200) -> Dict:
    amount, currency = _find_budget_amount(text)
    if amount is None:
        amount = default_amount
        currency = "INR"

    target_currency = destination_currency(destination)
    budget_usd = convert_currency(amount, currency, "USD")
    budget_local = convert_currency(amount, currency, target_currency)
    return {
        "amount": round(budget_usd, 2),
        "input_amount": round(amount, 2),
        "input_currency": currency,
        "local_amount": round(budget_local, 2),
        "local_currency": target_currency,
    }


def parse_budget_value(value, destination: str, default_currency: str = "INR") -> Dict:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        amount = 0

    target_currency = destination_currency(destination)
    budget_usd = convert_currency(amount, default_currency, "USD")
    budget_local = convert_currency(amount, default_currency, target_currency)
    return {
        "amount": round(budget_usd, 2),
        "input_amount": round(amount, 2),
        "input_currency": default_currency,
        "local_amount": round(budget_local, 2),
        "local_currency": target_currency,
    }


def format_currency(amount: float, currency: str) -> str:
    symbol = CURRENCY_SYMBOLS.get(currency, f"{currency} ")
    maximum_digits = 0 if currency in {"INR", "JPY"} else 2
    formatted = f"{amount:,.{maximum_digits}f}"
    return f"{symbol}{formatted}"


def _find_budget_amount(text: str) -> tuple[Optional[float], str]:
    patterns = [
        r"(?P<currency>₹|rs\.?|inr|\$|usd|eur|€|gbp|£|jpy|¥)\s*(?P<amount>\d+(?:,\d+)*(?:\.\d+)?)\s*(?P<suffix>k|lakh|lakhs|lac|lacs)?",
        r"(?P<amount>\d+(?:,\d+)*(?:\.\d+)?)\s*(?P<suffix>k|lakh|lakhs|lac|lacs)?\s*(?P<currency>₹|rs\.?|inr|\$|usd|eur|€|gbp|£|jpy|¥)?",
    ]
    candidates = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            amount = float(match.group("amount").replace(",", ""))
            suffix = (match.group("suffix") or "").lower()
            currency = _normalize_currency(match.group("currency"))
            if suffix == "k":
                amount *= 1000
            elif suffix in {"lakh", "lakhs", "lac", "lacs"}:
                amount *= 100000
            nearby_text = text[max(match.start() - 20, 0): match.end() + 20].lower()
            has_budget_word = any(term in nearby_text for term in ("budget", "under", "within", "rs", "inr", "₹", "$", "usd", "eur", "gbp", "jpy"))
            has_money_marker = bool(match.group("currency") or suffix)
            if has_budget_word or has_money_marker or amount >= 1000:
                candidates.append((match.start(), amount, currency, has_budget_word, has_money_marker))
    if not candidates:
        return None, "INR"

    _, amount, currency, _, _ = max(candidates, key=lambda item: (item[4], item[3], item[0]))
    return amount, currency


def _normalize_currency(value: Optional[str]) -> str:
    if not value:
        return "INR"

    lowered = value.lower().strip()
    if lowered in {"₹", "rs", "rs.", "inr"}:
        return "INR"
    if lowered in {"$", "usd"}:
        return "USD"
    if lowered in {"€", "eur"}:
        return "EUR"
    if lowered in {"£", "gbp"}:
        return "GBP"
    if lowered in {"¥", "jpy"}:
        return "JPY"
    return "INR"
