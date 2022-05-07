from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    order_id: int | None
    pricing_policy_id: int | None
    service_id: int | None
    amount: float | None
    amount_discounted: float | None
    payment_date: str | None
    status: str | None = Field(None, min_length=2, max_length=45)


class OrderCreate(OrderBase):
    service_id: int
    pricing_policy_id: int
    amount: float
    amount_discounted: float


class OrderUpdate(OrderBase):
    order_id: int


class OrderResponse(OrderBase):
    order_id: int

    class Config:
        orm_mode = True
