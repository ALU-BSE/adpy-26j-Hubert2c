from django.urls import path
from .views import (
    RegisterView,
    VerifyNIDView,
    UserProfileView,
    AgentOnboardView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/verify-nid/", VerifyNIDView.as_view()),
    path("users/me/", UserProfileView.as_view()),
    path("users/agents/onboard/", AgentOnboardView.as_view()),
]
