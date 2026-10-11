CREATE TABLE IF NOT EXISTS booking_locks (
    slot_id TEXT PRIMARY KEY,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_booking_locks_expires_at
    ON booking_locks (expires_at);
