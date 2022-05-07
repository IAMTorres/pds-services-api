from typing import Any, Optional
from sqlalchemy.orm import Session
from api.schemas import order_dto
from database.models.service import Service
from database.models.order import Order
from database.repository import SqlAlchemyRepository
from database.models.user import User


class OrderService(SqlAlchemyRepository):

    @staticmethod
    def verify_service_id(db: Session, id: Any) -> Optional[Service]:
        return db.query(Service).filter(Service.service_id == id).first()

    def get_order_all(self, db: Session):
        return db.query(Order).all()

    def create_order(
        self, db: Session, order: order_dto.OrderCreate, db_obj: User
    ) -> Order:
        obj_in_data = order.dict(exclude_unset=True)
        return super().create(db=db, db_obj=Order, obj_in=obj_in_data)

    def update_order(
        self, db: Session, order_in: order_dto.OrderUpdate, db_obj: User
    ) -> Order:
        if (
            orders := db.query(Order)
            .filter(Order.order_id == order_in.order_id)
            .first()
        ) is not None:
            obj_in_data = order_in.dict(exclude_unset=True)
            return super().update(db=db, db_obj=orders, obj_in=obj_in_data)
        return None

    def delete_order(self, db: Session, order_id: int, user_obj: User) -> Order:
        if (
            orders := db.query(Order)
            .filter(Order.order_id == order_id)
            .first()
        ) is not None:
            db.delete(orders)
            db.commit()
            return order_id
        return None


order = OrderService()
