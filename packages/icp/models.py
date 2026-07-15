from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column

from packages.shared.database import Base
from packages.shared.mixins import IdMixin, OrganizationScopedMixin, TimestampMixin


class ICP(IdMixin, OrganizationScopedMixin, TimestampMixin, Base):
    __tablename__ = "icps"

    workspace_id: Mapped[str | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="SET NULL"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    criteria: Mapped[dict] = mapped_column(JSON, default=dict)


class ScoringRule(IdMixin, OrganizationScopedMixin, TimestampMixin, Base):
    __tablename__ = "scoring_rules"

    icp_id: Mapped[str] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("icps.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    field: Mapped[str] = mapped_column(String(120), nullable=False)
    operator: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[dict] = mapped_column(JSON, default=dict)
    weight: Mapped[int] = mapped_column(default=10)
