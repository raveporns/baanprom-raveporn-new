from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from app.integrations.sms import SmsDelivery, send_sms

logger = logging.getLogger(__name__)


# REQ-FN-012, REQ-IF-002
@dataclass(slots=True)
class JobCreatedEvent:
    job_id: str
    customer_id: str
    technician_id: str
    scheduled_start: datetime
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    trace_id: str = field(default_factory=lambda: f'job-created-{uuid4().hex[:12]}')

    def notification_payloads(self) -> dict[str, str]:
        return {
            'customer': (
                f'Your service booking {self.job_id} is confirmed for {self.scheduled_start.isoformat()}.'
            ),
            'technician': (
                f'New booking {self.job_id} has been confirmed for {self.scheduled_start.isoformat()}.'
            ),
        }

    def deliver_notifications(self) -> list[SmsDelivery]:
        payloads = self.notification_payloads()
        deliveries: list[SmsDelivery] = []
        for recipient_id, message in (
            (self.customer_id, payloads['customer']),
            (self.technician_id, payloads['technician']),
        ):
            started_at = datetime.now(timezone.utc)
            delivery = send_sms(recipient_id, message, channel='sms')
            elapsed_seconds = (datetime.now(timezone.utc) - started_at).total_seconds()
            logger.info(
                'job_created_notification_sent',
                extra={
                    'job_id': self.job_id,
                    'recipient': recipient_id,
                    'trace_id': delivery.trace_id,
                    'sent_at': delivery.sent_at.isoformat(),
                    'elapsed_seconds': elapsed_seconds,
                },
            )
            if elapsed_seconds > 60:
                logger.warning(
                    'job_created_notification_exceeded_60s',
                    extra={
                        'job_id': self.job_id,
                        'recipient': recipient_id,
                        'trace_id': delivery.trace_id,
                        'elapsed_seconds': elapsed_seconds,
                    },
                )
            deliveries.append(delivery)
        return deliveries
