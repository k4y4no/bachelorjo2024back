from datetime import date
from model.offer_ticket import OfferTicket
from src.config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int]  = mapped_column( primary_key=True)
    sport_id: Mapped[int] = mapped_column( ForeignKey('sports.id'), nullable=False)
    location_id: Mapped[int]  = mapped_column(ForeignKey('locations.id'), nullable=False)
    # nb_places = Column(Integer, ForeignKey('locations.nb_places'))
    date_event:Mapped[date] = mapped_column(Date, default=date.today)
    sport: Mapped["Sport"] = relationship(back_populates="events")
    location: Mapped["Location"] = relationship(back_populates="events")
    offer_tickets: Mapped[list["OfferTicket"]] = relationship(back_populates="eventJO", cascade="all, delete-orphan")



class Sport(Base):
    __tablename__ = 'sports'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    events: Mapped[list["Event"]] = relationship( back_populates='sport',
        cascade="all, delete-orphan",)

class Location(Base):
    __tablename__ = 'locations'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    nb_places: Mapped[int] = mapped_column(Integer)
    events: Mapped[list["Event"]]  = relationship( back_populates='location',
        cascade="all, delete-orphan",)
