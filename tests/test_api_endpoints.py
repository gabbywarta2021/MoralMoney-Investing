import pytest

from httpx import ASGITransport, AsyncClient

from generated_client.moral_money_investing_api_client import Client as GenClient
from generated_client.moral_money_investing_api_client import AuthenticatedClient

from backend.app.main import app


@pytest.fixture
def asgi_transport():
    return ASGITransport(app=app)


@pytest.mark.asyncio
async def test_health(asgi_transport):
    async with AsyncClient(
        transport=asgi_transport,
        base_url="http://testserver",
        follow_redirects=True,
    ) as httpx_client:
        client = GenClient(base_url="http://testserver")
        client.set_async_httpx_client(httpx_client)
        r = await client.get_async_httpx_client().get("/health")
        assert r.status_code == 200
        assert r.json().get("status") == "ok"


@pytest.mark.asyncio
async def test_auth_register_login_and_protected(asgi_transport):
    async with AsyncClient(
        transport=asgi_transport,
        base_url="http://testserver",
        follow_redirects=True,
    ) as httpx_client:
        client = GenClient(base_url="http://testserver")
        client.set_async_httpx_client(httpx_client)

        reg_payload = {"email": "test@example.com", "password": "testpass"}
        r = await client.get_async_httpx_client().post(
            "/api/v1/auth/register",
            json=reg_payload,
        )
        assert r.status_code in (201, 400)

        login_resp = await client.get_async_httpx_client().post(
            "/api/v1/auth/login",
            json=reg_payload,
        )
        assert login_resp.status_code == 200
        body = login_resp.json()
        token = body.get("access_token") or body.get("token")
        assert token

        # Use AuthenticatedClient to call protected endpoint
        auth = AuthenticatedClient(base_url="http://testserver", token=token)
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
            headers={"Authorization": f"Bearer {token}"},
            follow_redirects=True,
        ) as auth_httpx:
            auth.set_async_httpx_client(auth_httpx)
            p = await auth.get_async_httpx_client().get("/api/v1/users/me/preferences")
            assert p.status_code in (200, 204, 307)
