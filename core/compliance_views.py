from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import AuditLog


class ComplianceAuditLogsView(APIView):
    """GET /api/compliance/audit-logs/ — Admin only: view access history."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from rest_framework import status
        from rest_framework.response import Response
        if getattr(request.user, "user_type", None) != "ADMIN":
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        logs = AuditLog.objects.all().order_by("-created_at")[:500].values(
            "id", "user_id", "username", "action", "resource", "created_at", "ip_address"
        )
        return Response({"logs": list(logs)})
