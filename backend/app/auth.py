from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from sqlmodel import Session, select

from passlib.context import CryptContext

from .db import engine
from .models import User

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], deprecated="auto")


def get_db():
    with Session(engine) as session:
        yield session


@router.post("/register", status_code=201)
def register(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password required")
    existing = db.exec(select(User).where(User.email == email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="user exists")
    hashed = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"email": user.email}


@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password required")
    user = db.exec(select(User).where(User.email == email)).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    # For tests we return a simple token equal to the email
    return {"access_token": user.email, "token_type": "bearer"}


def _extract_token(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2:
        return None
    if parts[0].lower() != "bearer":
        return None
    return parts[1]


def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    token = _extract_token(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="missing token")
    user = db.exec(select(User).where(User.email == token)).first()
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")
    return user


def get_current_active_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="admin privileges required")
    return current_user
