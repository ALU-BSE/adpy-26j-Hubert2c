from django.db import models

class DomesticShipment(models.Model):
    DELIVERY_METHODS = (
        ("MOTO", "Motorcycle"),
        ("BUS", "Bus"),
    )

    tracking_code = models.CharField(max_length=50, unique=True)
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=13)
    pickup_district = models.CharField(max_length=50)
    pickup_sector = models.CharField(max_length=50)
    destination_district = models.CharField(max_length=50)
    destination_sector = models.CharField(max_length=50)
    delivery_method = models.CharField(
        max_length=10, choices=DELIVERY_METHODS
    )
    status = models.CharField(
        max_length=30, default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tracking_code} ({self.pickup_district} → {self.destination_district})"
