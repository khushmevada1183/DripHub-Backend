# moved from app.api.api_v1.routers.users
from fastapi import APIRouter, Depends
from app.core.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import schemas
from app.core.supabase_auth import get_current_user

router = APIRouter()

@router.get("/me")
def read_users_me(current_user = Depends(get_current_user)):
    # current_user is the local DB user model
    return {"id": current_user.id, "email": current_user.email, "is_active": current_user.is_active}
