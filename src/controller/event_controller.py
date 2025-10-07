from sqlalchemy.orm import Session, selectinload

from src.model.event import Event
from src.schema.event_schema import EventCreate

def read_events(db: Session):
    return (
        db.query(Event)
        .options(
            selectinload(Event.sport),
            selectinload(Event.location),
        )
        .all()
    )

def create_events(eventJO: EventCreate ,db: Session):
    new_eventJO = Event(**eventJO.model_dump())
    db.add(new_eventJO)
    db.commit()
    db.refresh(new_eventJO)
    return new_eventJO
