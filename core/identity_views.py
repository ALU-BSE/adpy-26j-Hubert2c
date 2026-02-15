import random
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegisterSerializer
from .validators import validate_nid, validate_rwanda_phone

User = get_user_model()

OTP_TTL_SECONDS = 300  # 5 minutes
OTP_KEY_PREFIX = "otp:"
RECOVERY_KEY_PREFIX = "recovery:"


def _generate_otp() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(6))


def _otp_cache_key(phone: str, prefix: str = OTP_KEY_PREFIX) -> str:
    return f"{prefix}{phone}"


class IdentityRegisterView(APIView):
    """POST /api/identity/register/ — initial account creation (unverified)."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            terms = request.data.get("terms_version", "1.0")
            user.terms_version = terms
            user.save(update_fields=["terms_version"])
            return Response(
                {
                    "id": user.id,
                    "phone": user.phone,
                    "role": user.user_type,
                    "assigned_sector": user.assigned_sector,
                    "is_verified": False,
                    "message": "Account created. Complete OTP and NID to verify.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdentitySendOTPView(APIView):
    """POST /api/identity/send-otp/ — simulate sending OTP (stores in cache)."""
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        if not phone or not validate_rwanda_phone(phone):
            return Response(
                {"error": "Valid +250 phone required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = _generate_otp()
        cache.set(_otp_cache_key(phone), otp, OTP_TTL_SECONDS)
        return Response({"message": "OTP sent (simulated)", "otp": otp})


class VerifyOTPView(APIView):
    """POST /api/identity/verify-otp/ — validate SMS code (simulated)."""
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")
        if not phone or not code:
            return Response(
                {"error": "phone and code required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not validate_rwanda_phone(phone):
            return Response(
                {"error": "Invalid +250 phone format"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        key = _otp_cache_key(phone)
        stored = cache.get(key)
        if stored is None:
            return Response(
                {"error": "OTP expired or not sent"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if str(stored) != str(code).strip():
            return Response(
                {"error": "Invalid code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cache.delete(key)
        try:
            user = User.objects.get(phone=phone)
            user.is_verified = True
            user.save(update_fields=["is_verified"])
        except User.DoesNotExist:
            pass
        return Response({"message": "OTP verified", "verified": True})


class KYCNIDView(APIView):
    """POST /api/identity/kyc/nid/ — submit NID for verification."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nid = request.data.get("nid")
        if not nid or not validate_nid(nid):
            return Response(
                {"error": "Invalid NID. Must be 16 digits starting with 1 and valid birth year."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.nid = nid
        request.user.save(update_fields=["nid"])
        request.user.is_verified = True
        request.user.save(update_fields=["is_verified"])
        return Response({"message": "NID verified", "verified": True})


class RecoverInitiateView(APIView):
    """POST /api/identity/recover/initiate/ — start recovery (send OTP)."""
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        if not phone or not validate_rwanda_phone(phone):
            return Response(
                {"error": "Valid +250 phone required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = _generate_otp()
        cache.set(_otp_cache_key(phone, RECOVERY_KEY_PREFIX), otp, OTP_TTL_SECONDS)
        return Response(
            {"message": "Recovery OTP sent (simulated).", "otp": otp},
            status=status.HTTP_200_OK,
        )


class RecoverConfirmView(APIView):
    """POST /api/identity/recover/confirm/ — reset credentials after OTP."""
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")
        new_password = request.data.get("new_password")
        if not phone or not code or not new_password:
            return Response(
                {"error": "phone, code and new_password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        key = _otp_cache_key(phone, RECOVERY_KEY_PREFIX)
        stored = cache.get(key)
        if stored is None or str(stored) != str(code).strip():
            return Response(
                {"error": "Invalid or expired recovery code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cache.delete(key)
        try:
            user = User.objects.get(phone=phone)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successfully"})
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class IdentityStatusView(APIView):
    """GET /api/identity/status/ — check verification level."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "phone": u.phone,
            "is_verified": getattr(u, "is_verified", False),
            "has_nid": bool(getattr(u, "nid", None)),
            "can_ship": getattr(u, "is_verified", False),
        })
