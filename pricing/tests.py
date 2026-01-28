from django.test import TestCase
from django.core.cache import cache
from .services import get_tariffs, calculate_price

class PricingTest(TestCase):

    def setUp(self):
        cache.clear()

    def test_tariff_cache_loads(self):
        data = get_tariffs()
        self.assertIn("rates", data)

    def test_price_calculation_zone_2(self):
        price = calculate_price("ZONE_2", 3)
        self.assertEqual(price, 600)
