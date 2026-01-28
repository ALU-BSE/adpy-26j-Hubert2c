from django.db import models

class Shipment(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_TRANSIT", "In Transit"),
        ("ARRIVED_HUB", "Arrived at Hub"),
        ("DELIVERED", "Delivered"),
        ("CLEARED_CUSTOMS", "Cleared Customs"),
    )

    tracking_code = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    destination = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tracking_code


class ShipmentLog(models.Model):
    shipment = models.ForeignKey(
        Shipment, related_name="logs", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shipment.tracking_code} - {self.status}"
