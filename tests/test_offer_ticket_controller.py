import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status

from src.config.database import Base
from src.model.offer_ticket import OfferTicket
from src.schema.offer_tickets_schema import OfferTicketCreateSchema, OfferTicketUpdateSchema
from src.controller.offer_ticket_controller import (
    read_offer_tickets,
    create_offer_ticket,
    read_offer_ticket_by_id,
    update_offer_ticket,
    delete_offer_ticket,
)


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


def make_create_payload(name="Concert", price=20.0, tickets_quantity=100):
    return OfferTicketCreateSchema(name=name, price=price, tickets_quantity=tickets_quantity)


def test_read_offer_tickets_empty(db_session):
    items = read_offer_tickets(db_session)
    assert isinstance(items, list)
    assert items == []


def test_create_offer_ticket_persists(db_session):
    payload = make_create_payload()
    created = create_offer_ticket(payload, db_session)

    assert isinstance(created, OfferTicket)
    assert created.id is not None
    assert created.name == payload.name
    assert created.price == payload.price
    assert created.tickets_quantity == payload.tickets_quantity

    # confirm in DB
    db_item = db_session.query(OfferTicket).filter_by(id=created.id).first()
    assert db_item is not None
    assert db_item.name == payload.name


def test_read_offer_ticket_by_id_success(db_session):
    payload = make_create_payload("Show A", 15.5, 50)
    created = create_offer_ticket(payload, db_session)

    fetched = read_offer_ticket_by_id(created.id, db_session)
    assert isinstance(fetched, OfferTicket)
    assert fetched.id == created.id
    assert fetched.name == "Show A"


def test_read_offer_ticket_by_id_not_found_raises(db_session):
    with pytest.raises(HTTPException) as exc:
        read_offer_ticket_by_id(9999, db_session)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


def test_update_offer_ticket_modifies_fields(db_session):
    payload = make_create_payload("Initial", 10.0, 20)
    created = create_offer_ticket(payload, db_session)

    update_payload = OfferTicketUpdateSchema(name="Updated", price=12.5)
    updated = update_offer_ticket(created.id, update_payload, db_session)

    assert updated.id == created.id
    assert updated.name == "Updated"
    assert updated.price == 12.5
    # tickets_quantity should remain unchanged
    assert updated.tickets_quantity == 20

    # confirm in DB
    db_item = db_session.query(OfferTicket).filter_by(id=created.id).first()
    assert db_item.name == "Updated"
    assert db_item.price == 12.5


def test_delete_offer_ticket_removes_and_returns_204(db_session):
    payload = make_create_payload("ToDelete", 5.0, 10)
    created = create_offer_ticket(payload, db_session)

    resp = delete_offer_ticket(created.id, db_session)
    # Response object from FastAPI/Starlette has .status_code
    assert getattr(resp, "status_code", None) == status.HTTP_204_NO_CONTENT

    # ensure removed from DB
    db_item = db_session.query(OfferTicket).filter_by(id=created.id).first()
    assert db_item is None