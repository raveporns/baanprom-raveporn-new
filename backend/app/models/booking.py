from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


# REQ-DAT-002, REQ-SEC-004, REQ-PRV-002
@dataclass(slots=True)
class TimeSlot:
    id: str
    technician_id: str
    start: datetime
    end: datetime
    state: Literal['available', 'locked', 'booked'] = 'available'
    hold_expires_at: datetime | None = None
    customer_phone: str | None = None
    service_address_geo_point: dict[str, float] | None = None

    @property
    def status(self) -> str:
        return self.state

    @status.setter
    def status(self, value: str) -> None:
        self.state = value

    @property
    def lock_expires_at(self) -> datetime | None:
        return self.hold_expires_at

    @lock_expires_at.setter
    def lock_expires_at(self, value: datetime | None) -> None:
        self.hold_expires_at = value


# REQ-FN-008, REQ-DAT-002
@dataclass(slots=True)
class Booking:
    id: str
    customer_id: str
    technician_id: str
    service_type: str
    address_id: str
    slot_start: datetime
    slot_end: datetime
    deposit_amount: float
    status: str = 'pending_confirmation'
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# REQ-IF-001, REQ-IF-005
@dataclass(slots=True)
class Payment:
    id: str
    booking_id: str
    amount: float
    result: Literal['pending', 'authorized', 'captured', 'timeout', 'failed'] = 'pending'
    gateway_ref: str | None = None
    timeout_seconds: int = 30

    @property
    def status(self) -> str:
        return self.result

    @status.setter
    def status(self, value: str) -> None:
        self.result = value


# REQ-BR-001
@dataclass(slots=True)
class Refund:
    id: str
    booking_id: str
    amount: float
    rule: str = 'BR-01'
    status: Literal['pending', 'processed'] = 'pending'
    reason: str | None = None


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

    def add_history(self, event: str, at: datetime | None = None) -> None:
        ts = at or datetime.now(timezone.utc)
        self.history.append({
            'event': event,
            'state': self.status,
            'at': ts.isoformat(),
        })
