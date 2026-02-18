from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Annotated
from sqlmodel import Session, select

from .models import Instrument
from .schemas import InstrumentCreate, InstrumentOut
from .db import engine

router = APIRouter(prefix="/api/v1/instruments", tags=["instruments"])


def get_db():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=List[InstrumentOut])
def list_instruments(
    tags: Optional[str] = None,
    exclude_tags: Optional[str] = None,
    risk: Optional[str] = None,
    db: Annotated[Session, Depends(get_db)] = None,
):
    # Simple stub: ignore tags/risk filtering for now and return all instruments
    return db.exec(select(Instrument)).all()


@router.post("/", status_code=201, response_model=InstrumentOut)
def create_instrument(
    payload: InstrumentCreate,
    db: Annotated[Session, Depends(get_db)],
):
    existing = db.exec(
        select(Instrument).where(Instrument.ticker == payload.ticker)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Instrument already exists")
    inst = Instrument.from_orm(payload)
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst


@router.get("/{ticker}", response_model=InstrumentOut)
def get_instrument(
    ticker: str,
    db: Annotated[Session, Depends(get_db)],
):
    inst = db.exec(select(Instrument).where(Instrument.ticker == ticker)).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return inst
