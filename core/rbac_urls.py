from django.urls import path
from .rbac_views import (
    RolesListView,
    AssignRoleView,
    GovManifestsView,
    SectorStatsView,
)

urlpatterns = [
    path("roles/", RolesListView.as_view()),
    path("assign/", AssignRoleView.as_view()),
]
