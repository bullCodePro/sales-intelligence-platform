from uuid import UUID

from sqlalchemy.orm import Session

from packages.companies.models import Company
from packages.enrichment.providers import CompanyProvider, SimulatedCompanyProvider


async def enrich_company(
    session: Session,
    organization_id: UUID,
    company_id: UUID,
    provider: CompanyProvider | None = None,
) -> Company:
    company = session.get(Company, company_id)
    if company is None or company.organization_id != organization_id:
        raise ValueError("Company not found")

    provider = provider or SimulatedCompanyProvider()
    enriched = await provider.enrich_company(company)

    company.domain = enriched.domain
    company.website_url = enriched.website_url
    company.industry = enriched.industry
    company.country = enriched.country
    company.employee_count = enriched.employee_count
    company.confidence = enriched.confidence
    company.notes = (
        f"{company.notes or ''}\n"
        f"Enriched by {enriched.source_name} at {enriched.observed_at.isoformat()}."
    ).strip()
    session.commit()
    session.refresh(company)
    return company
