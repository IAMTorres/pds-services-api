from fastapi import APIRouter, Depends, HTTPException, Path, Security
from core.utils import get_db_session
from core.auth import get_current_active_user
from database.models.user import User
import api.service as service
from sqlalchemy.orm import Session
import api.schemas as schemas
from typing import Any, List

router = APIRouter()


@router.get("/", response_model=List[schemas.TrainingResponse])
def get_training(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    return service.training.get_training_all(db)


@router.post("/", response_model=schemas.TrainingResponse)
def add_training(
    obj_in: schemas.TraningCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    plan = service.training.create(db, obj_in, current_user)
    return plan


@router.put("/", response_model=schemas.TrainingResponse)
def update_training(
    obj_in: schemas.TraningUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    plan = service.training.update(db, obj_in, current_user)

    if not plan:
        raise HTTPException(status_code=400, detail="Training Plan does not exists")

    return plan


@router.delete("/{id}")
def delete_training(
    id: int = Path(..., title="The id of the training"),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    plan = service.training.delete(db, id, current_user)

    if not plan:
        raise HTTPException(status_code=400, detail="Training Plan does not exists")
