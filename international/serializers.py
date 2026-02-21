from rest_framework import serializers
from .models import InternationalShipment
from core.validators import validate_nid

class InternationalShipmentSerializer(serializers.ModelSerializer):

    def validate_sender_nid(self, value: str) -> str:
        if not validate_nid(value):
            raise serializers.ValidationError(
                "Invalid Rwanda National ID for sender."
            )
        return value

    class Meta:
        model = InternationalShipment
        fields = "__all__"
