from __future__ import annotations

from packages.companies.repository import create_company, list_companies
from packages.shared.db import ensure_database


SAMPLE_COMPANIES = [
    {
        "name": "Northstar CRM",
        "domain": "northstarcrm.com",
        "industry": "SaaS",
        "country": "United States",
        "employee_count": 180,
        "revenue_usd": 12_000_000,
        "tech_stack": "Salesforce, Stripe, Snowflake",
        "notes": "Growing sales operations team and active RevOps hiring.",
    },
    {
        "name": "RioPay",
        "domain": "riopay.com",
        "industry": "Fintech",
        "country": "Uruguay",
        "employee_count": 75,
        "revenue_usd": 3_500_000,
        "tech_stack": "HubSpot, Postgres, Segment",
        "notes": "Regional payments company expanding outbound motion.",
    },
    {
        "name": "Old Harbor Logistics",
        "domain": "oldharborlogistics.com",
        "industry": "Logistics",
        "country": "Canada",
        "employee_count": 1400,
        "revenue_usd": 50_000_000,
        "tech_stack": "Excel, Oracle",
        "notes": "Large account, lower ICP fit for current motion.",
    },
]


def main() -> None:
    ensure_database()
    if list_companies():
        print("Seed skipped: database already has companies.")
        return

    for company in SAMPLE_COMPANIES:
        create_company(company)
    print(f"Seeded {len(SAMPLE_COMPANIES)} companies.")


if __name__ == "__main__":
    main()
