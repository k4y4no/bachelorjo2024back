from sqlalchemy.orm import Session, selectinload

from src.model.event import Event

def read_events(db: Session):
    return (
        db.query(Event)
        .options(
            selectinload(Event.sport),
            selectinload(Event.location),
        )
        .all()
    )