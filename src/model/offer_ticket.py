from src.config.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, ForeignKey, Float

from src.model.event import Event



class OfferTicket(Base):
    __tablename__ = 'offer_tickets'
    id: Mapped[int]  = mapped_column( primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    tickets_quantity: Mapped[int] = mapped_column(Integer)
    # eventJO: Mapped["Event"] = relationship( back_populates='offer_tickets')