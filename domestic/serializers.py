from rest_framework import serializers
from .models import DomesticShipment
from core.validators import validate_rwanda_phone

class DomesticShipmentSerializer(serializers.ModelSerializer):

    def validate_sender_phone(self, value: str) -> str:
        if not validate_rwanda_phone(value):
            raise serializers.ValidationError(
                "Phone number must be in +2507XX XXX XXX format."
            )
        return value

    class Meta:
        model = DomesticShipment
        fields = "__all__"
