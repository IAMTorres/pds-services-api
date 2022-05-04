from pydantic import BaseModel, Field

class ServiceBase(BaseModel):
    service_name: str | None = Field(None, min_length=2, max_length=45)
    manager_id: int | None
    training_plan_id: int | None
    price: float | None
    rating: int | None
    status: str | None = Field(None, min_length=2, max_length=45)

class ServiceCreate(ServiceBase):
    service_name: str = Field(..., min_length=2, max_length=45)
    manager_id: int
    training_plan_id: int
    price: float

class UpdateService(ServiceBase):
    pass

class DeleteService(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    service_id: int

    class Config:
        orm_mode = True
        