from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import InternationalShipment
from .serializers import InternationalShipmentSerializer


class InternationalShipmentCreateView(APIView):
    """
    POST /api/international/shipments/
    """

    def post(self, request):
        serializer = InternationalShipmentSerializer(data=request.data)
        if serializer.is_valid():
            shipment = serializer.save()
            return Response(
                {
                    "tracking_code": shipment.tracking_code,
                    "destination": shipment.destination,
                    "customs_cleared": shipment.customs_cleared,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InternationalShipmentDetailView(APIView):
    """
    GET /api/international/shipments/{tracking_code}/
    """

    def get(self, request, tracking_code):
        shipment = get_object_or_404(
            InternationalShipment, tracking_code=tracking_code
        )
        serializer = InternationalShipmentSerializer(shipment)
        return Response(serializer.data)


class CustomsClearanceView(APIView):
    """
    POST /api/international/shipments/{tracking_code}/clear-customs/
    """

    def post(self, request, tracking_code):
        shipment = get_object_or_404(
            InternationalShipment, tracking_code=tracking_code
        )
        shipment.customs_cleared = True
        shipment.save()

        return Response(
            {
                "message": "Shipment cleared by customs.",
                "tracking_code": shipment.tracking_code,
            }
        )
