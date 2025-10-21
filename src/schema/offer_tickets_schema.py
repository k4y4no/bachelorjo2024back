from pydantic import BaseModel


class OfferTicketBaseSchema(BaseModel):
    name: str
    price: float
    tickets_quantity: int

    class ConfigDict:
        from_attributes = True

class OfferTicketCreateSchema(OfferTicketBaseSchema):
    pass

class OfferTicketResponseSchema(OfferTicketBaseSchema):
    id: int
    # event_id: int

    class ConfigDict:
        from_attributes = True

class OfferTicketUpdateSchema(BaseModel):
    name: str | None = None
    price: float | None = None
    tickets_quantity: int | None = None

    class ConfigDict:
        from_attributes = True

