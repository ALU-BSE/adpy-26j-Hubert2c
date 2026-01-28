from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import DomesticShipment
from .serializers import DomesticShipmentSerializer


class DomesticShipmentCreateView(APIView):
    """
    POST /api/domestic/shipments/
    """

    def post(self, request):
        serializer = DomesticShipmentSerializer(data=request.data)
        if serializer.is_valid():
            shipment = serializer.save()
            return Response(
                {
                    "tracking_code": shipment.tracking_code,
                    "status": shipment.status,
                    "delivery_method": shipment.delivery_method,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DomesticShipmentDetailView(APIView):
    """
    GET /api/domestic/shipments/{tracking_code}/
    """

    def get(self, request, tracking_code):
        shipment = get_object_or_404(
            DomesticShipment, tracking_code=tracking_code
        )
        serializer = DomesticShipmentSerializer(shipment)
        return Response(serializer.data)


class DomesticShipmentStatusUpdateView(APIView):
    """
    POST /api/domestic/shipments/{tracking_code}/update-status/
    """

    def post(self, request, tracking_code):
        shipment = get_object_or_404(
            DomesticShipment, tracking_code=tracking_code
        )
        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"error": "Status is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        shipment.status = new_status
        shipment.save()

        return Response(
            {
                "message": "Status updated successfully.",
                "tracking_code": shipment.tracking_code,
                "status": shipment.status,
            }
        )
