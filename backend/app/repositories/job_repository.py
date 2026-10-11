from __future__ import annotations

from datetime import datetime, timezone

from app.models.job import Job

_ACTIVE_JOBS: dict[str, Job] = {}


# REQ-DAT-002, REQ-FN-012
def create_job_from_booking(booking_id: str, *, scheduled_start: datetime | None, deposit_amount: float = 0.0) -> Job:
    job = Job(
        id=f'job-{booking_id}',
        booking_id=booking_id,
        status='confirmed',
        scheduled_start=scheduled_start,
        deposit_amount=deposit_amount,
    )
    job.add_history('created', status='confirmed')
    _ACTIVE_JOBS[job.id] = job
    return job


def get_job(job_id: str) -> Job | None:
    return _ACTIVE_JOBS.get(job_id)


def list_jobs() -> list[Job]:
    return list(_ACTIVE_JOBS.values())


def append_status_history(job_id: str, event: str, new_status: str, at: datetime | None = None) -> Job | None:
    job = _ACTIVE_JOBS.get(job_id)
    if job is None:
        return None
    job.transition_to(new_status, event, at=at or datetime.now(timezone.utc))
    return job
