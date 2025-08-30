from fastapi import APIRouter, Depends
from app.core.exceptions import HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db.session import get_db
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=schemas.user.Token)
def login(login_data: schemas.user.UserLogin, db: Session = Depends(get_db)):
    user = crud.crud_user.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=400, message="Incorrect email or password")
    access_token = create_access_token(subject=user.email, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.user.UserRead)
def register(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
    existing = crud.crud_user.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, message="Email already registered")
    user = crud.crud_user.create_user(db, user_in)
    return user
