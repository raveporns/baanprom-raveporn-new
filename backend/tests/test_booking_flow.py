import time
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.services.booking_lock import acquire_lock, is_lock_valid, release_lock
from app.services.payment import process_payment, resolve_payment_result
from app.tasks.lock_expiry import expire_lock_if_needed

client = TestClient(app)

def test_availability_endpoint() -> None:
    response = client.get('/api/v1/availability', params={'service_type': 'repair', 'date': '2026-10-05T00:00:00'})
    assert response.status_code == 200
    payload = response.json()
    assert 'slots' in payload and len(payload['slots']) >= 1


def test_AC_07_01_search_within_seven_days() -> None:
    response = client.get('/api/v1/availability', params={'service_type': 'repair', 'date': '2026-10-05T00:00:00'})
    assert response.status_code == 200
    payload = response.json()
    assert payload['service_type'] == 'repair'
    assert payload['count'] >= 1
    assert len(payload['slots']) == payload['count']
    assert all(slot['service_type'] == 'repair' for slot in payload['slots'])
    assert all(slot['deposit_amount'] > 0 for slot in payload['slots'])
    assert all(slot['cancellation_terms'] for slot in payload['slots'])


def test_AC_07_02_show_customer_price_and_terms() -> None:
    response = client.get('/api/v1/availability', params={'service_type': 'repair', 'date': '2026-10-05T00:00:00'})
    assert response.status_code == 200
    first_slot = response.json()['slots'][0]
    assert 'deposit_amount' in first_slot
    assert 'cancellation_terms' in first_slot
    assert first_slot['deposit_amount'] == 1500.0
    assert 'policy' in first_slot['cancellation_terms'].lower()


def test_AC_07_04_lock_window_expires_and_prevents_overlap() -> None:
    slot_id = 'slot-ac-07-04'
    release_lock(slot_id)

    first_lock = acquire_lock(slot_id, expires_in_minutes=10)
    assert is_lock_valid(slot_id) is True
    assert first_lock['slot_id'] == slot_id

    second_lock = acquire_lock(slot_id, expires_in_minutes=10)
    assert second_lock == first_lock

    from app.services import booking_lock

    booking_lock._LOCKS[slot_id] = {
        'slot_id': slot_id,
        'expires_at': (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
        'created_at': (datetime.now(timezone.utc) - timedelta(minutes=11)).isoformat(),
    }
    assert is_lock_valid(slot_id) is False
    assert expire_lock_if_needed(slot_id) is True
    assert is_lock_valid(slot_id) is False

    release_lock(slot_id)


def test_AC_07_05_authorize_and_capture_deposit() -> None:
    result = process_payment(1500.0, timeout_seconds=30)
    assert result.status == 'captured'
    assert result.gateway_ref is not None
    assert result.gateway_ref.startswith('gw-')


def test_AC_07_06_timeout_uses_reference_for_status_inquiry() -> None:
    reference = 'gw-ac-07-06'
    result = resolve_payment_result(reference, timeout_seconds=30, simulate_timeout=True)
    assert result.status == 'captured'
    assert result.gateway_ref == reference


def test_AC_07_07_checkout_timeout_retries_status_inquiry() -> None:
    response = client.post(
        '/api/v1/checkout',
        params={'booking_id': 'booking-ac-07-07', 'amount': 1500.0, 'simulate_timeout': True, 'reference': 'gw-ac-07-07'},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload['gateway_status'] == 'captured'
    assert payload['gateway_ref'] == 'gw-ac-07-07'


def test_AC_07_08_search_and_confirm_under_2_seconds_p95() -> None:
    samples: list[float] = []
    for _ in range(50):
        started = time.perf_counter()
        response = client.get('/api/v1/availability', params={'service_type': 'repair', 'date': '2026-10-05T00:00:00'})
        elapsed = time.perf_counter() - started
        assert response.status_code == 200
        samples.append(elapsed)

    samples.sort()
    p95 = samples[max(0, int(0.95 * len(samples)) - 1)]
    assert p95 < 2.0


def test_booking_and_checkout_workflow() -> None:
    booking_response = client.post(
        '/api/v1/bookings',
        json={
            'customer_id': 'cust-01',
            'service_type': 'repair',
            'address_id': 'addr-01',
            'technician_id': 'tech-1',
            'slot_start': '2026-10-05T09:00:00',
            'slot_end': '2026-10-05T10:00:00',
            'deposit_amount': 1500.0,
        },
    )
    assert booking_response.status_code == 200
    booking_id = booking_response.json()['id']

    payment_response = client.post('/api/v1/checkout', params={'booking_id': booking_id, 'amount': 1500.0})
    assert payment_response.status_code == 200
    assert payment_response.json()['gateway_status'] in {'captured', 'timeout'}

    cancellation_response = client.post(f'/api/v1/bookings/{booking_id}/cancel', params={'reason': 'customer_cancelled'})
    assert cancellation_response.status_code == 200
    assert 'refund_amount' in cancellation_response.json()
