from sqlalchemy.orm import Session
from database.repository import SqlAlchemyRepository
from api.schemas import company_dto
from database.models.user import Owner
from database.models.company import Company

class CompanyOwner(SqlAlchemyRepository):

    def get_company_all(db: Session):
            return db.query(Company).all()

    def create_company(self, db: Session, company: company_dto.CompanyCreate, owner_id: int):
        obj_in_data = company.dict(exclude_unset=True)
        obj_in_data["owner_id"] = owner_id
        return super().create(db=db, db_obj=Company, obj_in=obj_in_data)

    def update_company(
        self, id: int, db: Session, company: company_dto.CompanyUpdate, owner_obj: Owner
    ) -> Company:
        if (
            company := db.query(Company)
            .filter(Company.company_id == id)
            .first()
        ) is not None:
            for owner_company in owner_obj.owner_id:
                if owner_company.owner_id == company.owner_id:
                    obj_in_data = company.dict(exclude_unset=True)
                    obj_in_data = company["owner_id"] = owner_obj.owner_id
                    return super().update(db, db_obj=company, obj_in=obj_in_data)
        return None
        

    def delete_company(self, db: Session, company_id: int, owner_obj: Owner) -> Company:
        if (
            company := db.query(Company)
            .filter(Company.company_id == company_id)
            .first()
        ) is not None:
            for owner_company in owner_obj.owner_id:
                if owner_company.owner_id == company.owner_id:
                    db.delete(company)
                    db.commit()
                    return company_id
        return None


company_owner = CompanyOwner()