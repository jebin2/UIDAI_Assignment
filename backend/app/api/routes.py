import json
import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.models import PayloadAcknowledgement, PublicKeyResponse, SecurePayloadRequest
from app.services.crypto_service import DecryptionError, crypto_service
from app.services.kafka_service import TOPIC_SECURE_PAYLOAD, kafka_producer

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/api/v1/keys/public", response_model=PublicKeyResponse)
async def get_public_key() -> PublicKeyResponse:
    logger.info("PUBLIC_KEY_SERVED")
    return PublicKeyResponse(public_key=crypto_service.get_public_key_pem())


@router.post("/api/v1/sandbox/secure-payload", response_model=PayloadAcknowledgement)
async def receive_secure_payload(payload: SecurePayloadRequest) -> PayloadAcknowledgement:
    partner_id = payload.partner_id
    logger.info("PAYLOAD_RECEIVED partner_id=%s", partner_id)

    logger.info("DECRYPTION_START partner_id=%s", partner_id)
    plaintext = crypto_service.decrypt(payload.encrypted_data)
    logger.info("DECRYPTION_SUCCESS partner_id=%s", partner_id)

    logger.info("PARSING_IDENTITY partner_id=%s", partner_id)
    try:
        identity = json.loads(plaintext.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Decrypted payload is not valid JSON") from exc

    required_fields = {"name", "aadhaar_number", "device_id"}
    missing = required_fields - identity.keys()
    if missing:
        raise ValueError(f"Decrypted payload is missing required fields: {missing}")

    logger.info("IDENTITY_VALID partner_id=%s fields_present=%s", partner_id, sorted(identity.keys()))

    transaction_id = str(uuid.uuid4())
    event = {
        "event": "Secure_Payload_Received",
        "transaction_id": transaction_id,
        "partner_id": partner_id,
        "identity": identity,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }

    logger.info("KAFKA_PUBLISH_START topic=%s transaction_id=%s", TOPIC_SECURE_PAYLOAD, transaction_id)
    kafka_producer.publish(TOPIC_SECURE_PAYLOAD, event)
    logger.info("KAFKA_PUBLISH_SUCCESS topic=%s transaction_id=%s", TOPIC_SECURE_PAYLOAD, transaction_id)

    return PayloadAcknowledgement(
        transaction_id=transaction_id,
        status="accepted",
        message="Payload decrypted and queued successfully.",
    )
