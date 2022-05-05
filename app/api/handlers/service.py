from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from api.schemas.service_dto import ServiceCreate, ServiceResponse, UpdateService
from core.utils import get_db_session
from core.auth import get_current_active_user
from database.models.user import User
import api.service as service

router = APIRouter()

@router.get("/", response_model=List[ServiceResponse])
def list_services(db: Session = Depends(get_db_session)):
    return service.manager.get_service_all(db)

@router.post("/", response_model=ServiceResponse)
def create_service(service_in: ServiceCreate, db: Session = Depends(get_db_session),  
    current_user: User = Depends(get_current_active_user)):

    manager_in = service.user.verify_manager_id(db=db, id=service_in.manager_id)
    if manager_in:
        return service.manager.create_service(db=db, service=service_in, db_obj=current_user)
    else:
        raise HTTPException(
            status_code=400,
            detail="Manager does not exists",)

    
@router.put("/", response_model=ServiceResponse)
def update_service(service_in: UpdateService,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user)):

    manager = service.manager.update_service(db=db, service=service_in, db_obj=current_user)
    if not manager:
        raise HTTPException(
            status_code=400,
            detail="Service does not exists",)

@router.delete("/{id}")
def delete_service(
    id: int = Path(..., title="The id of the service"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    service_in = service.manager.delete_service(db, id, current_user)

    if not service_in:
        raise HTTPException(status_code=400, detail="Service does not exists")