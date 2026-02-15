from django.urls import path
from .rbac_views import GovManifestsView

urlpatterns = [
    path("manifests/", GovManifestsView.as_view()),
]
