import httpx
from fastapi import Depends
from app.core.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings
from app.core.supabase_client import supabase_client
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db.repositories.crud_user import get_or_create_by_email

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_from_supabase(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    if not creds:
        raise HTTPException(status_code=401, message="Not authenticated")
    token = creds.credentials
    if not settings.SUPABASE_URL:
        raise HTTPException(status_code=500, message="Supabase URL not configured on server")
    try:
        sb_user = await supabase_client.get_user(token)
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=401, message="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, message=f"Supabase error: {e}")

    # Ensure a local user exists for relational data (orders/products). This creates
    # a minimal user row if none exists yet. Authentication remains delegated to Supabase.
    email = sb_user.get("email")
    if not email:
        raise HTTPException(status_code=500, message="Supabase returned user without email")
    local_user = get_or_create_by_email(db, email)

    # Return a merged object with both Supabase user and local_id for convenience
    merged = {"supabase_user": sb_user, "local_user": {"id": local_user.id, "email": local_user.email}}
    return merged
