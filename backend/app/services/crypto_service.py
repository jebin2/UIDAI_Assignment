import base64
import logging

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from app.core.config import settings

logger = logging.getLogger(__name__)


class CryptoService:
    def __init__(self) -> None:
        if settings.rsa_private_key_pem:
            logger.info("CryptoService: loading RSA private key from config")
            self._private_key: RSAPrivateKey = serialization.load_pem_private_key(
                settings.rsa_private_key_pem.encode("utf-8"),
                password=None,
            )
        else:
            logger.warning("CryptoService: RSA_PRIVATE_KEY_PEM not set - generating a temporary mock keypair")
            self._private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
        self._public_key: RSAPublicKey = self._private_key.public_key()

    def get_public_key_pem(self) -> str:
        return self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    def decrypt(self, ciphertext_b64: str) -> bytes:
        try:
            ciphertext = base64.b64decode(ciphertext_b64)
        except Exception as exc:
            logger.warning("DECRYPT_BASE64_ERROR ciphertext_len=%s", len(ciphertext_b64))
            raise ValueError("encrypted_data is not valid base-64") from exc

        try:
            plaintext = self._private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
        except (ValueError, TypeError) as exc:
            logger.warning("DECRYPT_RSA_ERROR ciphertext_bytes=%s", len(ciphertext))
            raise DecryptionError("RSA decryption failed") from exc

        logger.info("DECRYPT_OK plaintext_bytes=%s", len(plaintext))
        return plaintext


class DecryptionError(Exception):
    pass


crypto_service = CryptoService()
