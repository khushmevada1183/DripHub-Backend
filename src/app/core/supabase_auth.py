import httpx
from fastapi import Depends
from app.core.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings
from app.core.supabase_client import supabase_client
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db.repositories.crud_user import get_or_create_by_email, get_user_by_email
from app.core.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_from_supabase(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    """Legacy Supabase auth dependency kept for compatibility. Validates Supabase token and
    returns merged supabase/local user object. Not used by default when backend auth is enabled.
    """
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

    email = sb_user.get("email")
    if not email:
        raise HTTPException(status_code=500, message="Supabase returned user without email")
    local_user = get_or_create_by_email(db, email)

    return {"supabase_user": sb_user, "local_user": {"id": local_user.id, "email": local_user.email}}


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    """Primary auth dependency: accepts local JWTs (issued by this backend).

    Returns the local user model from the database on success.
    """
    if not creds:
        raise HTTPException(status_code=401, message="Not authenticated")
    token = creds.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, message="Invalid or expired token")
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, message="Token missing subject")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, message="User not found")
    return user
