from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlmodel import Session, select

from .models import Provider, User
from .schemas import ProviderCreate
from .db import engine
from .auth import get_current_active_admin

router = APIRouter(prefix="/api/v1/providers", tags=["providers"])


def get_db():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=List[Provider])
def list_providers(db: Annotated[Session, Depends(get_db)]):
    return db.exec(select(Provider)).all()


@router.post("/", status_code=201, response_model=Provider)
def create_provider(
    payload: ProviderCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(get_current_active_admin)],
):
    prov = Provider.from_orm(payload)
    db.add(prov)
    db.commit()
    db.refresh(prov)
    return prov


@router.get("/{provider_id}", response_model=Provider)
def get_provider(
    provider_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    prov = db.get(Provider, provider_id)
    if not prov:
        raise HTTPException(status_code=404, detail="Provider not found")
    return prov


@router.put("/{provider_id}", response_model=Provider)
def update_provider(
    provider_id: int,
    payload: ProviderCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(get_current_active_admin)],
):
    prov = db.get(Provider, provider_id)
    if not prov:
        raise HTTPException(status_code=404, detail="Provider not found")
    prov_data = payload.dict(exclude_unset=True)
    for k, v in prov_data.items():
        setattr(prov, k, v)
    db.add(prov)
    db.commit()
    db.refresh(prov)
    return prov


@router.delete("/{provider_id}", status_code=204)
def delete_provider(
    provider_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(get_current_active_admin)],
):
    prov = db.get(Provider, provider_id)
    if not prov:
        raise HTTPException(status_code=404, detail="Provider not found")
    db.delete(prov)
    db.commit()
    return None
