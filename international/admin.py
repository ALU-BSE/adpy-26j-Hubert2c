from django.contrib import admin
from .models import InternationalShipment

@admin.register(InternationalShipment)
class InternationalShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_code",
        "destination",
        "customs_cleared",
        "created_at",
    )
    search_fields = ("tracking_code", "sender_name")
