from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    organization_id: UUID
    workspace_id: UUID | None = None
    name: str
    legal_name: str | None = None
    operating_group: str | None = None
    domain: str | None = None
    website_url: str | None = None
    industry: str | None = None
    country: str | None = None
    employee_count: int | None = Field(default=None, ge=0)
    confidence: float | None = Field(default=None, ge=0, le=1)
    notes: str | None = None


class CompanyRead(CompanyCreate):
    id: UUID
    normalized_name: str

    model_config = ConfigDict(from_attributes=True)
