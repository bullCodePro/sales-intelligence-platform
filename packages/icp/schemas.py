from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ICPCreate(BaseModel):
    organization_id: UUID
    workspace_id: UUID | None = None
    name: str
    description: str | None = None
    criteria: dict = {}


class ICPRead(ICPCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
