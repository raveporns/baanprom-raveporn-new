from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# REQ-DAT-002, REQ-SEC-004, REQ-PRV-002
class TimeSlotSchema(BaseModel):
    id: str
    technician_id: str
    start: datetime
    end: datetime
    state: Literal['available', 'locked', 'booked'] = 'available'
    hold_expires_at: datetime | None = None
    customer_phone: str | None = None
    service_address_geo_point: dict[str, float] | None = None


class PaymentSchema(BaseModel):
    id: str
    booking_id: str
    amount: float = Field(..., gt=0)
    result: Literal['pending', 'authorized', 'captured', 'timeout', 'failed'] = 'pending'
    gateway_ref: str | None = None
    timeout_seconds: int = 30


class RefundSchema(BaseModel):
    id: str
    booking_id: str
    amount: float = Field(..., ge=0)
    rule: str = 'BR-01'
    status: Literal['pending', 'processed'] = 'pending'
    reason: str | None = None


class JobSchema(BaseModel):
    id: str
    booking_id: str
    status: str = 'confirmed'
    scheduled_start: datetime | None = None
    deposit_amount: float = 0.0
    customer_phone: str | None = None
    service_address_geo_point: dict[str, float] | None = None
    history: list[dict[str, object]] = Field(default_factory=list)


# REQ-FN-008
class AvailabilitySlot(BaseModel):
    slot_id: str
    technician_id: str
    service_type: str = 'repair'
    address_id: str = 'default-address'
    start: datetime
    end: datetime
    available: bool = True
    deposit_amount: float = 0.0
    cancellation_terms: str = 'Refund follows the published cancellation policy for this booking.'


class BookingCreateRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    service_type: str = Field(..., min_length=1)
    address_id: str = Field(..., min_length=1)
    technician_id: str = Field(..., min_length=1)
    slot_start: datetime
    slot_end: datetime
    deposit_amount: float = Field(default=0.0, ge=0)


class BookingResponse(BaseModel):
    id: str
    customer_id: str
    technician_id: str
    service_type: str
    address_id: str
    slot_start: datetime
    slot_end: datetime
    deposit_amount: float
    status: str


class PaymentRequest(BaseModel):
    booking_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    gateway_ref: str | None = None


class CancelRequest(BaseModel):
    booking_id: str = Field(..., min_length=1)
    reason: str = 'customer_cancelled'


class Notification(BaseModel):
    recipient: str
    channel: Literal['sms', 'email']
    message: str
