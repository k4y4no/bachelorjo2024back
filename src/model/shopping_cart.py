from datetime import date
from src.config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column


class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'
    id: Mapped[int]  = mapped_column( primary_key=True)
    user_id: Mapped[int] = mapped_column( ForeignKey('users.id'), nullable=False)
    created_at:Mapped[date] = mapped_column(Date, default=date.today)
    # user: Mapped["User"] = relationship("User", back_populates="shopping_carts")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem",back_populates="shopping_cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = 'cart_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    shopping_cart_id: Mapped[int] = mapped_column(ForeignKey('shopping_carts.id'), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'), nullable=False)
    offer_id: Mapped[int] = mapped_column(ForeignKey('offer_tickets.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    shopping_cart: Mapped["ShoppingCart"] = relationship("ShoppingCart",back_populates="cart_items")
    # offer_ticket: Mapped["OfferTicket"] = relationship("OfferTicket",back_populates="cart_items")
    # eventJO: Mapped["Event"] = relationship("Event",back_populates="cart_items")