from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.models.booking import Booking
from app.schemas.booking import BookingCreateRequest, BookingResponse
from app.services.availability import get_available_slots
from app.services.booking_lock import acquire_lock, is_lock_valid

router = APIRouter(prefix='/api/v1')

_BOOKINGS: dict[str, Booking] = {}


# REQ-FN-008
@router.get('/availability')
def get_booking_availability(service_type: str = 'repair', date: str | None = None, address_id: str | None = None):
    slots = get_available_slots(service_type, date=date, days_ahead=7)
    return {
        'service_type': service_type,
        'address_id': address_id or 'default-address',
        'available_from': slots[0].start.isoformat() if slots else None,
        'available_to': slots[-1].end.isoformat() if slots else None,
        'count': len(slots),
        'slots': [slot.model_dump(mode='json') for slot in slots],
    }


@router.post('/bookings', response_model=BookingResponse)
def create_booking(payload: BookingCreateRequest):
    slot_key = payload.technician_id
    if not is_lock_valid(slot_key):
        acquire_lock(slot_key, expires_in_minutes=10)
    elif not payload.slot_start:
        raise HTTPException(status_code=400, detail='slot_start is required')

    booking = Booking(
        id=f'booking-{len(_BOOKINGS) + 1:04d}',
        customer_id=payload.customer_id,
        technician_id=payload.technician_id,
        service_type=payload.service_type,
        address_id=payload.address_id,
        slot_start=payload.slot_start,
        slot_end=payload.slot_end,
        deposit_amount=payload.deposit_amount,
        status='confirmed',
    )
    _BOOKINGS[booking.id] = booking
    return BookingResponse(
        id=booking.id,
        customer_id=booking.customer_id,
        technician_id=booking.technician_id,
        service_type=booking.service_type,
        address_id=booking.address_id,
        slot_start=booking.slot_start,
        slot_end=booking.slot_end,
        deposit_amount=booking.deposit_amount,
        status=booking.status,
    )


@router.get('/bookings/{booking_id}', response_model=BookingResponse)
def get_booking(booking_id: str):
    booking = _BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')
    return BookingResponse(
        id=booking.id,
        customer_id=booking.customer_id,
        technician_id=booking.technician_id,
        service_type=booking.service_type,
        address_id=booking.address_id,
        slot_start=booking.slot_start,
        slot_end=booking.slot_end,
        deposit_amount=booking.deposit_amount,
        status=booking.status,
    )
