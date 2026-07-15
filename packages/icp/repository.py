from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.icp.models import ICP
from packages.icp.schemas import ICPCreate


def create_icp(session: Session, payload: ICPCreate) -> ICP:
    icp = ICP(**payload.model_dump())
    session.add(icp)
    session.commit()
    session.refresh(icp)
    return icp


def list_icps(session: Session, organization_id: UUID) -> list[ICP]:
    statement = select(ICP).where(ICP.organization_id == organization_id).order_by(ICP.name)
    return list(session.scalars(statement))
