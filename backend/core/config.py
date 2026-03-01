from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DOMAIN: str

    REDIS_URL: str

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

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()