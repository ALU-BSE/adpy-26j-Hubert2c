from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import UserRegisterSerializer, UserProfileSerializer
from .validators import validate_nid


class RegisterView(APIView):
    """
    POST /api/auth/register/
    """

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "phone": user.phone,
                    "role": user.user_type,
                    "assigned_sector": user.assigned_sector,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyNIDView(APIView):
    """
    POST /api/auth/verify-nid/
    """

    def post(self, request):
        nid = request.data.get("nid")
        if not nid or not validate_nid(nid):
            return Response(
                {
                    "valid": False,
                    "error": "Invalid NID format. Must be 16 numeric digits starting with 1."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"valid": True})


class UserProfileView(APIView):
    """
    GET /api/users/me/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class AgentOnboardView(APIView):
    """
    POST /api/users/agents/onboard/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.user_type != "AGENT":
            return Response(
                {"error": "Only agents can access this endpoint."},
                status=status.HTTP_403_FORBIDDEN,
            )

        nid = request.data.get("nid")
        if not validate_nid(nid):
            return Response(
                {"error": "Invalid Rwanda National ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.nid = nid
        request.user.save()

        return Response({"message": "Agent onboarded successfully."})
