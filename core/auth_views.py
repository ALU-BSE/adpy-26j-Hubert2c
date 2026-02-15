from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User


class LoginRateThrottle(AnonRateThrottle):
    rate = "5/minute"
    scope = "login"


class SessionLoginView(APIView):
    """POST /api/auth/login/session/ — web dashboard login (session)."""
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        phone = request.data.get("phone") or request.data.get("username")
        password = request.data.get("password")
        if not phone or not password:
            return Response(
                {"error": "phone and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        from django.contrib.auth import authenticate
        user = authenticate(request, username=phone, password=password)
        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if getattr(user, "is_anonymized", False):
            return Response(
                {"error": "Account disabled"},
                status=status.HTTP_403_FORBIDDEN,
            )
        login(request, user)
        return Response({
            "user_id": user.id,
            "phone": user.phone,
            "user_type": user.user_type,
        })


class LogoutView(APIView):
    """POST /api/auth/logout/ — session logout; JWT clients should discard tokens."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})


class WhoAmIView(APIView):
    """GET /api/auth/whoami/ — current user and auth method."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        auth_type = "session" if request.session.session_key else "jwt"
        return Response({
            "user_id": user.id,
            "phone": user.phone,
            "user_type": user.user_type,
            "assigned_sector": getattr(user, "assigned_sector", None),
            "is_verified": getattr(user, "is_verified", False),
            "auth_method": auth_type,
        })


class PasswordChangeView(APIView):
    """POST /api/auth/password/change/ — authenticated password change."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old = request.data.get("old_password")
        new = request.data.get("new_password")
        if not old or not new:
            return Response(
                {"error": "old_password and new_password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.user.check_password(old):
            return Response(
                {"error": "Invalid current password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.set_password(new)
        request.user.save()
        return Response({"message": "Password updated"})


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
    permission_classes = [AllowAny]


class ThrottledTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
