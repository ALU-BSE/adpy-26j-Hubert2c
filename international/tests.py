from django.test import TestCase
from .models import InternationalShipment

class InternationalShipmentTest(TestCase):

    def test_create_international_shipment(self):
        shipment = InternationalShipment.objects.create(
            tracking_code="INT-001",
            destination="KAMPALA",
            sender_name="Jean Paul",
            sender_nid="1199887766554433",
            receiver_name="Moses K",
            passport_number="PA123456",
        )
        self.assertEqual(shipment.destination, "KAMPALA")
        self.assertFalse(shipment.customs_cleared)
