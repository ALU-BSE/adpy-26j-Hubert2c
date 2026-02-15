from .models import AuditLog

SENSITIVE_PATHS = (
    "/api/domestic/shipments/",
    "/api/international/shipments/",
    "/api/shipments/",
    "/api/users/me/",
    "/api/privacy/",
    "/api/compliance/",
)


class AuditLogMiddleware:
    """Log GET (and other) access to sensitive resources for the Glass Log."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method in ("GET", "POST", "PUT", "PATCH") and response.status_code == 200:
            path = request.path
            if any(path.startswith(p) for p in SENSITIVE_PATHS):
                user = getattr(request, "user", None)
                user_id = user.id if user and getattr(user, "id", None) else None
                username = getattr(user, "phone", None) or getattr(user, "username", "") if user else ""
                xff = request.META.get("HTTP_X_FORWARDED_FOR")
                ip = (xff.split(",")[0].strip() if xff else None) or request.META.get("REMOTE_ADDR")
                AuditLog.objects.create(
                    user_id=user_id,
                    username=str(username)[:50],
                    action=f"{request.method} {path}",
                    resource=path,
                    details={"method": request.method},
                    ip_address=ip,
                )
        return response
