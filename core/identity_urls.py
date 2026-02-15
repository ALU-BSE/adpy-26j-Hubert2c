from django.urls import path
from .identity_views import (
    IdentityRegisterView,
    IdentitySendOTPView,
    VerifyOTPView,
    KYCNIDView,
    RecoverInitiateView,
    RecoverConfirmView,
    IdentityStatusView,
)

urlpatterns = [
    path("register/", IdentityRegisterView.as_view()),
    path("send-otp/", IdentitySendOTPView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("kyc/nid/", KYCNIDView.as_view()),
    path("recover/initiate/", RecoverInitiateView.as_view()),
    path("recover/confirm/", RecoverConfirmView.as_view()),
    path("status/", IdentityStatusView.as_view()),
]
