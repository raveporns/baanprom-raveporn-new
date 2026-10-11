from __future__ import annotations

from app.models.booking import Booking
from app.models.job import Job
from app.repositories.job_repository import create_job_from_booking as repo_create_job_from_booking


# REQ-DAT-002, REQ-FN-012
def create_job_from_booking(booking: Booking) -> Job:
    return repo_create_job_from_booking(
        booking.id,
        scheduled_start=booking.slot_start,
        deposit_amount=booking.deposit_amount,
    )
