from django.urls import path
from .views import (
    InternationalShipmentCreateView,
    InternationalShipmentDetailView,
    CustomsClearanceView,
)

urlpatterns = [
    path("shipments/", InternationalShipmentCreateView.as_view()),
    path(
        "shipments/<str:tracking_code>/",
        InternationalShipmentDetailView.as_view(),
    ),
    path(
        "shipments/<str:tracking_code>/clear-customs/",
        CustomsClearanceView.as_view(),
    ),
]
