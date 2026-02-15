import re
from datetime import datetime

PHONE_REGEX = r"^\+2507[2-9]\d{7}$"

def validate_rwanda_phone(phone: str) -> bool:
    return bool(phone and re.match(PHONE_REGEX, str(phone).strip()))


def validate_nid(nid: str) -> bool:
    if not nid or not nid.isdigit() or len(nid) != 16 or not nid.startswith("1"):
        return False
    # Birth year consistency: digits 8–11 often encode YYYY (e.g. 1990)
    try:
        year = int(nid[7:11])
        return 1900 <= year <= datetime.now().year
    except (ValueError, IndexError):
        return False
