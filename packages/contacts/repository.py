from __future__ import annotations

from typing import Any

from packages.shared.db import connect


def list_contacts() -> list[dict[str, Any]]:
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT contacts.id, contacts.company_id, contacts.full_name, contacts.title,
                   contacts.email, contacts.linkedin_url, contacts.seniority,
                   contacts.created_at, companies.name AS company_name
            FROM contacts
            JOIN companies ON companies.id = contacts.company_id
            ORDER BY contacts.created_at DESC, contacts.id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def create_contact(payload: dict[str, Any]) -> dict[str, Any]:
    values = {
        "company_id": int(payload.get("company_id") or 0),
        "full_name": str(payload.get("full_name", "")).strip(),
        "title": str(payload.get("title", "")).strip(),
        "email": str(payload.get("email", "")).strip(),
        "linkedin_url": str(payload.get("linkedin_url", "")).strip(),
        "seniority": str(payload.get("seniority", "")).strip(),
    }

    missing = [field for field in ("company_id", "full_name", "title", "email") if not values[field]]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    with connect() as connection:
        company = connection.execute(
            "SELECT id FROM companies WHERE id = ?",
            (values["company_id"],),
        ).fetchone()
        if company is None:
            raise ValueError("Company does not exist")

        cursor = connection.execute(
            """
            INSERT INTO contacts
                (company_id, full_name, title, email, linkedin_url, seniority)
            VALUES
                (:company_id, :full_name, :title, :email, :linkedin_url, :seniority)
            """,
            values,
        )
        row = connection.execute(
            "SELECT * FROM contacts WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return dict(row)
