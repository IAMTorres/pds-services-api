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

def number_valid(number: str) -> bool:
    number = str(number) if isinstance(number, int) else number
    len_number = len(number)

    if (
        number[0:1] not in ["2", "9"]
        and len_number != 9
    ):
        return False
    sumAux = 0
    for i in range(9, 1, -1):
        sumAux += i * (int(number[len_number - i]))

    module = sumAux % 11

    number_without_last_digit = number[0:8]
    if module == 0 or module == 1:
        return f"{number_without_last_digit}0" == number
    else:
        return f"{number_without_last_digit}{11-module}" == number

class ContactBase(BaseModel):
    contact_id: int | None
    contact_type: str | None = Field(None, min_length=2, max_length=200)
    number: str | None 

    @validator("contact_type")
    def check_category(cls, v):
        if v is None:
            return v
        if check_category(v) is None:
            raise ValueError("invalid contact_type")
        return v

    @validator("number")
    def check_number(cls, v):
        if v is None:
            return v
        if number_valid(v) is False:
            raise ValueError("invalid number")
        return v

class ContactCreate(ContactBase):
    contact_type: str
    number: str


class ContactUpdate(ContactBase):
    contact_id: int


class ContactResponse(ContactBase):
    class Config:
        orm_mode = True
