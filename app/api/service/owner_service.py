from sqlalchemy.orm import Session
from database.models.user import User
from database.repository import SqlAlchemyRepository
from api.schemas import company_dto
from database.models.user import Owner
from database.models.company import Company

class CompanyOwner(SqlAlchemyRepository):

    def get_company_all(self, db: Session, user_obj: User):
        return db.query(Company).all()

    def create_company(
        self, db: Session, company_in: company_dto.CompanyCreate, db_obj: User
    ) -> Company:
        obj_in_data = company_in.dict(exclude_unset=True)
        return super().create(db=db, db_obj=Company, obj_in=obj_in_data)

    def update_company(
        self, db: Session, company_in: company_dto.CompanyUpdate, db_obj: User
    ) -> Company:
        if (
            company_in := db.query(Company)
            .filter(Company.company_id == company_in.company_id)
            .first()
        ) is not None:
                obj_in_data = company_in.dict(exclude_unset=True)
                return super().update(db=db, db_obj=company_in, obj_in=obj_in_data)
        return None
        

    def delete_company(self, db: Session, company_id: int, user_obj: User) -> Company:
        if (
            company := db.query(Company)
            .filter(Company.company_id == company_id)
            .first()
        ) is not None:
                db.delete(company)
                db.commit()
                return company_id
        return None


owner = CompanyOwner()