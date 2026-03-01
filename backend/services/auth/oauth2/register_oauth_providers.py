from typing import Any, Dict
from core.config import settings
from authlib.integrations.starlette_client import OAuth


def register_oauth_providers(SUPPORTED_PROVIDERS: Dict[str, Dict[str, Any]], oauth: OAuth):
    """Register OAuth providers with the OAuth client."""
    for name, provider_settings in SUPPORTED_PROVIDERS.items():
        client_id = getattr(settings, f"{name.upper()}_CLIENT_ID")
        client_secret = getattr(settings, f"{name.upper()}_CLIENT_SECRET")

        oauth.register(
            name=name,
            client_id=client_id,
            client_secret=client_secret,
            **provider_settings
        )