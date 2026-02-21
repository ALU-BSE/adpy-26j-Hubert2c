from django.contrib import admin
from .models import DomesticShipment

@admin.register(DomesticShipment)
class DomesticShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_code",
        "pickup_district",
        "destination_district",
        "delivery_method",
        "status",
        "created_at",
    )
    search_fields = ("tracking_code", "sender_name")
    list_filter = ("delivery_method", "status")
