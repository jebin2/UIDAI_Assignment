from pydantic import BaseModel


class SecurePayloadRequest(BaseModel):
    encrypted_data: str
    partner_id: str


class PublicKeyResponse(BaseModel):
    public_key: str


class PayloadAcknowledgement(BaseModel):
    transaction_id: str
    status: str
    message: str
