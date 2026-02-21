from django.test import TestCase
from .models import Shipment

class ShipmentTest(TestCase):

    def test_create_shipment(self):
        shipment = Shipment.objects.create(
            tracking_code="RW-KP-001",
            status="PENDING",
            destination="Kampala",
        )
        self.assertEqual(shipment.status, "PENDING")
