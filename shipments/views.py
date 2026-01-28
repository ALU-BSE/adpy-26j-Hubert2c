import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import Shipment
from .serializers import ShipmentSerializer, ShipmentLogSerializer
from .tasks import process_status_update


class ShipmentStatusUpdateView(APIView):
    """
    POST /api/shipments/{id}/update-status/
    """

    def post(self, request, id):
        shipment = get_object_or_404(Shipment, id=id)
        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"error": "Status is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        asyncio.create_task(
            process_status_update(shipment, new_status)
        )

        return Response(
            {
                "message": "Status update queued",
                "tracking_code": shipment.tracking_code,
                "status": "queued",
            }
        )


class ShipmentBatchUpdateView(APIView):
    """
    POST /api/shipments/batch-update/
    """

    def post(self, request):
        shipment_ids = request.data.get("shipment_ids", [])
        new_status = request.data.get("status")

        if not shipment_ids or not new_status:
            return Response(
                {"error": "shipment_ids and status are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for shipment_id in shipment_ids:
            try:
                shipment = Shipment.objects.get(id=shipment_id)
                asyncio.create_task(
                    process_status_update(shipment, new_status)
                )
            except Shipment.DoesNotExist:
                continue

        return Response(
            {
                "message": f"Processing started for {len(shipment_ids)} shipments.",
                "status": "queued",
            }
        )


class ShipmentTrackingView(APIView):
    """
    GET /api/shipments/{id}/tracking/
    """

    def get(self, request, id):
        shipment = get_object_or_404(Shipment, id=id)
        logs = shipment.logs.all().order_by("-created_at")
        serializer = ShipmentLogSerializer(logs, many=True)
        return Response(serializer.data)


class ShipmentListView(APIView):
    """
    GET /api/shipments/?page=1&size=20&status=IN_TRANSIT&search=TRK
    """

    def get(self, request):
        qs = Shipment.objects.all().order_by("-updated_at")

        status_filter = request.GET.get("status")
        search = request.GET.get("search")

        if status_filter:
            qs = qs.filter(status=status_filter)

        if search:
            qs = qs.filter(tracking_code__icontains=search)

        page = int(request.GET.get("page", 1))
        size = int(request.GET.get("size", 20))

        paginator = Paginator(qs, size)
        page_obj = paginator.get_page(page)

        serializer = ShipmentSerializer(page_obj.object_list, many=True)

        return Response(
            {
                "meta": {
                    "total_count": paginator.count,
                    "current_page": page,
                    "next_link": (
                        f"?page={page + 1}&size={size}"
                        if page_obj.has_next()
                        else None
                    ),
                },
                "data": serializer.data,
            }
        )
