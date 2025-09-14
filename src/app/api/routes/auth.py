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

router = APIRouter()


@router.post("/login", response_model=schemas.user.Token)
def login(login_data: schemas.user.UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=400, message="Incorrect email or password")
    access_token = create_access_token(subject=user.email, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.user.UserWithToken)
def register(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
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
