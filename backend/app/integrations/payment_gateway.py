from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class GatewayResult:
    status: str
    gateway_ref: str | None = None
    message: str = ''


def _make_gateway_reference() -> str:
    return f'gw-{datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")}'


# REQ-IF-001, REQ-IF-005, REQ-CON-003
def authorize_and_capture(amount: float, timeout_seconds: int = 30, simulate_timeout: bool = False) -> GatewayResult:
    if amount <= 0:
        return GatewayResult(status='failed', gateway_ref=None, message='amount must be greater than zero')

    reference = _make_gateway_reference()
    if simulate_timeout:
        return GatewayResult(
            status='timeout',
            gateway_ref=reference,
            message=f'Gateway timeout after {timeout_seconds} seconds; retry status inquiry with reference {reference}',
        )

    return GatewayResult(
        status='captured',
        gateway_ref=reference,
        message='Payment authorized and captured successfully',
    )


# REQ-IF-001, REQ-IF-005, REQ-CON-003
def status_inquiry(reference: str, timeout_seconds: int = 30) -> GatewayResult:
    if not reference:
        return GatewayResult(status='not_found', gateway_ref=None, message='Missing reference')

    return GatewayResult(
        status='captured',
        gateway_ref=reference,
        message=f'Status inquiry succeeded within {timeout_seconds} seconds',
    )
