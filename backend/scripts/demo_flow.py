from fastapi.testclient import TestClient
from app.main import app
from app.db import create_db_and_tables


def main():
    create_db_and_tables()
    client = TestClient(app)

    print("\n1) Create a tag (public)")
    tag_name = "Clean Energy"
    r = client.post(
        "/api/v1/tags/",
        json={"name": tag_name, "category": "Theme", "description": "Renewables"},
    )
    if r.status_code == 201:
        tag = r.json()
        print(r.status_code, tag)
    else:
        print(r.status_code, r.json())
        # fetch existing tag by name
        r2 = client.get("/api/v1/tags/")
        tags = r2.json()
        tag = next((t for t in tags if t.get("name") == tag_name), None)
        print("Resolved tag:", tag)

    print("\n2) Create an instrument (public)")
    ticker = "AAPL"
    r = client.post(
        "/api/v1/instruments/",
        json={
            "ticker": ticker,
            "name": "Apple Inc.",
            "sector": "Technology",
            "market_cap": 2_500_000_000_000,
            "vol_30d": 0.25,
            "esg_score": 68,
        },
    )
    if r.status_code == 201:
        inst = r.json()
        print(r.status_code, inst)
    else:
        print(r.status_code, r.json())
        # fetch existing instrument by ticker
        r2 = client.get(f"/api/v1/instruments/{ticker}")
        inst = r2.json() if r2.status_code == 200 else None
        print("Resolved instrument:", inst)

    print("\n3) Register user (public)")
    r = client.post(
        "/api/v1/auth/register",
        json={
            "email": "demo@example.com",
            "password": "secret",
            "risk_level": "Medium",
        },
    )
    print(r.status_code, r.json())

    print("\n4) Login user (public) and obtain token")
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com", "password": "secret"},
    )
    print(r.status_code, r.json())
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    print("\n5) Call protected GET preferences (should be empty list)")
    r = client.get("/api/v1/users/me/preferences/", headers=headers)
    print(r.status_code, r.json())

    print("\n6) Add a preference (protected)")
    r = client.post(
        "/api/v1/users/me/preferences/",
        json={
            "tag_id": tag.get("id") if tag else None,
            "type": "inclusion",
            "strength": 80,
        },
        headers=headers,
    )
    print(r.status_code, r.json())

    print("\n7) Add to watchlist (protected)")
    r = client.post(
        "/api/v1/users/me/watchlist/",
        json={"ticker": "AAPL", "weight": 10},
        headers=headers,
    )
    print(r.status_code, r.json())

    print("\n8) Try admin-only action (create provider) — should fail for non-admin")
    r = client.post(
        "/api/v1/providers/",
        json={"name": "TestProv", "base_url": "https://example.com"},
        headers=headers,
    )
    print(r.status_code, r.json())


if __name__ == "__main__":
    main()
