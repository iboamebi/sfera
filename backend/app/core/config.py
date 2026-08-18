from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://sphere:sphere@localhost/sphere"
    AUTH_COOKIE_NAME: str = "sfera_session"
    AUTH_COOKIE_SECURE: bool = False
    AUTH_COOKIE_SAMESITE: str = "lax"
    AUTH_SESSION_TTL_SECONDS: int = 60 * 60 * 12

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
