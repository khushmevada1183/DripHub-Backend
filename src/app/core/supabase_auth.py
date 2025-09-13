import httpx
from fastapi import Depends
from app.core.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings
from app.core.supabase_client import supabase_client

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_from_supabase(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not creds:
        raise HTTPException(status_code=401, message="Not authenticated")
    token = creds.credentials
    if not settings.SUPABASE_URL:
        raise HTTPException(status_code=500, message="Supabase URL not configured on server")
    try:
        user = await supabase_client.get_user(token)
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=401, message="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, message=f"Supabase error: {e}")
    return user
