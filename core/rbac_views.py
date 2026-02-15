from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsGovOfficial, IsSectorAgent

User = get_user_model()

ROLES = [{"id": k, "name": v} for k, v in User.USER_TYPES]


class RolesListView(APIView):
    """GET /api/rbac/roles/ — list available roles."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"roles": ROLES})


class AssignRoleView(APIView):
    """POST /api/rbac/assign/ — promote user (e.g. Customer -> Driver). Admin only."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if getattr(request.user, "user_type", None) != "ADMIN":
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get("user_id")
        role = request.data.get("role")
        if not user_id or not role:
            return Response(
                {"error": "user_id and role required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        valid_roles = [r["id"] for r in ROLES]
        if role not in valid_roles:
            return Response(
                {"error": f"role must be one of {valid_roles}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            target = User.objects.get(pk=user_id)
            target.user_type = role
            if role == "AGENT" and request.data.get("assigned_sector"):
                target.assigned_sector = request.data.get("assigned_sector")
            target.save()
            return Response({"message": f"User {user_id} assigned role {role}"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class GovManifestsView(APIView):
    """GET /api/gov/manifests/ — Gov role: read-only view of all cargo."""
    permission_classes = [IsAuthenticated, IsGovOfficial]

    def get(self, request):
        from domestic.models import DomesticShipment
        from international.models import InternationalShipment
        from shipments.models import Shipment
        domestic = list(
            DomesticShipment.objects.all().values(
                "tracking_code", "pickup_district", "pickup_sector",
                "destination_district", "destination_sector", "status", "created_at"
            )[:200]
        )
        international = list(
            InternationalShipment.objects.all().values(
                "tracking_code", "destination", "customs_cleared", "created_at"
            )[:200]
        )
        unified = list(
            Shipment.objects.all().values(
                "id", "tracking_code", "status", "destination", "updated_at"
            )[:200]
        )
        return Response({
            "domestic": domestic,
            "international": international,
            "unified": unified,
        })


class SectorStatsView(APIView):
    """GET /api/ops/sector-stats/ — Agent role: stats for their sector only."""
    permission_classes = [IsAuthenticated, IsSectorAgent]

    def get(self, request):
        sector = getattr(request.user, "assigned_sector", None)
        if not sector:
            return Response({"error": "No sector assigned"}, status=status.HTTP_403_FORBIDDEN)
        from django.db.models import Count, Q
        from domestic.models import DomesticShipment
        qs = DomesticShipment.objects.filter(
            Q(pickup_sector=sector) | Q(destination_sector=sector)
        )
        total = qs.count()
        by_status = dict(qs.values("status").annotate(c=Count("id")).values_list("status", "c"))
        return Response({
            "sector": sector,
            "total_shipments": total,
            "by_status": by_status,
        })
