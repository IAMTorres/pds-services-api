from typing import List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from api.schemas.service_dto import ServiceCreate, ServiceResponse, UpdateService
from api.schemas import service_dto
from core.utils import get_db_session
from core.auth import get_current_active_user
from database.models.user import User
from api.service import manager_service


router = APIRouter()

@router.get("/", response_model=List[ServiceResponse])
def list_services(db: Session = Depends(get_db_session)):
    return manager_service.get_service_all(db=db)


@router.post("/", response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db_session),  
    current_user: User = Depends(get_current_active_user)):
    return manager_service.create_service(db=db, service=service, user_id=current_user.user_id)

@router.put("/{id}", response_model=ServiceResponse)
def update_service(service: service_dto.UpdateService,
    id: int = Path(..., title="The id of the service"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user)):
    return manager_service.update_service(db=db, service=service,id=id, user_id=current_user.user_id)

@router.delete("/{id}")
def delete_service(db: Session = Depends(get_db_session), id: int = int):
    return manager_service.delete_service(db=db, id=id)