from packages.companies.repository import create_company, list_companies
from packages.companies.schemas import CompanyCreate
from packages.icp.repository import create_icp
from packages.icp.schemas import ICPCreate
from packages.organizations.repository import create_organization
from packages.organizations.schemas import OrganizationCreate
from packages.shared.config import settings
from packages.shared.database import SessionLocal


def main() -> None:
    with SessionLocal() as session:
        organization = create_organization(
            session,
            OrganizationCreate(
                name=settings.default_organization_name,
                description="Generic demo organization for local development.",
            ),
        )
        if list_companies(session, organization.id):
            print("Seed skipped: demo organization already has companies.")
            return

        create_icp(
            session,
            ICPCreate(
                organization_id=organization.id,
                name="Generic mid-market ICP",
                description="Reusable sample ICP. Replace criteria per workspace or client.",
                criteria={
                    "industries": ["Software", "Retail", "Logistics"],
                    "countries": ["United States", "Brazil", "Mexico"],
                    "min_employees": 100,
                    "max_employees": 2000,
                },
            ),
        )
        create_company(
            session,
            CompanyCreate(
                organization_id=organization.id,
                name="Example Target Account",
                domain="example.com",
                industry="Software",
                country="United States",
                employee_count=250,
                confidence=0.8,
            ),
        )
        print(f"Seeded organization {organization.id}.")


if __name__ == "__main__":
    main()
