from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    contact_id: int | None
    contact_type: str | None = Field(None, min_length=4, max_length=200)
    number: str | None = Field(None, min_length=9, max_length=12)


class ContactCreate(ContactBase):
    contact_type: str
    number: str = Field(..., min_length=9, max_length=12)


class ContactUpdate(ContactBase):
    contact_id: int


class ContactResponse(ContactBase):
    class Config:
        orm_mode = True