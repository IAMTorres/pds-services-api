from typing import Any, Optional
from sqlalchemy.orm import Session
from database.models.user import User
from database.repository import SqlAlchemyRepository
from api.schemas import company_dto
from database.models.user import Owner
from database.models.company import Company


class CompanyOwner(SqlAlchemyRepository):
    def get_company_all(db: Session):
        return db.query(Company).all()

    @staticmethod
    def get_owner_by_user_id(db: Session, id: Any) -> Optional[Owner]:
        return db.query(Owner).filter(Owner.user_id == id).first()

    def create_company(
        self, db: Session, company: company_dto.CompanyCreate, user_obj: User
    ) -> Company:
        if (owner := self.get_owner_by_user_id(db, user_obj.user_id)) is not None:
            obj_in_data = company.dict(exclude_unset=True)
            obj_in_data["owner_id"] = owner.owner_id
        return super().create(db=db, db_obj=Company, obj_in=obj_in_data)

    def update_company(
        self, id: int, db: Session, company: company_dto.CompanyUpdate, user_obj: User
    ) -> Company:
        if (
            company := db.query(Company).filter(Company.company_id == id).first()
        ) is not None:
            if (owner := self.get_owner_by_user_id(db, user_obj.user_id)) is not None:
                if owner.owner_id == company.owner_id:
                    obj_in_data = company.dict(exclude_unset=True)
                    return super().update(db, db_obj=company, obj_in=obj_in_data)
        return None

    def delete_company(self, db: Session, company_id: int, user_obj: User) -> None:
        if (
            company := db.query(Company)
            .filter(Company.company_id == company_id)
            .first()
        ) is not None:
            if (owner := self.get_owner_by_user_id(db, user_obj.user_id)) is not None:
                if owner.owner_id == company.owner_id:
                    db.delete(company)
                    db.commit()
                    return company_id
        return None


owner = CompanyOwner()
