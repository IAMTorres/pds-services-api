from typing import List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from api.schemas.service_dto import ServiceCreate, ServiceResponse, UpdateService
from core.utils import get_db_session
from core.auth import get_current_active_user
from database.models.user import User
from api.service.manager_service import ManagerService

router = APIRouter()

@router.get("/", response_model=List[ServiceResponse])
def list_services(db: Session = Depends(get_db_session)):
    return ManagerService.get_service_all(db=db)

@router.post("/", response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db_session),  
    current_user: User = Depends(get_current_active_user)):
    return ManagerService.create_service(db, service, current_user)

@router.put("/{id}", response_model=ServiceResponse)
def update_service(service: UpdateService,
    id: int = Path(..., title="The id of the service"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user)):
    return ManagerService.update_service(db=db, service=service,id=id, user_id=current_user.user_id)

@router.delete("/{id}")
def delete_service(db: Session = Depends(get_db_session), id: int = int):
    return ~ManagerService.delete_service(db=db, id=id)