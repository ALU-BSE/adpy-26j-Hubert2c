from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import get_tariffs, calculate_price, clear_tariff_cache


class TariffListView(APIView):
    """
    GET /api/pricing/tariffs/
    """

    def get(self, request):
        data = get_tariffs()
        response = Response(data)
        response["X-Cache-Hit"] = "TRUE"
        return response


class PriceCalculateView(APIView):
    """
    POST /api/pricing/calculate/
    """

    def post(self, request):
        zone = request.data.get("zone")
        weight = request.data.get("weight_kg")

        if not zone or not weight:
            return Response(
                {"error": "zone and weight_kg are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            price = calculate_price(zone, float(weight))
        except ValueError:
            return Response(
                {"error": "Invalid zone provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "zone": zone,
                "weight_kg": weight,
                "price": price,
            }
        )


class ClearTariffCacheView(APIView):
    """
    POST /api/admin/cache/clear-tariffs/
    """

    def post(self, request):
        clear_tariff_cache()
        return Response({"message": "Tariff cache cleared successfully."})
