from typing import Any


def score_company(company: Any, criteria: dict) -> dict[str, Any]:
    score = 0
    reasons: list[str] = []

    industries = {value.lower() for value in criteria.get("industries", [])}
    countries = {value.lower() for value in criteria.get("countries", [])}
    min_employees = criteria.get("min_employees")
    max_employees = criteria.get("max_employees")

    industry = (company.industry or "").lower()
    country = (company.country or "").lower()
    employee_count = company.employee_count or 0

    if industries and industry in industries:
        score += 35
        reasons.append("industry match")

    if countries and country in countries:
        score += 25
        reasons.append("country match")

    if min_employees is not None and employee_count >= int(min_employees):
        score += 20
        reasons.append("minimum size match")

    if max_employees is None or employee_count <= int(max_employees):
        score += 10
        reasons.append("maximum size match")

    if company.confidence:
        score += round(company.confidence * 10)
        reasons.append("enrichment confidence")

    score = min(score, 100)
    tier = "A" if score >= 80 else "B" if score >= 60 else "C"

    return {
        "company_id": company.id,
        "company_name": company.name,
        "score": score,
        "tier": tier,
        "reasons": reasons or ["no matching ICP criteria"],
    }
