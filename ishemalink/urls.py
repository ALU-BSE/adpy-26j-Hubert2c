from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connections

def health_check(request):
    try:
        connections["default"].cursor()
        db_status = "ok"
    except Exception:
        db_status = "error"

    return JsonResponse({
        "status": "running",
        "database": db_status
    })

def api_root(request):
    return JsonResponse({
        "name": "IshemaLink API",
        "version": "v1",
        "status_endpoint": "/api/status/"
    })

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core endpoints
    path("api/", api_root),
    path("api/status/", health_check),
    path("api/", include("core.urls")),
    path("api/identity/", include("core.identity_urls")),
    path("api/privacy/", include("core.privacy_urls")),
    path("api/compliance/", include("core.compliance_urls")),
    path("api/rbac/", include("core.rbac_urls")),
    path("api/gov/", include("core.gov_urls")),
    path("api/ops/", include("core.ops_urls")),

    # Domain apps
    path("api/domestic/", include("domestic.urls")),
    path("api/international/", include("international.urls")),
    path("api/shipments/", include("shipments.urls")),
    path("api/pricing/", include("pricing.urls")),
]
