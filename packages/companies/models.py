from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.shared.database import Base
from packages.shared.mixins import IdMixin, OrganizationScopedMixin, TimestampMixin


class Company(IdMixin, OrganizationScopedMixin, TimestampMixin, Base):
    __tablename__ = "companies"

    workspace_id: Mapped[str | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="SET NULL"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    legal_name: Mapped[str | None] = mapped_column(String(255))
    operating_group: Mapped[str | None] = mapped_column(String(255))
    domain: Mapped[str | None] = mapped_column(String(255), index=True)
    website_url: Mapped[str | None] = mapped_column(String(500))
    industry: Mapped[str | None] = mapped_column(String(120), index=True)
    country: Mapped[str | None] = mapped_column(String(120), index=True)
    employee_count: Mapped[int | None] = mapped_column(Integer)
    confidence: Mapped[float | None]
    notes: Mapped[str | None] = mapped_column(Text)

    aliases: Mapped[list["CompanyAlias"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("organization_id", "normalized_name", name="uq_company_org_normalized_name"),
    )


class CompanyAlias(IdMixin, OrganizationScopedMixin, TimestampMixin, Base):
    __tablename__ = "company_aliases"

    company_id: Mapped[str] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    alias: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_alias: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    company: Mapped[Company] = relationship(back_populates="aliases")
