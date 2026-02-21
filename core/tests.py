from django.test import TestCase
from .validators import validate_rwanda_phone, validate_nid

class ValidatorTests(TestCase):

    def test_valid_rwanda_phone(self):
        self.assertTrue(validate_rwanda_phone("+250788123456"))

    def test_invalid_rwanda_phone(self):
        self.assertFalse(validate_rwanda_phone("0788123456"))

    def test_valid_nid(self):
        self.assertTrue(validate_nid("1199887766554433"))

    def test_invalid_nid(self):
        self.assertFalse(validate_nid("ABC123"))
