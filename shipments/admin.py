from django.contrib import admin
from .models import Shipment, ShipmentLog

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("tracking_code", "status", "destination", "updated_at")
    search_fields = ("tracking_code",)
    list_filter = ("status",)

@admin.register(ShipmentLog)
class ShipmentLogAdmin(admin.ModelAdmin):
    list_display = ("shipment", "status", "created_at")
