from django.urls import path
from .views import (
    TariffListView,
    PriceCalculateView,
    ClearTariffCacheView,
)

urlpatterns = [
    path("tariffs/", TariffListView.as_view()),
    path("calculate/", PriceCalculateView.as_view()),
    path("admin/cache/clear-tariffs/", ClearTariffCacheView.as_view()),
]
