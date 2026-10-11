from __future__ import annotations

from datetime import datetime
from typing import Any

from app.security.access_control import can_technician_view_customer_phone
from app.validators.pii import mask_phone, sanitize_for_external_use


# REQ-SEC-004, REQ-PRV-002
def get_customer_profile_for_technician(
    customer_id: str,
    customer_phone: str | None,
    scheduled_start: datetime | None,
    current_time: datetime | None = None,
    *,
    include_geo: bool = False,
    service_address_geo_point: dict[str, float] | None = None,
) -> dict[str, Any]:
    profile: dict[str, Any] = {
        'customer_id': customer_id,
        'customer_phone': mask_phone(customer_phone),
    }
    if include_geo:
        profile['service_address_geo_point'] = service_address_geo_point
    carry_phone = bool(
        scheduled_start is not None
        and can_technician_view_customer_phone(scheduled_start, current_time)
    )
    if carry_phone:
        profile['customer_phone'] = customer_phone or '***'
    if service_address_geo_point is not None and not include_geo:
        profile['service_address_geo_point'] = {'lat': '***', 'lon': '***'}
    return profile


def get_external_customer_profile(profile: dict[str, Any]) -> dict[str, Any]:
    return sanitize_for_external_use(profile)
