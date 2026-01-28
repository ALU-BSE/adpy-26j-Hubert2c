from rest_framework import serializers
from .models import User
from .validators import validate_rwanda_phone, validate_nid

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "password",
            "user_type",
            "nid",
            "assigned_sector",
        )

    def validate_phone(self, value: str) -> str:
        if not validate_rwanda_phone(value):
            raise serializers.ValidationError(
                "Phone number must follow +2507XX XXX XXX format."
            )
        return value

    def validate_nid(self, value: str) -> str:
        if value and not validate_nid(value):
            raise serializers.ValidationError(
                "Invalid NID format. Must be 16 numeric digits starting with 1."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "user_type",
            "nid",
            "assigned_sector",
        )
