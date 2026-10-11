from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

HISTORY_RETENTION_DAYS = 730


# REQ-DAT-002, REQ-FN-012
@dataclass(slots=True)
class Job:
    id: str
    booking_id: str
    status: str = 'confirmed'
    scheduled_start: datetime | None = None
    deposit_amount: float = 0.0
    customer_phone: str | None = None
    service_address_geo_point: dict[str, float] | None = None
    history: list[dict[str, object]] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def add_history(self, event: str, status: str | None = None, at: datetime | None = None) -> dict[str, object]:
        timestamp = at or datetime.now(timezone.utc)
        snapshot = {
            'event': event,
            'state': status if status is not None else self.status,
            'at': timestamp.isoformat(),
        }
        self.history.append(snapshot)
        self.updated_at = timestamp
        return snapshot

    def transition_to(self, new_status: str, event: str, at: datetime | None = None) -> dict[str, object]:
        self.status = new_status
        return self.add_history(event, status=new_status, at=at)

    @property
    def retention_days(self) -> int:
        return HISTORY_RETENTION_DAYS
