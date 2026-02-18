from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    risk_level: Optional[str] = Field(default="Medium")
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: Optional[str] = None
    base_url: str
    api_key_required: bool = Field(default=True)
    priority: Optional[int] = Field(default=100)
    enabled: bool = Field(default=True)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    category: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Instrument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True, unique=True)
    name: Optional[str] = None
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    vol_30d: Optional[float] = None
    esg_score: Optional[float] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Preference(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    tag_id: int
    type: str = Field(default="inclusion")
    strength: int = Field(default=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WatchlistEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    instrument_id: int
    weight: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
