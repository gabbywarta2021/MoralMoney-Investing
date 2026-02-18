from fastapi import FastAPI

from .db import create_db_and_tables
from .auth import router as auth_router
from .providers import router as providers_router
from .tags import router as tags_router
from .instruments import router as instruments_router
from .preferences import router as preferences_router
from .watchlist import router as watchlist_router
from .allocate import router as allocate_router

app = FastAPI(title="MoralMoney API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth_router)
app.include_router(providers_router)
app.include_router(tags_router)
app.include_router(instruments_router)
app.include_router(preferences_router)
app.include_router(watchlist_router)
app.include_router(allocate_router)


@app.get("/health")
def health():
    return {"status": "ok"}
