from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.contacts.models import Contact
from packages.contacts.schemas import ContactCreate


def create_contact(session: Session, payload: ContactCreate) -> Contact:
    contact = Contact(**payload.model_dump())
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


def list_contacts(session: Session, organization_id: UUID) -> list[Contact]:
    statement = (
        select(Contact)
        .where(Contact.organization_id == organization_id)
        .order_by(Contact.created_at.desc())
    )
    return list(session.scalars(statement))
