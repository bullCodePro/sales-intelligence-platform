from __future__ import annotations

from typing import Any

from packages.shared.db import connect


COMPANY_FIELDS = (
    "name",
    "domain",
    "industry",
    "country",
    "employee_count",
    "revenue_usd",
    "tech_stack",
    "notes",
)


def list_companies() -> list[dict[str, Any]]:
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT id, name, domain, industry, country, employee_count, revenue_usd,
                   tech_stack, notes, created_at
            FROM companies
            ORDER BY created_at DESC, id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def create_company(payload: dict[str, Any]) -> dict[str, Any]:
    values = {
        "name": str(payload.get("name", "")).strip(),
        "domain": str(payload.get("domain", "")).strip(),
        "industry": str(payload.get("industry", "")).strip(),
        "country": str(payload.get("country", "")).strip(),
        "employee_count": int(payload.get("employee_count") or 0),
        "revenue_usd": int(payload.get("revenue_usd") or 0),
        "tech_stack": str(payload.get("tech_stack", "")).strip(),
        "notes": str(payload.get("notes", "")).strip(),
    }

    missing = [field for field in ("name", "domain", "industry", "country") if not values[field]]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    with connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO companies
                (name, domain, industry, country, employee_count, revenue_usd, tech_stack, notes)
            VALUES
                (:name, :domain, :industry, :country, :employee_count, :revenue_usd, :tech_stack, :notes)
            """,
            values,
        )
        row = connection.execute(
            "SELECT * FROM companies WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return dict(row)
