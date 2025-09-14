from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.user.User).filter(models.user.User.email == email).first()

def create_user(db: Session, user_in: schemas.user.UserCreate):
    hashed = get_password_hash(user_in.password)
    db_user = models.user.User(email=user_in.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_or_create_by_email(db: Session, email: str):
    """Find a local user by email or create a lightweight local record.

    Local records created this way will have an empty `hashed_password` because
    authentication is delegated to Supabase. This keeps local relations (orders,
    products) working while Supabase remains the single auth source.
    """
    user = get_user_by_email(db, email)
    if user:
        return user
    # Create a minimal local user. hashed_password is set to empty string since
    # Supabase manages passwords.
    db_user = models.user.User(email=email, hashed_password="")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
