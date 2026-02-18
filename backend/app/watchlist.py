from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlmodel import Session, select

from .models import WatchlistEntry, Instrument, User
from .schemas import WatchlistCreate, WatchlistOut
from .db import engine
from .auth import get_current_user

router = APIRouter(prefix="/api/v1/users/me/watchlist", tags=["watchlist"])


def get_db():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=List[WatchlistOut])
def list_watchlist(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return db.exec(
        select(WatchlistEntry).where(WatchlistEntry.user_id == current_user.id)
    ).all()


@router.post("/", response_model=WatchlistOut)
def add_watchlist(
    item: WatchlistCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    # Resolve ticker -> instrument
    inst = db.exec(
        select(Instrument).where(Instrument.ticker == item.ticker)
    ).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instrument not found")
    w = WatchlistEntry(
        user_id=current_user.id,
        instrument_id=inst.id,
        weight=item.weight,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return w
