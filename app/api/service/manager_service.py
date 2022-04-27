from typing import Optional, Any
from sqlalchemy.orm import Session
from database.repository import SqlAlchemyRepository
from database.models.service import Service
from api.schemas import service_dto
from database.models.user import User

class ManagerService(SqlAlchemyRepository):

    def get_service_all(db: Session):
            return db.query(Service).all()

    @staticmethod
    def get_service_by_id(db: Session, id: int) -> Optional[Service]:
        return db.query(Service).filter(Service.service_id == id).first()

    def create_service(self, db: Session, service: service_dto.ServiceCreate, user_id: int):
        obj_in_data = service.dict(exclude_unset=True)
        obj_in_data["user_id"] = user_id
        return super().create(db=db, db_obj=Service, obj_in=obj_in_data)

    def update_service(self, db: Session, service: service_dto.UpdateService, user_obj: User
    ) -> Service:
        if (
            address := db.query(Service)
            .filter(Service.service_id==service.service_id)
            .first()
        ) is not None:
            for user_address in user_obj.address:
                if user_address.address_id == address.address_id:
                    obj_in_data = address.dict(exclude_unset=True)
                    obj_in_data = address["user_id"] = user_obj.user_id
                    return super().update(db, db_obj=address, obj_in=obj_in_data)
        return None
        

    def delete_service(self, db: Session, id: int):
        db_service = db.query(Service).get(id)
        db.delete(db_service)
        db.commit()


