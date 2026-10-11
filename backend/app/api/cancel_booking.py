from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services.refund import issue_refund

router = APIRouter(prefix='/api/v1')


# REQ-BR-001
@router.post('/bookings/{booking_id}/cancel')
def cancel_booking(booking_id: str, reason: str = 'customer_cancelled', technician_departed: bool = False):
    if not booking_id:
        raise HTTPException(status_code=400, detail='booking_id is required')

    refund = issue_refund(booking_id, 1500.0, reason, technician_departed=technician_departed)
    message = (
        'Refund processed under BR-01.'
        if refund.amount > 0
        else 'Cancellation is not eligible for a refund; contact call center.'
    )
    return {
        'booking_id': booking_id,
        'refund_amount': refund.amount,
        'rule': refund.rule,
        'status': refund.status,
        'reason': refund.reason,
        'message': message,
    }
