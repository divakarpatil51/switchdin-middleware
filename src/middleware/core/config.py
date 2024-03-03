from typing import Any

from pydantic import (
    AnyHttpUrl,
    PostgresDsn,
    ValidationInfo,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | str = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Switchdin Middleware"
    # TODO: Hardcode details for now.. use env file if time permits
    POSTGRES_SERVER: str = "0.0.0.0"
    POSTGRES_USER: str = "dev"
    POSTGRES_PASSWORD: str = "pass"
    POSTGRES_DB: str = "dev"
    POSTGRES_HOST: int = 5438
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            port=info.data.get("POSTGRES_HOST"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
