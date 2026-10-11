from __future__ import annotations

import re
from typing import Any

# REQ-PRV-002, REQ-SEC-004

def mask_phone(value: str | None) -> str:
    if value is None:
        return '***'
    digits = re.sub(r'\D', '', value)
    if len(digits) < 8:
        return '***'
    visible_prefix = digits[:-4]
    return f'{visible_prefix[:3]}***{digits[-4:]}' if visible_prefix else f'***{digits[-4:]}'


def sanitize_for_log(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered in {'customer_phone', 'phone', 'mobile_phone'}:
                sanitized[key] = mask_phone(item if isinstance(item, str) else str(item))
            elif lowered in {'geo_point', 'service_address_geo_point', 'location'}:
                sanitized[key] = {'lat': '***', 'lon': '***'} if isinstance(item, dict) else '***'
            else:
                sanitized[key] = sanitize_for_log(item)
        return sanitized
    if isinstance(value, list):
        return [sanitize_for_log(item) for item in value]
    if isinstance(value, str):
        if re.search(r'\d{8,}', value):
            return mask_phone(value)
        return value
    return value
