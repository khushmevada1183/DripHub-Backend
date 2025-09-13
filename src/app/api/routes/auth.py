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
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, message="Email already registered")
    user = create_user(db, user_in)
    access_token = create_access_token(subject=user.email, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return schemas.user.UserWithToken(user=user, access_token=access_token, token_type="bearer")
