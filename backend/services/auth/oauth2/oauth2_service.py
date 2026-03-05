from authlib.integrations.starlette_client import OAuth
from fastapi import Request, Response
from starlette.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user import User
from services.auth.oauth2.login_or_register_user.service import login_or_register_user
from services.auth.oauth2.SUPPORTED_PROVIDERS import SUPPORTED_PROVIDERS
from services.auth.oauth2.get_users_from_providers import get_user_from_provider
from services.auth.oauth2.register_oauth_providers import register_oauth_providers

config = Config('.env')
oauth = OAuth(config)
register_oauth_providers(SUPPORTED_PROVIDERS, oauth)

async def oauth2_service(db: AsyncSession, response: Response, client, provider: str, request: Request) -> User:
    """Handles full OAuth2 flow: exchanges code, gets user info, and initializes Redis session."""
    normalized_user = await get_user_from_provider(client, provider, request)
    user = await login_or_register_user(db, response, normalized_user)
    return user