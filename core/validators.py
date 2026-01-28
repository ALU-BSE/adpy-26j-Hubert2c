import re

PHONE_REGEX = r"^\+2507[2-9]\d{7}$"

def validate_rwanda_phone(phone: str) -> bool:
    return bool(re.match(PHONE_REGEX, phone))


def validate_nid(nid: str) -> bool:
    return nid.isdigit() and len(nid) == 16 and nid.startswith("1")
