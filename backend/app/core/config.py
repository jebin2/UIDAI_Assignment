import os

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    allowed_origins: list[str] = []

    rsa_private_key_pem: str = ""

    kafka_topic_secure_payload: str = "secure_payload_received"

    rate_limit_capacity: int = 10
    rate_limit_window_seconds: int = 1

    log_file_path: str = ""

    @field_validator("log_file_path")
    @classmethod
    def create_log_directory(cls, v: str) -> str:
        if v:
            os.makedirs(os.path.dirname(v), exist_ok=True)
        return v


settings = Settings()
