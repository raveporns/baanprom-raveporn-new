from __future__ import annotations

import logging
from datetime import datetime, timezone

from app.events.job_created import JobCreatedEvent
from app.integrations.sms import SmsDelivery, send_sms

logger = logging.getLogger(__name__)


# REQ-FN-012, REQ-IF-002
def send_notifications(
    recipient_customer: str | JobCreatedEvent,
    recipient_technician: str | None = None,
    message_customer: str | None = None,
    message_technician: str | None = None,
) -> list[SmsDelivery]:
    if isinstance(recipient_customer, JobCreatedEvent):
        return recipient_customer.deliver_notifications()

    if recipient_technician is None or message_customer is None or message_technician is None:
        raise ValueError('customer/technician recipient and message payloads are required')

    deliveries = [
        send_sms(recipient_customer, message_customer, channel='sms'),
        send_sms(recipient_technician, message_technician, channel='sms'),
    ]
    for delivery in deliveries:
        logger.info(
            'job_created_notification_sent',
            extra={
                'recipient': delivery.recipient,
                'trace_id': delivery.trace_id,
                'sent_at': delivery.sent_at.isoformat(),
                'status': delivery.status,
            },
        )
    return deliveries
