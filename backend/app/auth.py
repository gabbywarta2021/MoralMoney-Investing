from datetime import datetime, timedelta
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session, select

from .models import User
from .schemas import UserCreate, Token
from . import db

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
SECRET_KEY = "change-this-secret"  # TODO: load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire_delta = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception from None
    with Session(db.engine) as session:
        user = session.get(User, int(sub)) if sub is not None else None
        if not user:
            raise credentials_exception
        return user


def get_current_active_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


@router.post("/register", status_code=201, response_model=dict)
def register(payload: UserCreate):
    with Session(db.engine) as session:
        stmt = select(User).where(User.email == payload.email)
        existing = session.exec(stmt).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(
            email=payload.email,
            hashed_password=get_password_hash(payload.password),
            risk_level=payload.risk_level,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"id": user.id, "email": user.email, "risk_level": user.risk_level}


@router.post("/login", response_model=Token)
def login(payload: UserCreate):
    with Session(db.engine) as session:
        stmt = select(User).where(User.email == payload.email)
        user = session.exec(stmt).first()
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
        })
        return {"access_token": token, "token_type": "bearer"}
