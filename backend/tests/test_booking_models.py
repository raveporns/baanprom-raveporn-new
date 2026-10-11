from datetime import datetime, timedelta, timezone

from app.models.booking import Job, TimeSlot
from app.security.access_control import can_technician_view_customer_phone
from app.services.security import sanitize_for_log


def test_AC_07_04_time_slot_history_and_lock_expiry() -> None:
    scheduled_start = datetime(2026, 10, 5, 9, 0, tzinfo=timezone.utc)
    slot = TimeSlot(
        id='slot-42',
        technician_id='tech-1',
        start=scheduled_start,
        end=scheduled_start + timedelta(hours=1),
        state='locked',
        hold_expires_at=scheduled_start + timedelta(minutes=10),
    )
    job = Job(
        id='job-42',
        booking_id='booking-42',
        status='confirmed',
        scheduled_start=scheduled_start,
        deposit_amount=1500.0,
    )

    job.add_history('created')

    assert slot.state == 'locked'
    assert slot.status == 'locked'
    assert slot.lock_expires_at == slot.hold_expires_at
    assert job.history[-1]['state'] == 'confirmed'
    assert job.history[-1]['event'] == 'created'


def test_AC_07_09_customer_phone_redaction_and_access_window() -> None:
    scheduled_start = datetime(2026, 10, 5, 9, 0, tzinfo=timezone.utc)
    assert can_technician_view_customer_phone(scheduled_start, scheduled_start)
    assert not can_technician_view_customer_phone(scheduled_start, scheduled_start - timedelta(days=1))

    payload = {
        'customer_phone': '0912345678',
        'service_address_geo_point': {'lat': 13.736717, 'lon': 100.523186},
    }
    sanitized = sanitize_for_log(payload)

    assert sanitized['customer_phone'] != '0912345678'
    assert '0912345678' not in str(sanitized)
    assert sanitized['service_address_geo_point'] == {'lat': '***', 'lon': '***'}
