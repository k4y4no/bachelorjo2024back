from typing import Type, TypeVar, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.config.database import Base

T = TypeVar("T", bound=Base)
db: Session

def get_all(db: Session, model: Type[T]) -> list[T]:
    return db.query(model).all()

def get_item_by_id(db: Session, model: Type[T], id: int) -> Optional[T]:
    return db.query(model).filter(model.id == id).first()

def get_by_id_or_404(db: Session, model: Type[T], id: int) -> T:
    instance = get_item_by_id(db, model, id)
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")
    return instance