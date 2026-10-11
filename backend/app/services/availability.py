from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.schemas.booking import AvailabilitySlot


# REQ-FN-008
def get_available_slots(service_type: str, date: str | None = None, days_ahead: int = 7) -> list[AvailabilitySlot]:
    parsed = datetime.fromisoformat(date) if date else datetime.now(timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    base_day = parsed.astimezone(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    slots: list[AvailabilitySlot] = []
    deposit_amount = 1500.0 if service_type.lower() == 'repair' else 1200.0
    for day in range(days_ahead):
        current_day = base_day + timedelta(days=day)
        for offset, start_hour in enumerate((9, 13, 16)):
            start = current_day + timedelta(hours=start_hour)
            end = start + timedelta(hours=1)
            slots.append(
                AvailabilitySlot(
                    slot_id=f'{service_type}-{day}-{offset}',
                    technician_id=f'tech-{(day + offset) % 3 + 1}',
                    service_type=service_type,
                    address_id=f'addr-{(day + offset) % 4 + 1}',
                    start=start,
                    end=end,
                    available=True,
                    deposit_amount=deposit_amount,
                    cancellation_terms='Deposit is refundable under the published cancellation policy for this service.',
                )
            )
    return slots
