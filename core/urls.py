from django.urls import path
from .auth_views import (
    SessionLoginView,
    LogoutView,
    WhoAmIView,
    PasswordChangeView,
    ThrottledTokenObtainPairView,
    ThrottledTokenRefreshView,
)
from .views import (
    RegisterView,
    VerifyNIDView,
    UserProfileView,
    AgentOnboardView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/verify-nid/", VerifyNIDView.as_view()),
    path("auth/login/session/", SessionLoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/whoami/", WhoAmIView.as_view()),
    path("auth/password/change/", PasswordChangeView.as_view()),
    path("auth/token/obtain/", ThrottledTokenObtainPairView.as_view()),
    path("auth/token/refresh/", ThrottledTokenRefreshView.as_view()),
    path("users/me/", UserProfileView.as_view()),
    path("users/agents/onboard/", AgentOnboardView.as_view()),
]
