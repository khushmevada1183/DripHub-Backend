from fastapi import APIRouter, Depends
from app.core.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import crud, schemas
from app.core.supabase_auth import get_current_user_from_supabase

router = APIRouter()

@router.get("/me")
def read_users_me(current_user = Depends(get_current_user_from_supabase)):
    # current_user is the JSON user object from Supabase; map to a schema or return directly
    return current_user
