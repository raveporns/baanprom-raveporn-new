CREATE TABLE IF NOT EXISTS time_slots (
    id TEXT PRIMARY KEY,
    technician_id TEXT NOT NULL,
    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ NOT NULL,
    state TEXT NOT NULL DEFAULT 'available',
    hold_expires_at TIMESTAMPTZ,
    customer_phone TEXT,
    service_address_geo_point JSONB
);

CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    booking_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'confirmed',
    scheduled_start TIMESTAMPTZ,
    deposit_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    customer_phone TEXT,
    service_address_geo_point JSONB,
    history JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    booking_id TEXT NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    result TEXT NOT NULL DEFAULT 'pending',
    gateway_ref TEXT,
    timeout_seconds INTEGER NOT NULL DEFAULT 30,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS refunds (
    id TEXT PRIMARY KEY,
    booking_id TEXT NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    rule TEXT NOT NULL DEFAULT 'BR-01',
    status TEXT NOT NULL DEFAULT 'pending',
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
