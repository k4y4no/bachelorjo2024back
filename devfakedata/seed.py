# scripts/seed.py
from datetime import date
from sqlalchemy.orm import Session
from src.model.event import Sport, Location, Event

def seed(db: Session):
    # évite de doubler le seed
    if db.query(Sport).first():
        return

    natation = Sport(name='Natation')
    course = Sport(name='Course')
    saut = Sport(name='Saut')

    piscine = Location(name='Piscine', nb_places=75)
    terrain = Location(name='Terrain', nb_places=60)
    terrain2 = Location(name='Terrain 2', nb_places=100)

    db.add_all([natation, course, saut, piscine, terrain, terrain2])
    db.flush()  # pour avoir les IDs si tu veux passer par *_id

    # Version RELATIONNELLE (recommandée)
    event1 = Event(sport=natation, location=piscine,  date_event=date.today())
    event2 = Event(sport=course,   location=terrain,  date_event=date.today())
    event3 = Event(sport=course,   location=terrain2, date_event=date.today())
    event4 = Event(sport=saut,     location=terrain,  date_event=date.today())

    db.add_all([event1, event2, event3, event4])
    db.commit()
