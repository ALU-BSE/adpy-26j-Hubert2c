from django.urls import path
from .rbac_views import SectorStatsView

urlpatterns = [
    path("sector-stats/", SectorStatsView.as_view()),
]
