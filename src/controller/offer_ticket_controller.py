from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status


from src.service.query_service import get_by_id_or_404, get_all
from src.model.offer_ticket import OfferTicket
from src.schema.offer_tickets_schema import OfferTicketCreateSchema, OfferTicketResponseSchema, OfferTicketUpdateSchema

def read_offer_tickets(db: Session) -> list[OfferTicket]:
   return get_all(db, OfferTicket)

def read_offer_ticket_by_id(offer_ticket_id: int, db: Session) -> OfferTicket:
    return get_by_id_or_404(db, OfferTicket, offer_ticket_id)

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
    offer_ticket = get_by_id_or_404(db, OfferTicket, offer_ticket_id)
    db.delete(offer_ticket)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def update_offer_ticket(offer_ticket_id: int, offer_ticket_data: OfferTicketUpdateSchema, db: Session):
    offer_ticket = get_by_id_or_404(db, OfferTicket, offer_ticket_id)
    update_data = offer_ticket_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(offer_ticket, key):
            setattr(offer_ticket, key, value)


    db.commit()
    db.refresh(offer_ticket)
    return offer_ticket