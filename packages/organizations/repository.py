from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.organizations.models import Organization, Workspace
from packages.organizations.schemas import OrganizationCreate, WorkspaceCreate


def create_organization(session: Session, payload: OrganizationCreate) -> Organization:
    organization = Organization(**payload.model_dump())
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization


def list_organizations(session: Session) -> list[Organization]:
    return list(session.scalars(select(Organization).order_by(Organization.name)))


def create_workspace(session: Session, payload: WorkspaceCreate) -> Workspace:
    workspace = Workspace(**payload.model_dump())
    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    return workspace
