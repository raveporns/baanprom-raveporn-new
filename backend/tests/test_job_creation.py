from datetime import datetime, timezone

from app.models.booking import Booking
from app.models.job import Job
from app.repositories.job_repository import create_job_from_booking, get_job


def test_AC_07_03_create_confirmed_job_and_history() -> None:
    booking = Booking(
        id='booking-0001',
        customer_id='cust-01',
        technician_id='tech-01',
        service_type='repair',
        address_id='addr-01',
        slot_start=datetime(2026, 10, 5, 9, 0, tzinfo=timezone.utc),
        slot_end=datetime(2026, 10, 5, 10, 0, tzinfo=timezone.utc),
        deposit_amount=1500.0,
    )

    job = create_job_from_booking(booking.id, scheduled_start=booking.slot_start, deposit_amount=booking.deposit_amount)

    assert job.status == 'confirmed'
    assert job.booking_id == booking.id
    assert job.scheduled_start == booking.slot_start
    assert job.deposit_amount == 1500.0
    assert job.history[-1]['event'] == 'created'
    assert job.history[-1]['state'] == 'confirmed'
    assert job.retention_days == 730
    assert get_job(job.id) is not None


def test_job_transition_records_status_history() -> None:
    booking = Booking(
        id='booking-0002',
        customer_id='cust-02',
        technician_id='tech-02',
        service_type='repair',
        address_id='addr-02',
        slot_start=datetime(2026, 10, 6, 9, 0, tzinfo=timezone.utc),
        slot_end=datetime(2026, 10, 6, 10, 0, tzinfo=timezone.utc),
        deposit_amount=1500.0,
    )

    job = create_job_from_booking(booking.id, scheduled_start=booking.slot_start, deposit_amount=booking.deposit_amount)
    job.transition_to('in_progress', 'started_work')

    assert job.status == 'in_progress'
    assert job.history[-1]['event'] == 'started_work'
    assert job.history[-1]['state'] == 'in_progress'
