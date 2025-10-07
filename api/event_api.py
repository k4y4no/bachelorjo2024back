from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.schema.event_schema import EventResponse, EventOut, EventCreate
from src.controller.event_controller import read_events, create_events


class EventAPI:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.get("/", response_model=List[EventOut])
        def read_events_endpoint(db: Session = Depends(get_db)):
            return read_events(db)

        @self.router.post("/", response_model=EventResponse)
        def create_event_endpoint(eventJO: EventCreate, request: Request,db: Session = Depends(get_db)):
            return create_events(eventJO, db)