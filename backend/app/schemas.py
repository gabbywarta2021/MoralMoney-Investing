from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    risk_level: Optional[str] = "Medium"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProviderCreate(BaseModel):
    name: str
    type: Optional[str] = None
    base_url: str
    api_key_required: Optional[bool] = True
    priority: Optional[int] = 100
    enabled: Optional[bool] = True
    notes: Optional[str] = None


class TagOut(BaseModel):
    id: int
    name: str
    category: Optional[str]
    description: Optional[str]


class TagCreate(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None


class InstrumentOut(BaseModel):
    id: int
    ticker: str
    name: Optional[str]
    sector: Optional[str]
    market_cap: Optional[float]
    vol_30d: Optional[float]
    esg_score: Optional[float]


class InstrumentCreate(BaseModel):
    ticker: str
    name: Optional[str] = None
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    vol_30d: Optional[float] = None
    esg_score: Optional[float] = None


class PreferenceOut(BaseModel):
    id: int
    user_id: int
    tag_id: int
    type: str
    strength: int


class PreferenceCreate(BaseModel):
    tag_id: int
    type: str
    strength: Optional[int] = 50


class WatchlistOut(BaseModel):
    id: int
    user_id: int
    instrument_id: int
    weight: Optional[float]


class WatchlistCreate(BaseModel):
    ticker: str
    weight: Optional[float] = None
