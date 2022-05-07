from database.repository import SqlAlchemyRepository
from database.models.user import User, Manager
from database.models.training import TrainingPlan
from sqlalchemy.orm import Session
import api.schemas as schemas
from typing import Optional, Any


class TrainingService(SqlAlchemyRepository):
    
    @staticmethod
    def get_training_all(db: Session):
        return db.query(TrainingPlan).filter(TrainingPlan.status != False).all()


    @staticmethod
    def get_manager_by_user_id(db: Session, id: Any) -> Optional[Manager]:
        return db.query(Manager).filter(Manager.user_id == id).first()
    
    @staticmethod
    def get_manager_by_user_id(db: Session, id: Any) -> Optional[Manager]:
        return db.query(Manager).filter(Manager.user_id == id).first()

    @staticmethod
    def get_training_by_manager_id(db: Session, id: Any) -> Optional[Manager]:
        return db.query(Manager).filter(Manager.user_id == id).first()

    @staticmethod
    def get_training_by_id(db: Session, id: Any) -> Optional[TrainingPlan]:
        return (
            db.query(TrainingPlan).filter(TrainingPlan.training_plan_id == id).first()
        )

    def create(
        self, db: Session, training_in: schemas.TraningCreate, user_obj: User
    ) -> Optional[TrainingPlan]:
        if (manager := self.get_manager_by_user_id(db, user_obj.user_id)) is not None:
            obj_in_data = training_in.dict(exclude_unset=True)
            obj_in_data["manager_id"] = manager.manager_id
            return super().create(db=db, db_obj=TrainingPlan, obj_in=obj_in_data)
        return None

    def update(
        self, db: Session, training_in: schemas.TraningUpdate, user_obj: User
    ) -> TrainingPlan:
        if (manager := self.get_manager_by_user_id(db, user_obj.user_id)) is not None:
            if (
                trianing_plan := db.query(TrainingPlan)
                .filter(TrainingPlan.training_plan_id == training_in.training_plan_id)
                .first()
            ) is not None:
                if trianing_plan.manager_id == manager.manager_id:
                    return super().update(db, db_obj=trianing_plan, obj_in=training_in)
        return None
    
    def delete(self, db: Session, training_id: int, user_obj: User):
        if (manager := self.get_manager_by_user_id(db, user_obj.user_id)) is not None:
            if (
                trianing_plan := db.query(TrainingPlan)
                .filter(TrainingPlan.training_plan_id == training_id)
                .first()
            ) is not None:
                if trianing_plan.manager_id == manager.manager_id:
                    trianing_plan.status = False
                    db.commit()
                    return training_id
        return None

    def accept_service(
        self, db: Session, service_id: int, user_obj: User
    ) -> Optional[int]:
        if manager := self.get_manager_by_user_id(db, user_obj.user_id) is not None:
            pass

training = TrainingService()