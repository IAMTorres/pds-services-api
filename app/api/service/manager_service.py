from typing import Optional
from sqlalchemy.orm import Session
from database.repository import SqlAlchemyRepository
from database.models.service import Service
from api.schemas import service_dto
from database.models.user import User
import api.service as service

class ManagerService(SqlAlchemyRepository):

    def get_service_all(self, db: Session):
        return db.query(Service).all()


    def get_service_by_id(self, db: Session, id: int) -> Optional[Service]:
        return db.query(Service).filter(Service.service_id == id).first()


    def create_service(self, db: Session, service: service_dto.ServiceCreate, db_obj: User) -> Service:
        obj_in_data = service.dict(exclude_unset=True)
        obj_in_data["user_id"] = db_obj.user_id
        return super().create(db=db, db_obj=Service, obj_in=obj_in_data)


    def update_service(
        self, db: Session, service_in: service_dto.UpdateService, db_obj: User
    ) -> Service:
        if (
            services := db.query(Service)
            .filter(Service.service_id == service_in.service_id)
            .first()
        ) is not None:
            is_manager = service.user.get_manager_by_user_id(db, db_obj.user_id)
            if(is_manager == service_in.manager_id):
                obj_in_data = service_in.dict(exclude_unset=True)
                obj_in_data["user_id"] = db_obj.user_id
                return super().update(db=db, db_obj=services, obj_in=obj_in_data)
        return None
        

    def delete_service(self, db: Session, service_id: int, user_obj: User) -> Service:
        if (
            service := db.query(Service)
            .filter(Service.service_id == service_id)
            .first()
        ) is not None:
                db.delete(service)
                db.commit()
                return service_id
        return None


manager = ManagerService()
