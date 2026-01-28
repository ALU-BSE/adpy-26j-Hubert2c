from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ("AGENT", "Agent"),
        ("CUSTOMER", "Customer"),
        ("ADMIN", "Admin"),
    )

    phone = models.CharField(max_length=13, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    nid = models.CharField(max_length=16, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
