from django.urls import path
from .privacy_views import (
    MyDataView,
    AnonymizeView,
    ConsentHistoryView,
)

urlpatterns = [
    path("my-data/", MyDataView.as_view()),
    path("anonymize/", AnonymizeView.as_view()),
    path("consent-history/", ConsentHistoryView.as_view()),
]
