from fastapi import APIRouter, Depends
from typing import List, Annotated
from sqlmodel import Session, select

from .models import Preference, User
from .schemas import PreferenceCreate, PreferenceOut
from .db import engine
from .auth import get_current_user

router = APIRouter(prefix="/api/v1/users/me/preferences", tags=["preferences"])


def get_db():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=List[PreferenceOut])
def list_preferences(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return db.exec(
        select(Preference).where(Preference.user_id == current_user.id)
    ).all()


@router.post("/", response_model=PreferenceOut)
def add_preference(
    payload: PreferenceCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    pref = Preference(
        user_id=current_user.id,
        tag_id=payload.tag_id,
        type=payload.type,
        strength=payload.strength,
    )
    db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref
