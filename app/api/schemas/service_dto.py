from pydantic import BaseModel, Field


class ServiceBase(BaseModel):
    service_id: int | None
    manager_id: int | None
    training_plan_id: int | None
    service_category_id: int | None
    rating: int | None
    status: str | None = Field(None, min_length=2, max_length=45)


class ServiceCreate(ServiceBase):
    manager_id: int
    training_plan_id: int
    service_category_id: int


class UpdateService(ServiceBase):
    service_id: int


class DeleteService(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    service_id: int

    class Config:
        orm_mode = True
