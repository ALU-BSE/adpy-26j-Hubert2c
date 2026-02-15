import base64
import hashlib
from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet


def _get_fernet() -> Fernet:
    raw = getattr(settings, "FIELD_ENCRYPTION_KEY", None) or settings.SECRET_KEY
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    h = hashlib.sha256(raw).digest()
    key = base64.urlsafe_b64encode(h)
    return Fernet(key)


class EncryptedTextField(models.TextField):
    """Stores value encrypted at rest; decrypts when read."""

    def get_prep_value(self, value):
        if value is None or value == "":
            return value
        return _get_fernet().encrypt(value.encode("utf-8")).decode("ascii")

    def from_db_value(self, value, expression, connection):
        if value is None or value == "":
            return value
        try:
            return _get_fernet().decrypt(value.encode("ascii")).decode("utf-8")
        except Exception:
            return value  # legacy plaintext

    def to_python(self, value):
        if value is None or value == "":
            return value
        if isinstance(value, str) and not value.startswith("g"):
            return value  # plaintext
        try:
            return _get_fernet().decrypt(value.encode("ascii")).decode("utf-8")
        except Exception:
            return value