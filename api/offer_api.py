from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.config.database import get_db  
from src.schema.offer_tickets_schema import OfferTicketResponseSchema, OfferTicketCreateSchema, OfferTicketUpdateSchema
from src.controller.offer_ticket_controller import (
    read_offer_tickets,
    read_offer_ticket_by_id,
    create_offer_ticket,
    delete_offer_ticket,
    update_offer_ticket
)

class OfferTicketAPI:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.get("/", response_model=list[OfferTicketResponseSchema])
        def read_offer_tickets_endpoint(db: Session = Depends(get_db)):
            return read_offer_tickets(db)

        @self.router.get("/{offer_ticket_id}", response_model=OfferTicketResponseSchema)
        def read_offer_ticket_by_id_endpoint(offer_ticket_id: int, db: Session = Depends(get_db)):
            return read_offer_ticket_by_id(offer_ticket_id, db)

        @self.router.post("/", response_model=OfferTicketResponseSchema)
        def create_offer_ticket_endpoint(offer_ticket: OfferTicketCreateSchema, db: Session = Depends(get_db)):
            return create_offer_ticket(offer_ticket, db)

        @self.router.delete("/{offer_ticket_id}", response_model=OfferTicketResponseSchema)
        def delete_offer_ticket_endpoint(offer_ticket_id: int, db: Session = Depends(get_db)):
            return delete_offer_ticket(offer_ticket_id, db)
        
        @self.router.put("/{offer_ticket_id}", response_model=OfferTicketResponseSchema)
        def update_offer_ticket_endpoint(offer_ticket_id: int, offer_ticket_data: OfferTicketUpdateSchema, db: Session = Depends(get_db)):
            return update_offer_ticket(offer_ticket_id, offer_ticket_data, db)
