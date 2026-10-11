from __future__ import annotations

# REQ-BR-001

def calculate_refund(deposit_amount: float, cancelled_reason: str, technician_departed: bool = False) -> float:
    reason = (cancelled_reason or '').strip().lower()

    if technician_departed:
        return 0.0

    if reason in {'customer_cancelled', 'cancelled_by_customer', 'customer_request', 'customer-requested'}:
        return deposit_amount

    if reason in {'contact_call_center', 'call_center', 'manual_review'}:
        return 0.0

    if reason in {'service_not_required', 'reschedule_requested'}:
        return deposit_amount

    return 0.0
