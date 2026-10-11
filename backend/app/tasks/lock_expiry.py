from __future__ import annotations

from app.services import booking_lock
from app.services.booking_lock import is_lock_valid, release_lock


# REQ-FN-041
def expire_lock_if_needed(slot_id: str) -> bool:
    if not is_lock_valid(slot_id):
        release_lock(slot_id)
        return True
    return False


# REQ-FN-041
def expire_all_locks() -> list[str]:
    expired: list[str] = []
    for slot_id in list(booking_lock._LOCKS):
        if not is_lock_valid(slot_id):
            release_lock(slot_id)
            expired.append(slot_id)
    return expired
