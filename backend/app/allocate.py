from fastapi import APIRouter, Depends
from typing import Dict, Any, Annotated
from sqlmodel import Session, select

from .db import engine
from .models import Instrument

router = APIRouter(prefix="/api/v1", tags=["allocate"])


def get_db():
    with Session(engine) as session:
        yield session


@router.get("/allocate")
def allocate(
    db: Annotated[Session, Depends(get_db)],
    suggest: bool = True,
) -> Dict[str, Any]:
    # Very simple allocation: equal weight to all instruments.
    # Cash buffer is a fixed percentage for medium risk.
    instruments = db.exec(select(Instrument)).all()
    if not instruments:
        return {"user_id": 1, "risk_level": "Medium", "cash_pct": 20, "items": []}
    n = len(instruments)
    pct = round((1 - 0.2) / n * 100, 2)
    items = [
        {"ticker": inst.ticker, "pct": pct, "reason": "match"}
        for inst in instruments
    ]
    return {"user_id": 1, "risk_level": "Medium", "cash_pct": 20, "items": items}
