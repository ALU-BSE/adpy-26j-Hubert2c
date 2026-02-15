from rest_framework import permissions


class IsSectorAgent(permissions.BasePermission):
    """Only users with user_type AGENT and assigned_sector can access."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, "user_type", None) == "AGENT" and bool(
            getattr(request.user, "assigned_sector", None)
        )


class IsGovOfficial(permissions.BasePermission):
    """Read-only for user_type GOV (RURA/RRA)."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if getattr(request.user, "user_type", None) != "GOV":
            return False
        return request.method in ("GET", "HEAD", "OPTIONS")


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Write only for owner; read for others if allowed by view."""

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "created_by", None)
        if owner is None:
            return True
        return owner == request.user
