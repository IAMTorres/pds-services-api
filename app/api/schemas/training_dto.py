from typing import Optional, Dict
from unicodedata import name
from pydantic import BaseModel, EmailStr, Field, validator, Json
from datetime import date
from sqlalchemy.orm import Session
from core.utils import get_session
from database.models.training import TrainingCategory


def load_training_categories(db: Session) -> Dict:
    categories_dict = dict()
    training_categories = db.query(TrainingCategory).all()
    for training in training_categories:
        categories_dict[training.training_category_id] = training.name
        categories_dict[training.name] = training.training_category_id
    return categories_dict


CATEGORIES = load_training_categories(get_session())


def check_category(category) -> int:
    if category_id := CATEGORIES.get(category, None) is not None and isinstance(
        category, str
    ):
        return category_id
    if description := CATEGORIES.get(category, None) is not None and isinstance(
        category, int
    ):
        return CATEGORIES[description]
    return None


class TrainingBase(BaseModel):
    training_plan_category: int | None
    price: float | None
    description: str | None = Field(None, min_length=4, max_length=45)
    expiration_date: date | None
    details: Json | None
    number_of_sessions: int | None
    notes: str | None

    @validator("training_plan_category")
    def check_category(cls, v):
        if v is None:
            return v
        if check_category(v) is None:
            raise ValueError("invalid training_plan_category")
        return v


class TraningCreate(TrainingBase):
    training_plan_category: int
    price: float
    description: str = Field(None, min_length=4, max_length=200)


class TraningUpdate(TrainingBase):
    training_plan_id: int


class TrainingResponse(TrainingBase):
    training_plan_id: int | None

    class Config:
        orm_mode = True
