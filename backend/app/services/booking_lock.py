from __future__ import annotations

from datetime import datetime, timedelta, timezone

DEFAULT_LOCK_MINUTES = 10
_LOCKS: dict[str, dict] = {}


# REQ-FN-041, Q-18
def acquire_lock(slot_id: str, expires_in_minutes: int = DEFAULT_LOCK_MINUTES) -> dict:
    existing_lock = _LOCKS.get(slot_id)
    if existing_lock and is_lock_valid(slot_id):
        return existing_lock

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
    lock = {'slot_id': slot_id, 'expires_at': expires_at.isoformat(), 'created_at': datetime.now(timezone.utc).isoformat()}
    _LOCKS[slot_id] = lock
    return lock


def is_lock_valid(slot_id: str) -> bool:
    lock = _LOCKS.get(slot_id)
    if not lock:
        return False

    expires_at = datetime.fromisoformat(lock['expires_at'])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= datetime.now(timezone.utc):
        _LOCKS.pop(slot_id, None)
        return False
    return True


def release_lock(slot_id: str) -> None:
    _LOCKS.pop(slot_id, None)
