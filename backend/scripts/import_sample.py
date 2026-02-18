from sqlmodel import Session, select
from app.db import create_db_and_tables, engine
from app.models import Tag, Instrument
import json


def seed_tags(session: Session):
    sample = [
        {
            "name": "Clean Energy",
            "category": "Theme",
            "description": "Companies focused on renewable energy",
        },
        {
            "name": "Fossil-Free",
            "category": "Exclusion",
            "description": "Exclude fossil fuel producers",
        },
        {
            "name": "Technology",
            "category": "Sector",
            "description": "Technology sector",
        },
        {
            "name": "Tobacco-Free",
            "category": "Exclusion",
            "description": "Exclude tobacco-related companies",
        },
    ]
    for t in sample:
        exists = session.exec(select(Tag).where(Tag.name == t["name"])).first()
        if not exists:
            session.add(Tag(**t))


def seed_instruments(session: Session):
    sample = [
        {
            "ticker": "NEE",
            "name": "NextEra Energy",
            "sector": "Utilities",
            "market_cap": 150_000_000_000,
            "vol_30d": 0.18,
            "esg_score": 75.0,
        },
        {
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "sector": "Technology",
            "market_cap": 2_500_000_000_000,
            "vol_30d": 0.25,
            "esg_score": 68.0,
        },
        {
            "ticker": "TSLA",
            "name": "Tesla, Inc.",
            "sector": "Automotive",
            "market_cap": 700_000_000_000,
            "vol_30d": 0.45,
            "esg_score": 60.0,
        },
        {
            "ticker": "PM",
            "name": "Philip Morris",
            "sector": "Consumer",
            "market_cap": 150_000_000_000,
            "vol_30d": 0.2,
            "esg_score": 30.0,
        },
    ]
    for i in sample:
        exists = session.exec(
            select(Instrument).where(Instrument.ticker == i["ticker"])
        ).first()
        if not exists:
            session.add(Instrument(**i))


def compute_allocation(session: Session):
    instruments = session.exec(select(Instrument)).all()
    if not instruments:
        return {"items": []}
    n = len(instruments)
    cash_pct = 20
    pct = round((1 - cash_pct / 100) / n * 100, 2)
    items = [
        {"ticker": inst.ticker, "pct": pct, "reason": "sample-match"}
        for inst in instruments
    ]
    return {"user_id": 1, "risk_level": "Medium", "cash_pct": cash_pct, "items": items}


def main():
    create_db_and_tables()
    with Session(engine) as session:
        seed_tags(session)
        seed_instruments(session)
        session.commit()
        allocation = compute_allocation(session)
        print(json.dumps(allocation, indent=2))


if __name__ == "__main__":
    main()
