from __future__ import annotations

from typing import Any

from packages.companies.repository import list_companies


TARGET_INDUSTRIES = {"saas", "software", "fintech", "ecommerce", "b2b services"}
TARGET_COUNTRIES = {"united states", "usa", "uruguay", "argentina", "chile", "brazil"}
TARGET_TECH = {"salesforce", "hubspot", "segment", "stripe", "snowflake", "postgres"}


def score_company(company: dict[str, Any]) -> dict[str, Any]:
    industry = str(company.get("industry", "")).lower()
    country = str(company.get("country", "")).lower()
    tech_stack = {item.strip().lower() for item in str(company.get("tech_stack", "")).split(",")}
    employees = int(company.get("employee_count") or 0)
    revenue = int(company.get("revenue_usd") or 0)

    score = 20
    reasons: list[str] = []

    if industry in TARGET_INDUSTRIES:
        score += 25
        reasons.append("target industry")
    if country in TARGET_COUNTRIES:
        score += 15
        reasons.append("reachable market")
    if 25 <= employees <= 1000:
        score += 20
        reasons.append("ideal team size")
    if revenue >= 1_000_000:
        score += 10
        reasons.append("validated revenue")

    tech_overlap = sorted(tech_stack & TARGET_TECH)
    if tech_overlap:
        score += min(20, len(tech_overlap) * 7)
        reasons.append(f"uses {', '.join(tech_overlap)}")

    score = min(score, 100)
    tier = "A" if score >= 80 else "B" if score >= 60 else "C"

    return {
        "company_id": company["id"],
        "company_name": company["name"],
        "domain": company["domain"],
        "score": score,
        "tier": tier,
        "reasons": reasons or ["needs more qualification data"],
    }


def list_scores() -> list[dict[str, Any]]:
    return sorted(
        (score_company(company) for company in list_companies()),
        key=lambda item: item["score"],
        reverse=True,
    )
