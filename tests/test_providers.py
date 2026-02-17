import pytest

from httpx import ASGITransport, AsyncClient

from generated_client.moral_money_investing_api_client import Client as GenClient
from generated_client.moral_money_investing_api_client import AuthenticatedClient

from backend.app.main import app
from backend.app.auth import create_access_token
from backend.app import db
from sqlmodel import Session, select


@pytest.mark.asyncio
async def test_list_providers(seed_data):
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        follow_redirects=True,
    ) as httpx_client:
        client = GenClient(base_url="http://testserver")
        client.set_async_httpx_client(httpx_client)
        r = await client.get_async_httpx_client().get("/api/v1/providers/")
        assert r.status_code == 200
        items = r.json()
        assert isinstance(items, list)
        assert len(items) >= 1


@pytest.mark.asyncio
async def test_admin_create_update_delete_provider(seed_data):
    # create admin token from seeded admin user
    from backend.app.models import User

    with Session(db.engine) as s:
        admin = s.exec(select(User).where(User.email == "admin@example.com")).first()
    assert admin is not None
    token = create_access_token({"sub": str(admin.id), "email": admin.email})

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        headers={"Authorization": f"Bearer {token}"},
        follow_redirects=True,
    ) as httpx_client:
        client = AuthenticatedClient(base_url="http://testserver", token=token)
        client.set_async_httpx_client(httpx_client)

        # Create provider
        payload = {
            "name": "New Prov",
            "base_url": "https://new.example",
            "api_key_required": False,
        }
        r = await client.get_async_httpx_client().post(
            "/api/v1/providers/",
            json=payload,
        )
        assert r.status_code == 201
        created = r.json()
        pid = created.get("id")
        assert pid

        # Get provider
        g = await client.get_async_httpx_client().get(f"/api/v1/providers/{pid}")
        assert g.status_code == 200

        # Update provider
        u = await client.get_async_httpx_client().put(
            f"/api/v1/providers/{pid}",
            json={
                "name": "Updated Prov",
                "base_url": "https://u.example",
                "api_key_required": False,
            },
        )
        assert u.status_code == 200
        assert u.json().get("name") == "Updated Prov"

        # Delete provider
        d = await client.get_async_httpx_client().delete(f"/api/v1/providers/{pid}")
        assert d.status_code == 204
