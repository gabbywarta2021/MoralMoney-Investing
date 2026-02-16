# MoralMoney Investing — MVP


[![CI Tests](https://github.com/gabbywarta2021/MoralMoney-Investing/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/gabbywarta2021/MoralMoney-Investing/actions/workflows/ci.yml)
[![Codecov](https://img.shields.io/codecov/c/github/gabbywarta2021/MoralMoney-Investing?logo=codecov)](https://codecov.io/gh/gabbywarta2021/MoralMoney-Investing)

A small FastAPI backend + OpenAPI contract and generated Python client for the MoralMoney investing MVP.

## Repo
https://github.com/gabbywarta2021/MoralMoney-Investing

## Quickstart

1. Create and activate a virtualenv (macOS/Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install runtime deps (example):

```bash
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install fastapi uvicorn sqlmodel httpx openapi-python-client
```

3. Run the API server locally:

```bash
.venv/bin/python -m uvicorn backend.app.main:app --reload --port 8000
```

4. Regenerate/write canonical OpenAPI and (optionally) re-generate client:

```bash
python3 scripts/write_openapi.py   # writes validated openapi.json
.venv/bin/python -m openapi_python_client generate --path openapi.json --output-path generated_client
.venv/bin/python -m pip install -e generated_client
```

5. Run the example authenticated client:

```bash
.venv/bin/python scripts/example_client.py
```

## Included files
- `openapi_full.json` — editable OpenAPI template
- `openapi.json` — canonical, validated OpenAPI contract
- `scripts/` — utilities: `generate_openapi_full.py`, `write_openapi.py`, `example_client.py`
- `generated_client/` — generated Python client package (editable installable)
- `backend/` — FastAPI application and routers

## Contributing
- Create feature branches and open PRs against `main` on GitHub.

## Next steps (suggestions)
- Add CI to validate `openapi.json` and run tests.
- Add example frontend or Postman collection demonstrating flows.
