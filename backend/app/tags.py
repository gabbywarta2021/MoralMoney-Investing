from fastapi import APIRouter, HTTPException, Depends
from typing import List, Annotated
from sqlmodel import Session, select

from .models import Tag
from .schemas import TagCreate, TagOut
from .db import engine

router = APIRouter(prefix="/api/v1/tags", tags=["tags"])


def get_db():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=List[TagOut])
def list_tags(db: Annotated[Session, Depends(get_db)]):
    return db.exec(select(Tag)).all()


@router.post("/", status_code=201, response_model=TagOut)
def create_tag(payload: TagCreate, db: Annotated[Session, Depends(get_db)]):
    existing = db.exec(select(Tag).where(Tag.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag exists")
    tag = Tag.from_orm(payload)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag
