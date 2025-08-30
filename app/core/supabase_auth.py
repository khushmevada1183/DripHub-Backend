import os
import httpx
from fastapi import Depends
from app.core.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user_from_supabase(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not creds:
        raise HTTPException(status_code=401, message="Not authenticated")
    token = creds.credentials
    if not settings.SUPABASE_URL:
        raise HTTPException(status_code=500, message="Supabase URL not configured on server")
    # Prefer using the anon/public key for normal token verification (safer).
    apikey = settings.SUPABASE_ANON_KEY or settings.SUPABASE_SERVICE_ROLE_KEY
    if not apikey:
        raise HTTPException(status_code=500, message="No Supabase API key (anon or service_role) configured on server")
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": apikey,
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{settings.SUPABASE_URL}/auth/v1/user", headers=headers, timeout=10.0)
    if r.status_code != 200:
        raise HTTPException(status_code=401, message="Invalid token")
    user = r.json()
    return user
