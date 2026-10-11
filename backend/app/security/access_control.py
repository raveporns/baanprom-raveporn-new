from __future__ import annotations

from datetime import datetime, timedelta


# REQ-SEC-004, REQ-PRV-002
def can_technician_view_customer_phone(job_time: datetime | None, current_time: datetime | None = None) -> bool:
    if job_time is None:
        return False
    current = current_time or datetime.utcnow()
    window_start = job_time - timedelta(hours=2)
    window_end = job_time + timedelta(hours=2)
    return window_start <= current <= window_end
