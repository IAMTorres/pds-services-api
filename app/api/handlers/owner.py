from typing import List
from anyio import current_effective_deadline
from fastapi import APIRouter, Depends, HTTPException, Path
from database.models.user import Owner, User
from core.utils import get_db_session
from core.auth import get_current_active_user
import api.service as service
from api.schemas.company_dto import CompanyCreate, CompanyUpdate, CompanyResponse
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/company", response_model=List[CompanyResponse])
def get_company(
    db: Session = Depends(get_db_session),
    current_user: Owner = Depends(get_current_active_user)
):
    return service.owner.get_company_all(db, current_user)


@router.post("/company", response_model=CompanyResponse)
def add_company(
    obj_in: CompanyCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    company = service.owner.create_company(db, obj_in, current_user)
    return company


@router.put("/company", response_model=CompanyResponse)
def update_company(
    obj_in: CompanyUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    company = service.owner.update_company(db, obj_in, current_user)

    if not company:
        raise HTTPException(status_code=400, detail="Company does not exists")

    return company


@router.delete("/company/{id}")
def delete_company(
    company_id: int = Path(..., title="The id of the company"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    address = service.owner.delete_company(db, company_id, current_user)

    if not address:
        raise HTTPException(status_code=400, detail="Company does not exists")

