from django.core.cache import cache
from datetime import datetime

TARIFF_CACHE_KEY = "shipping_tariffs"
TARIFF_CACHE_TTL = 60 * 60  # 1 hour

def load_tariffs_from_db() -> dict:
    """
    Simulate database tariff lookup.
    In production, this would come from a Pricing table.
    """
    return {
        "zone_1_base": 1500,       # Kigali
        "zone_2_kg_rate": 200,     # Provinces
        "zone_3_kg_rate": 500,     # EAC
    }


def get_tariffs() -> dict:
    tariffs = cache.get(TARIFF_CACHE_KEY)

    if tariffs is None:
        tariffs = load_tariffs_from_db()
        cache.set(TARIFF_CACHE_KEY, tariffs, TARIFF_CACHE_TTL)

    return {
        "cached_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rates": tariffs,
    }


def clear_tariff_cache() -> None:
    cache.delete(TARIFF_CACHE_KEY)


def calculate_price(zone: str, weight_kg: float) -> int:
    tariffs = cache.get(TARIFF_CACHE_KEY)

    if tariffs is None:
        tariffs = load_tariffs_from_db()
        cache.set(TARIFF_CACHE_KEY, tariffs, TARIFF_CACHE_TTL)

    if zone == "ZONE_1":
        return tariffs["zone_1_base"]

    if zone == "ZONE_2":
        return tariffs["zone_2_kg_rate"] * int(weight_kg)

    if zone == "ZONE_3":
        return tariffs["zone_3_kg_rate"] * int(weight_kg)

    raise ValueError("Invalid zone")
