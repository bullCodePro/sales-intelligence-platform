from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from packages.companies.models import Company


@dataclass(frozen=True)
class EnrichedCompanyData:
    domain: str | None
    website_url: str | None
    industry: str | None
    country: str | None
    employee_count: int | None
    source_name: str
    source_url: str | None
    confidence: float
    observed_at: datetime


class CompanyProvider(Protocol):
    async def enrich_company(self, company: Company) -> EnrichedCompanyData:
        ...


class SimulatedCompanyProvider:
    source_name = "simulated-company-provider"

    async def enrich_company(self, company: Company) -> EnrichedCompanyData:
        normalized = company.normalized_name.replace(" ", "")
        domain = company.domain or f"{normalized}.example.com"
        return EnrichedCompanyData(
            domain=domain,
            website_url=company.website_url or f"https://{domain}",
            industry=company.industry or "Unknown",
            country=company.country or "Unknown",
            employee_count=company.employee_count,
            source_name=self.source_name,
            source_url=None,
            confidence=0.35,
            observed_at=datetime.now(UTC),
        )
