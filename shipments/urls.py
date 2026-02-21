from django.urls import path
from .views import (
    ShipmentStatusUpdateView,
    ShipmentBatchUpdateView,
    ShipmentTrackingView,
    ShipmentListView,
)

urlpatterns = [
    path("<int:id>/update-status/", ShipmentStatusUpdateView.as_view()),
    path("batch-update/", ShipmentBatchUpdateView.as_view()),
    path("<int:id>/tracking/", ShipmentTrackingView.as_view()),
    path("", ShipmentListView.as_view()),
]
