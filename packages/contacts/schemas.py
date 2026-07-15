from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ContactCreate(BaseModel):
    organization_id: UUID
    company_id: UUID
    full_name: str | None = None
    title: str | None = None
    role_category: str | None = None
    email: str | None = None
    linkedin_url: str | None = None
    source_name: str | None = None
    source_url: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    review_status: str = "pending"
    notes: str | None = None


class ContactRead(ContactCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
