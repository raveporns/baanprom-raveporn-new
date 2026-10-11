from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


# REQ-FN-012, REQ-IF-002
@dataclass(slots=True)
class SmsDelivery:
    recipient: str
    channel: str
    status: str
    trace_id: str
    sent_at: datetime
    message: str


def send_sms(recipient: str, message: str, *, channel: str = 'sms') -> SmsDelivery:
    sent_at = datetime.now(timezone.utc)
    return SmsDelivery(
        recipient=recipient,
        channel=channel,
        status='sent',
        trace_id=f'sms-{uuid4().hex[:12]}',
        sent_at=sent_at,
        message=message,
    )
