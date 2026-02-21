from django.urls import path
from .views import (
    DomesticShipmentCreateView,
    DomesticShipmentDetailView,
    DomesticShipmentStatusUpdateView,
)

urlpatterns = [
    path("shipments/", DomesticShipmentCreateView.as_view()),
    path(
        "shipments/<str:tracking_code>/",
        DomesticShipmentDetailView.as_view(),
    ),
    path(
        "shipments/<str:tracking_code>/update-status/",
        DomesticShipmentStatusUpdateView.as_view(),
    ),
]
