from sqlalchemy.orm import Session
from fastapi import HTTPException, status


from src.model.offer_ticket import OfferTicket
from src.schema.offer_tickets_schema import OfferTicketCreateSchema, OfferTicketResponseSchema, OfferTicketUpdateSchema

def read_offer_tickets(db: Session):
   return db.query(OfferTicket).all()
   
def read_offer_ticket_by_id(offer_ticket_id: int, db: Session):
    offer_ticket = db.query(OfferTicket).filter(OfferTicket.id == offer_ticket_id).first()
    if not offer_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer ticket not found"
        )
    return offer_ticket

def create_offer_ticket(offer_ticket: OfferTicketCreateSchema, db: Session):
    new_offer_ticket = OfferTicket(
        name=offer_ticket.name,
        price=offer_ticket.price,
        tickets_quantity=offer_ticket.tickets_quantity,
    )
    db.add(new_offer_ticket)
    db.commit()
    db.refresh(new_offer_ticket)
    return new_offer_ticket

def delete_offer_ticket(offer_ticket_id: int, db: Session):
    offer_ticket = db.query(OfferTicket).filter(OfferTicket.id == offer_ticket_id).first()
    if not offer_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer ticket not found"
        )
    db.delete(offer_ticket)
    db.commit()
    return {"message": "Offer ticket deleted successfully"}

def update_offer_ticket(offer_ticket_id: int, offer_ticket_data: OfferTicketUpdateSchema, db: Session):
    offer_ticket = db.query(OfferTicket).filter(OfferTicket.id == offer_ticket_id).first()
    if not offer_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer ticket not found"
        )
    for key, value in offer_ticket_data.model_dump().items():
        setattr(offer_ticket_data, key, value)


    db.commit()
    db.refresh(offer_ticket)
    return offer_ticket