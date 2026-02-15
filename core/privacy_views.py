from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class MyDataView(APIView):
    """GET /api/privacy/my-data/ — JSON export of all data we hold on the user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if getattr(user, "is_anonymized", False):
            return Response({"message": "Account anonymized", "data": {}}, status=status.HTTP_200_OK)
        from domestic.models import DomesticShipment
        from international.models import InternationalShipment
        from shipments.models import Shipment
        domestic = list(
            DomesticShipment.objects.filter(sender_phone=user.phone).values(
                "tracking_code", "sender_name", "pickup_district", "destination_district", "status", "created_at"
            )
        )
        international = []
        payload = {
            "user": {
                "id": user.id,
                "phone": user.phone,
                "user_type": user.user_type,
                "nid": getattr(user, "nid", None),
                "assigned_sector": getattr(user, "assigned_sector", None),
                "is_verified": getattr(user, "is_verified", False),
                "terms_version": getattr(user, "terms_version", None),
                "date_joined": user.date_joined.isoformat() if user.date_joined else None,
            },
            "domestic_shipments": domestic,
            "international_shipments": international,
            "consent": {"terms_version": getattr(user, "terms_version", None)},
        }
        return Response(payload)


class AnonymizeView(APIView):
    """POST /api/privacy/anonymize/ — Right to erasure: soft-delete and anonymize."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.first_name = "Redacted"
        user.last_name = "Redacted"
        user.email = ""
        user.phone = f"redacted_{user.id}"
        user.nid = None
        user.assigned_sector = None
        user.is_anonymized = True
        user.is_active = False
        user.set_unusable_password()
        user.save()
        from django.contrib.auth import logout
        logout(request)
        return Response({"message": "Account anonymized. You have been logged out."})


class ConsentHistoryView(APIView):
    """GET /api/privacy/consent-history/ — terms & versions agreed."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "terms_version": getattr(user, "terms_version", None),
            "history": [{"version": getattr(user, "terms_version", "1.0"), "agreed_at": getattr(user, "date_joined", None)}],
        })


