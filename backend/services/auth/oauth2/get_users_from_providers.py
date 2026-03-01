from typing import Any, Dict
from fastapi import HTTPException, Request

async def get_user_from_provider(client, provider: str, request: Request) -> Dict[str, Any]:
    try:
        token = await client.authorize_access_token(request)
    except Exception:
        raise HTTPException(500, detail='Tokens don\'t match, please try again.')
    user = token.get('userinfo')

    if not user:
        if provider == "github":
            response = await client.get('user', token=token)
            user = response.json()
        elif provider == "facebook":
            response = await client.get('me?fields=id,name,email', token=token)
            user = response.json()
            
    return _normalize_data(provider, user)

def _normalize_data(provider: str, raw_user: Dict[str, Any]) -> Dict[str, Any]:
    uid = raw_user.get("sub") or raw_user.get("id")
    return {
        'uid': str(uid),
        'email': raw_user.get("email"),
        'provider': provider
    }