from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT pair with custom claim user_type (and username = phone)."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_type"] = getattr(user, "user_type", None)
        token["phone"] = getattr(user, "phone", None)
        return token

    def validate(self, attrs):
        # Accept phone as username (AUTH_USER_MODEL uses USERNAME_FIELD = "phone")
        username = attrs.get("username") or attrs.get("phone")
        if username:
            attrs["username"] = username
        return super().validate(attrs)
