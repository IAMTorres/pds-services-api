from fastapi import APIRouter, Depends, HTTPException, Path
from core.utils import get_db_session
from core.auth import get_current_active_user
from database.models.user import User

from sqlalchemy.orm import Session
import api.schemas as schemas
from api.service.owner_service import CompanyOwner

router = APIRouter()

@router.get("/company", response_model=schemas.CompanyResponse)
def get_company(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
    page_num: int = 1, page_size: int = 10
):
    return CompanyOwner.get_company_all(db)


@router.post("/company", response_model=schemas.CompanyResponse)
def add_company(
    obj_in: schemas.CompanyCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    company = CompanyOwner.create_company(db, obj_in, current_user)
    return company


@router.put("/company/{id}", response_model=schemas.CompanyResponse)
def update_company(
    obj_in: schemas.CompanyUpdate,
    company_id: int = Path(..., title="The id of the company"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    company = CompanyOwner.update_company(company_id, db, obj_in, current_user)

    if not company:
        raise HTTPException(status_code=400, detail="Company does not exists")

    return company


@router.delete("/company/{id}")
def delete_company(
    company_id: int = Path(..., title="The id of the company"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    address = CompanyOwner.delete_company(db, company_id, current_user)

    if not address:
        raise HTTPException(status_code=400, detail="Company does not exists")

