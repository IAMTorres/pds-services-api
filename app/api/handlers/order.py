from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from api.schemas.order_dto import OrderCreate, OrderUpdate, OrderResponse
from core.utils import get_db_session
from core.auth import get_current_active_user
from database.models.user import User
import api.service as service

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db_session)):
    return service.order.get_order_all(db)


@router.post("/", response_model=OrderResponse)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):

    exist_service = service.order.verify_service_id(db=db, id=order_in.service_id)
    if exist_service:
        return service.order.create_order(db, order_in, current_user)
    else:
        raise HTTPException(
            status_code=400,
            detail="Service does not exists",
        )


@router.put("/", response_model=OrderResponse)
def update_order(
    order_in: OrderUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):

    order = service.order.update_order(db, order_in, current_user)
    if not order:
        raise HTTPException(
            status_code=400,
            detail="Order does not exists",
        )


@router.delete("/{id}")
def delete_order(
    id: int = Path(..., title="The id of the order"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    order_in = service.order.delete_order(db, id, current_user)

    if not order_in:
        raise HTTPException(status_code=400, detail="Order does not exists")
