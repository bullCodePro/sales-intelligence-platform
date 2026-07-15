from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrganizationCreate(BaseModel):
    name: str
    description: str | None = None


class OrganizationRead(BaseModel):
    id: UUID
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class WorkspaceCreate(BaseModel):
    organization_id: UUID
    name: str
    description: str | None = None


class WorkspaceRead(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
