from enum import Enum


class TokenPrefix(str, Enum):
    VERIFY_EMAIL = "email"
    PASSWORD_RESET = "reset"
    FORGOT_PASSWORD = "forgot"