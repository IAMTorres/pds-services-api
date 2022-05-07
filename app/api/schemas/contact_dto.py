from typing import Dict
from pydantic import BaseModel, Field, validator
from datetime import date
from sqlalchemy.orm import Session
from core.utils import get_session
from database.models.contact import Contact


def load_contact_categories(db: Session) -> Dict:
    categories_dict = dict()
    contact_categories = db.query(Contact).all()
    for contact in contact_categories:
        categories_dict[contact.contact_type] = contact.number
        categories_dict[contact.number] = contact.contact_type
    return categories_dict


CATEGORIES = load_contact_categories(get_session())


def check_category(category) -> int:
    if category_id := CATEGORIES.get(category, None) is not None and isinstance(
        category, str
    ):
        return category_id
    if description := CATEGORIES.get(category, None) is not None and isinstance(
        category, int
    ):
        return CATEGORIES[description]
    return None


class ContactBase(BaseModel):
    contact_id: int | None
    contact_type: str | None = Field(None, min_length=2, max_length=200)
    number: str | None 


class ContactCreate(ContactBase):
    contact_type: str
    number: str


class ContactUpdate(ContactBase):
    contact_id: int


class ContactResponse(ContactBase):
    class Config:
        orm_mode = True
