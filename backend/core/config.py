import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DOMAIN: str

    REDIS_HOST: str
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:6379/0"

    DB_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    @property
    def DB_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    MIDDLEWARE_SECRET_KEY: str
    COOKIE_SECURE: bool

    USER_COOKIE_SESSION_TTL: int
    USER_REDIS_SESSION_TTL: int
    ACCOUNT_REDIS_SESSION_TTL: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str

    model_config = SettingsConfigDict(env_file='../.env' if os.path.exists("../.env") else None, extra='ignore')

settings = Settings()