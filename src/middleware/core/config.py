import pydantic as pd
import pydantic_core as pd_core
import pydantic_settings as pd_settings


class Settings(pd_settings.BaseSettings):
    model_config = pd_settings.SettingsConfigDict(
        env_file="../.env",
        extra="ignore",
    )

    DOMAIN: str = "localhost"
    ENVIRONMENT: str = "local"

    @pd.computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    SQLITE_DB_PATH: str | None = None
    TEST_SQLITE_DB_PATH: str | None = None
    PROJECT_NAME: str = "Switchdin Middleware"
    DATABASE_SERVER: str | None = None
    DATABASE_USER: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_NAME: str = ""
    DATABASE_PORT: int | None = None

    @pd.computed_field  # type: ignore[misc]
    @property
    def DATABASE_URI(self) -> pd_core.MultiHostUrl | str:
        if self.SQLITE_DB_PATH:
            return f"sqlite:///{self.SQLITE_DB_PATH}"
        return pd_core.MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_SERVER,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME,
        )

    @pd.computed_field  # type: ignore[misc]
    @property
    def TEST_DATABASE_URI(self) -> pd_core.MultiHostUrl | str:
        return f"sqlite:///{self.TEST_SQLITE_DB_PATH}"

    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"


settings = Settings()  # type: ignore
