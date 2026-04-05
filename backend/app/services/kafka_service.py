import logging
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)

TOPIC_SECURE_PAYLOAD: str = settings.kafka_topic_secure_payload


class MockKafkaProducer:
    def publish(self, topic: str, event: dict[str, Any]) -> None:
        logger.info(
            "KAFKA_PUBLISH topic=%s event=%s transaction_id=%s partner_id=%s",
            topic,
            event.get("event"),
            event.get("transaction_id"),
            event.get("partner_id"),
        )


kafka_producer = MockKafkaProducer()
