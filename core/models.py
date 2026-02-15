from django.contrib.auth.models import AbstractUser
from django.db import models
from .fields import EncryptedTextField

class User(AbstractUser):
    USER_TYPES = (
        ("AGENT", "Agent"),
        ("CUSTOMER", "Customer"),
        ("ADMIN", "Admin"),
        ("DRIVER", "Driver"),
        ("GOV", "Government"),
    )

    phone = models.CharField(max_length=13, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    nid = EncryptedTextField(null=True, blank=True)
    assigned_sector = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    terms_version = models.CharField(max_length=20, null=True, blank=True)
    is_anonymized = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []


class AuditLog(models.Model):
    """Glass log: who viewed what sensitive data and when."""
    user_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=50, blank=True)
    action = models.CharField(max_length=50)
    resource = models.CharField(max_length=255, blank=True)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
