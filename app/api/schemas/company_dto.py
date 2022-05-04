from typing import Optional
from unicodedata import name
from pydantic import BaseModel, EmailStr, Field, validator


class CompanyBase(BaseModel):
    company_id: int | None
    owner_id: int | None
    name: str | None = Field(None, min_length=4, max_length=45)


class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=4, max_length=45)


class CompanyUpdate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    class Config:
        orm_mode = True
