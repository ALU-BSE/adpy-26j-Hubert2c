from django.test import TestCase
from .models import DomesticShipment

class DomesticShipmentTest(TestCase):

    def test_create_domestic_shipment(self):
        shipment = DomesticShipment.objects.create(
            tracking_code="DOM-001",
            sender_name="Aline M",
            sender_phone="+250788123456",
            pickup_district="Gasabo",
            pickup_sector="Kimironko",
            destination_district="Rwamagana",
            destination_sector="Kigabiro",
            delivery_method="MOTO",
        )

        self.assertEqual(shipment.status, "PENDING")
        self.assertEqual(shipment.delivery_method, "MOTO")
