from django.db import models

class InternationalShipment(models.Model):
    DESTINATION_CHOICES = (
        ("KAMPALA", "Kampala"),
        ("NAIROBI", "Nairobi"),
        ("GOMA", "Goma"),
    )

    tracking_code = models.CharField(max_length=50, unique=True)
    destination = models.CharField(max_length=20, choices=DESTINATION_CHOICES)
    sender_name = models.CharField(max_length=100)
    sender_nid = models.CharField(max_length=16)
    receiver_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20)
    customs_cleared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tracking_code} → {self.destination}"
