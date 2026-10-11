from __future__ import annotations

from app.integrations.payment_gateway import GatewayResult, authorize_and_capture, status_inquiry


# REQ-IF-001, REQ-CON-003
def process_payment(amount: float, timeout_seconds: int = 30, simulate_timeout: bool = False) -> GatewayResult:
    return authorize_and_capture(amount, timeout_seconds=timeout_seconds, simulate_timeout=simulate_timeout)


# REQ-IF-005, REQ-CON-003
def resolve_payment_result(reference: str | None, timeout_seconds: int = 30, simulate_timeout: bool = False) -> GatewayResult:
    if reference:
        return status_inquiry(reference, timeout_seconds=timeout_seconds)
    if simulate_timeout:
        return process_payment(1, timeout_seconds=timeout_seconds, simulate_timeout=True)
    return process_payment(1, timeout_seconds=timeout_seconds, simulate_timeout=False)
