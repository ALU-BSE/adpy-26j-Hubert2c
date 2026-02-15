from django.urls import path
from .compliance_views import ComplianceAuditLogsView

urlpatterns = [
    path("audit-logs/", ComplianceAuditLogsView.as_view()),
]
