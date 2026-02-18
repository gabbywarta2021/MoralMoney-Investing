#!/usr/bin/env python3
import argparse
from sqlmodel import Session, select
from app.db import create_db_and_tables, engine
from app.models import Provider, Instrument


def list_providers(session: Session):
    provs = session.exec(select(Provider)).all()
    for p in provs:
        print(f"{p.id}: {p.name} (enabled={p.enabled}, base_url={p.base_url})")
    if not provs:
        print("No providers configured.")


def create_provider(session: Session, name: str, base_url: str):
    p = Provider(name=name, base_url=base_url)
    session.add(p)
    session.commit()
    session.refresh(p)
    print("Created provider:", p.id, p.name)


def fake_fetch_instruments_for_provider(provider: Provider):
    # Simulated fetch: return a list of instrument dicts based on provider name
    if "polygon" in provider.name.lower():
        return [
            {
                "ticker": "POLY1",
                "name": "Polygon Sample 1",
                "sector": "Tech",
                "market_cap": 10_000_000_000,
                "vol_30d": 0.22,
                "esg_score": 70.0,
            },
            {
                "ticker": "POLY2",
                "name": "Polygon Sample 2",
                "sector": "Energy",
                "market_cap": 5_000_000_000,
                "vol_30d": 0.28,
                "esg_score": 55.0,
            },
        ]
    # fallback sample
    return [
        {
            "ticker": "SAMP1",
            "name": f"{provider.name} Sample 1",
            "sector": "Misc",
            "market_cap": 1_000_000_000,
            "vol_30d": 0.2,
            "esg_score": 50.0,
        }
    ]


def sync_provider(session: Session, provider_id: int, full: bool = False):
    prov = session.get(Provider, provider_id)
    if not prov:
        print("Provider not found")
        return
    print(f"Starting sync for provider {prov.id}: {prov.name} (full={full})")
    items = fake_fetch_instruments_for_provider(prov)
    added = 0
    for it in items:
        exists = session.exec(
            select(Instrument).where(Instrument.ticker == it["ticker"])
        ).first()
        if exists and not full:
            print(f"Skipping existing {it['ticker']}")
            continue
        if exists and full:
            # update
            exists.name = it.get("name")
            exists.sector = it.get("sector")
            exists.market_cap = it.get("market_cap")
            exists.vol_30d = it.get("vol_30d")
            exists.esg_score = it.get("esg_score")
            session.add(exists)
            added += 1
            continue
        inst = Instrument(**it)
        session.add(inst)
        added += 1
    session.commit()
    print(f"Sync complete. Instruments added/updated: {added}")


def main():
    parser = argparse.ArgumentParser(description="Admin CLI for MoralMoney backend")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list-providers")

    create_p = sub.add_parser("create-provider")
    create_p.add_argument("--name", required=True)
    create_p.add_argument("--base-url", required=True)

    sync_p = sub.add_parser("sync-provider")
    sync_p.add_argument("--provider-id", type=int, required=True)
    sync_p.add_argument("--full", action="store_true")

    args = parser.parse_args()

    create_db_and_tables()
    with Session(engine) as session:
        if args.cmd == "list-providers":
            list_providers(session)
        elif args.cmd == "create-provider":
            create_provider(session, args.name, args.base_url)
        elif args.cmd == "sync-provider":
            sync_provider(session, args.provider_id, full=args.full)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
