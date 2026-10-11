from __future__ import annotations

import re
from typing import Any

# REQ-PRV-002, REQ-SEC-004
_SENSITIVE_KEYS = {
    'customer_phone',
    'phone',
    'mobile_phone',
    'geo_point',
    'service_address_geo_point',
    'location',
}


def validate_phone(value: str | None) -> bool:
    if value is None:
        return False
    digits = re.sub(r'\D', '', value)
    return len(digits) >= 8


def mask_phone(value: str | None) -> str:
    if value is None:
        return '***'
    digits = re.sub(r'\D', '', value)
    if len(digits) < 8:
        return '***'
    visible_prefix = digits[:-4]
    return f'{visible_prefix[:3]}***{digits[-4:]}' if visible_prefix else f'***{digits[-4:]}'


def is_sensitive_field(field_name: str) -> bool:
    return str(field_name).lower() in _SENSITIVE_KEYS


def sanitize_for_external_use(value: Any) -> Any:
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        for key, item in value.items():
            if is_sensitive_field(key):
                if str(key).lower() in {'geo_point', 'service_address_geo_point', 'location'}:
                    output[key] = {'lat': '***', 'lon': '***'} if isinstance(item, dict) else '***'
                else:
                    output[key] = mask_phone(item if isinstance(item, str) else str(item))
            else:
                output[key] = sanitize_for_external_use(item)
        return output
    if isinstance(value, list):
        return [sanitize_for_external_use(item) for item in value]
    return value
