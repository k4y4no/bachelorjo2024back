from pydantic import BaseModel
from datetime import date

class SportOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class LocationOut(BaseModel):
    id: int
    name: str
    nb_places: int

    class Config:
        from_attributes = True

class EventOut(BaseModel):
    id: int
    date_event: date
    sport: SportOut
    location: LocationOut

    class Config:
        from_attributes = True

class EventResponse(BaseModel):
    id: int
    sport_id: int
    location_id: int
    # nb_places: int
    date_event: date

    class Config:
        from_attributes = True