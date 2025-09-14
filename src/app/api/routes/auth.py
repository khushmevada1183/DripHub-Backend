# moved from app.api.api_v1.routers.auth
from fastapi import APIRouter, Depends
from app.core.exceptions import HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.db.session import get_db
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import settings
from app.db.repositories.crud_user import authenticate_user, create_user, get_user_by_email
import logging
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from app.core.supabase_client import supabase_client

router = APIRouter()


@router.post("/login", response_model=schemas.user.Token)
async def login(login_data: schemas.user.UserLogin, db: Session = Depends(get_db)):
    # If Supabase is configured, prefer delegating login to Supabase
    if settings.SUPABASE_URL:
        try:
            resp = await supabase_client.sign_in(login_data.username, login_data.password)
        except Exception as e:
            logging.exception("Supabase sign-in failed")
            raise HTTPException(status_code=500, message=f"Supabase error: {e}")
        status = resp.get("status_code")
        body = resp.get("json")
        if status and status in (200, 201):
            # Supabase returns an object with access_token in session; return it to client
            return {"access_token": body.get("access_token") or body.get("access_token"), "token_type": "bearer"}
        # Map Supabase errors to 400
        raise HTTPException(status_code=400, message=body)

    # Fallback: local DB auth
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=400, message="Incorrect email or password")
    access_token = create_access_token(subject=user.email, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.user.UserWithToken)
async def register(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
    # If Supabase is configured, create the user there and return the Supabase session
    if settings.SUPABASE_URL:
        try:
            resp = await supabase_client.signup(user_in.email, user_in.password)
        except Exception as e:
            logging.exception("Supabase signup failed")
            raise HTTPException(status_code=500, message=f"Supabase error: {e}")
        status = resp.get("status_code")
        body = resp.get("json")
        if status and status in (200, 201):
            # Optionally, create a local user record if you keep local users in your DB
            # We return a simplified UserWithToken mapping if Supabase returned a session
            user_data = body.get("user") or {}
            access_token = body.get("access_token") or body.get("access_token")
            # Map Supabase user to UserRead schema fields if available
            user_read = schemas.user.UserRead(**{k: user_data.get(k) for k in ("id", "email", "is_active", "is_superuser") if user_data.get(k) is not None})
            return schemas.user.UserWithToken(user=user_read, access_token=access_token, token_type="bearer")
        # If Supabase returned an error (e.g., 400 email exists), propagate it
        raise HTTPException(status_code=400, message=body)

    # Fallback: local DB registration
    try:
        existing = get_user_by_email(db, user_in.email)
    except OperationalError:
        logging.exception("Database connection failed when checking existing user")
        raise HTTPException(status_code=503, message="Database unavailable, please try again later")
    except SQLAlchemyError:
        logging.exception("Unexpected database error when checking existing user")
        raise HTTPException(status_code=503, message="Database unavailable, please try again later")
    if existing:
        raise HTTPException(status_code=400, message="Email already registered")
    try:
        user = create_user(db, user_in)
    except SQLAlchemyError as e:
        logging.exception("Failed to create user due to database error")
        raise HTTPException(status_code=503, message="Database unavailable, please try again later")
    access_token = create_access_token(subject=user.email, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return schemas.user.UserWithToken(user=user, access_token=access_token, token_type="bearer")
