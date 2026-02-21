from rest_framework import serializers
from .models import Shipment, ShipmentLog

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = (
            "tracking_code",
            "status",
            "destination",
            "updated_at",
        )


class ShipmentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentLog
        fields = (
            "status",
            "message",
            "created_at",
        )
