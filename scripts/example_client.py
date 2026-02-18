from moral_money_investing_api_client import Client


def main():
    base_url = "http://localhost:8000"

    client = Client(base_url=base_url)
    httpx_client = client.get_httpx_client()

    # 1) Try health endpoint
    try:
        h = httpx_client.get("/health")
        print("health", h.status_code, h.json())
    except Exception as e:
        print("health request failed:", e)

    # 2) Auth flow: register (if not exists) then login to obtain token
    try:
        register_payload = {"email": "test@example.com", "password": "testpass"}
        r = httpx_client.post("/api/v1/auth/register", json=register_payload)
        print("register ->", r.status_code)
    except Exception as e:
        print("register failed:", e)

    token = None
    try:
        login_payload = {"email": "test@example.com", "password": "testpass"}
        login_resp = httpx_client.post("/api/v1/auth/login", json=login_payload)
        print("login ->", login_resp.status_code)
        if login_resp.status_code == 200:
            body = login_resp.json()
            token = body.get("access_token") or body.get("token")
            print("got token?", bool(token))
        else:
            print("login response:", login_resp.text[:400])
    except Exception as e:
        print("login failed:", e)

    # 3) Use token to call a protected endpoint
    if token:
        auth_headers = {"Authorization": f"Bearer {token}"}
        authed = Client(base_url=base_url, headers=auth_headers)
        httpx_auth = authed.get_httpx_client()
        try:
            p = httpx_auth.get("/api/v1/users/me/preferences", follow_redirects=True)
            print("protected call status:", p.status_code)
            print("protected call headers:", dict(p.headers))
            print(p.text[:4000])
        except Exception as e:
            print("protected call failed:", e)


if __name__ == "__main__":
    main()
