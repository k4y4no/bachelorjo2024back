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

def create_events(event_jo: EventCreate ,db: Session):
    new_event_jo = Event(**event_jo.model_dump())
    db.add(new_event_jo)
    db.commit()
    db.refresh(new_event_jo)
    return new_event_jo
