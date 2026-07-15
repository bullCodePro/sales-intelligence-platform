from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.companies.models import Company
from packages.companies.schemas import CompanyCreate
from packages.shared.normalization import normalize_company_name


def create_company(session: Session, payload: CompanyCreate) -> Company:
    company = Company(
        **payload.model_dump(),
        normalized_name=normalize_company_name(payload.name),
    )
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


def list_companies(session: Session, organization_id: UUID) -> list[Company]:
    statement = (
        select(Company)
        .where(Company.organization_id == organization_id)
        .order_by(Company.created_at.desc())
    )
    return list(session.scalars(statement))


def find_duplicate_by_name(session: Session, organization_id: UUID, name: str) -> Company | None:
    statement = select(Company).where(
        Company.organization_id == organization_id,
        Company.normalized_name == normalize_company_name(name),
    )
    return session.scalar(statement)
