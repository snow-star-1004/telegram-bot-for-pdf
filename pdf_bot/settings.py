from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env.test", ".env"
        env_file_encoding = "utf-8"

    telegram_token: str = Field(..., env="telegram_token")
    slack_token: str = Field(..., env="slack_token")
    stripe_token: str = Field(..., env="stripe_token")
    google_fonts_token: str = Field(..., env="google_fonts_token")
    ga_api_secret: str = Field(..., env="ga_api_secret")
    ga_measurement_id: str = Field(..., env="ga_measurement_id")
    gcp_service_account: dict = Field(..., env="gcp_service_account")

    admin_telegram_id: int = Field(..., env="admin_telegram_id")

    app_url: str | None = Field(default=None, env="app_url")
    port: int = Field(default=8443, env="port")

    request_connection_pool_size: int = 8
    request_read_timeout: int = 45
    request_write_timeout: int = 45
    request_connect_timeout: int = 45
    request_pool_timeout: int = 45

    sentry_dsn: str | None = Field(env="sentry_dsn")
