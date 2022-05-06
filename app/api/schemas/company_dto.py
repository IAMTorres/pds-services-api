from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    company_id: int | None
    owner_id: int | None
    name: str | None = Field(None, min_length=2, max_length=45)


class CompanyCreate(BaseModel):
    owner_id: int
    name: str = Field(..., min_length=2, max_length=45)


class CompanyUpdate(CompanyBase):
    company_id: int


class CompanyResponse(CompanyBase):
    class Config:
        orm_mode = True
